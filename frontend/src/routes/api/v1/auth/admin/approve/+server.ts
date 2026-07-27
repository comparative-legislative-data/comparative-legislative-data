import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import pool from '$lib/server/db';
import crypto from 'crypto';
import { Resend } from 'resend';

export const POST: RequestHandler = async ({ request, locals, url }) => {
  if (!locals.user || !locals.user.is_super_user) {
    return json({ error: 'Unauthorized. Super User access required.' }, { status: 403 });
  }

  try {
    const { request_id } = await request.json();
    if (!request_id) {
      return json({ error: 'request_id is required.' }, { status: 400 });
    }

    const reqRes = await pool.query(
      'SELECT name, email, institution_role, research_reason FROM beta_access_requests WHERE request_id = $1',
      [request_id]
    );

    if (reqRes.rows.length === 0) {
      return json({ error: 'Request not found.' }, { status: 404 });
    }

    const applicant = reqRes.rows[0];

    // 1. Update status to APPROVED
    await pool.query(
      "UPDATE beta_access_requests SET status = 'APPROVED', reviewed_at = CURRENT_TIMESTAMP WHERE request_id = $1",
      [request_id]
    );

    // 2. Upsert user in users table
    await pool.query(
      `INSERT INTO users (email, name, institution_role, is_super_user, is_active)
       VALUES ($1, $2, $3, FALSE, TRUE)
       ON CONFLICT (email) DO UPDATE SET
         name = EXCLUDED.name,
         institution_role = EXCLUDED.institution_role,
         is_active = TRUE`,
      [applicant.email, applicant.name, applicant.institution_role]
    );

    // 3. Generate raw token and hash
    const rawToken = crypto.randomBytes(32).toString('hex');
    const tokenHash = crypto.createHash('sha256').update(rawToken).digest('hex');
    const expiresAt = new Date(Date.now() + 72 * 60 * 60 * 1000); // 72 hours

    await pool.query(
      `INSERT INTO auth_tokens (token_hash, email, token_type, expires_at)
       VALUES ($1, $2, 'SIGNUP', $3)`,
      [tokenHash, applicant.email, expiresAt]
    );

    // 4. Construct Signup Link
    const origin = url.origin.includes('localhost') ? url.origin : 'https://legislativedata.org';
    const signupLink = `${origin}/?action=verify_signup&token=${rawToken}&email=${encodeURIComponent(applicant.email)}`;

    // 5. Send Email via Resend API
    let emailSent = false;
    let emailError: string | null = null;

    const resendApiKey = process.env.RESEND_API_KEY;
    if (resendApiKey && resendApiKey !== 're_123456789_abcdefg') {
      try {
        const resend = new Resend(resendApiKey);
        const fromEmail = process.env.RESEND_FROM_EMAIL || 'access@legislativedata.org';

        await resend.emails.send({
          from: `Comparative Legislative Data Platform <${fromEmail}>`,
          to: applicant.email,
          subject: 'Beta Access Approved — Set Your Password',
          html: `
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0f172a; color: #f8fafc; padding: 24px; border-radius: 8px;">
              <h2 style="color: #38bdf8; margin-top: 0;">Beta Access Approved</h2>
              <p>Dear ${applicant.name},</p>
              <p>Your request for beta access to the <strong>Comparative Legislative Data Platform</strong> has been approved by the platform administrator!</p>
              <p>Please click the link below to set your password and access the platform:</p>
              <p style="margin: 24px 0;">
                <a href="${signupLink}" style="background: #0284c7; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">Set Your Password & Access Platform</a>
              </p>
              <p style="font-size: 12px; color: #94a3b8;">This signup link is valid for 72 hours. If you did not request access, please ignore this email.</p>
              <hr style="border: none; border-top: 1px solid #334155; margin: 24px 0;" />
              <p style="font-size: 11px; color: #64748b;">Comparative Legislative Data Platform &bull; Open Science Data Infrastructure</p>
            </div>
          `
        });
        emailSent = true;
      } catch (err: any) {
        console.error('Resend API dispatch error:', err);
        emailError = err.message || 'Failed to dispatch email via Resend API.';
      }
    } else {
      emailError = 'RESEND_API_KEY not configured. Signup link generated for manual copy.';
    }

    return json({
      success: true,
      message: emailSent ? `Access approved and signup email sent to ${applicant.email}.` : `Access approved! ${emailError}`,
      email_sent: emailSent,
      signup_link: signupLink,
      applicant: {
        name: applicant.name,
        email: applicant.email
      }
    });

  } catch (err: any) {
    console.error('Error approving request:', err);
    return json({ error: 'Failed to approve access request.' }, { status: 500 });
  }
};
