import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import pool from '$lib/server/db';
import crypto from 'crypto';
import { Resend } from 'resend';

export const POST: RequestHandler = async ({ request, url }) => {
  try {
    const { email } = await request.json();

    if (!email) {
      return json({ error: 'Email address is required.' }, { status: 400 });
    }

    const cleanEmail = email.trim().toLowerCase();

    // Check if user exists or is super user
    const superEmail = (process.env.SUPER_USER_EMAIL || 'admin@legislativedata.org').trim().toLowerCase();
    const isSuper = cleanEmail === superEmail;

    let userExists = isSuper;
    let userName = isSuper ? 'Platform Super User' : 'Researcher';

    if (!isSuper) {
      const res = await pool.query('SELECT name, is_active FROM users WHERE email = $1 AND is_active = TRUE', [cleanEmail]);
      if (res.rows.length > 0) {
        userExists = true;
        userName = res.rows[0].name;
      }
    }

    if (!userExists) {
      // Don't reveal if account exists for security, return friendly generic message
      return json({
        success: true,
        message: 'If an active account exists for this email, a Magic Link has been sent!'
      });
    }

    // Generate Magic Link token
    const rawToken = crypto.randomBytes(32).toString('hex');
    const tokenHash = crypto.createHash('sha256').update(rawToken).digest('hex');
    const expiresAt = new Date(Date.now() + 60 * 60 * 1000); // 1 hour

    await pool.query(
      `INSERT INTO auth_tokens (token_hash, email, token_type, expires_at)
       VALUES ($1, $2, 'MAGIC_LINK', $3)`,
      [tokenHash, cleanEmail, expiresAt]
    );

    const origin = url.origin.includes('localhost') ? url.origin : 'https://legislativedata.org';
    const magicLink = `${origin}/?action=magic_login&token=${rawToken}&email=${encodeURIComponent(cleanEmail)}`;

    let emailSent = false;
    let emailError: string | null = null;

    const resendApiKey = process.env.RESEND_API_KEY;
    if (resendApiKey && resendApiKey !== 're_123456789_abcdefg') {
      try {
        const resend = new Resend(resendApiKey);
        const fromEmail = process.env.RESEND_FROM_EMAIL || 'access@legislativedata.org';

        await resend.emails.send({
          from: `Comparative Legislative Data Platform <${fromEmail}>`,
          to: cleanEmail,
          subject: 'One-Time Magic Link Login',
          html: `
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0f172a; color: #f8fafc; padding: 24px; border-radius: 8px;">
              <h2 style="color: #38bdf8; margin-top: 0;">One-Time Magic Link Login</h2>
              <p>Hello ${userName},</p>
              <p>Click the link below to instantly log in to your <strong>Comparative Legislative Data Platform</strong> account:</p>
              <p style="margin: 24px 0;">
                <a href="${magicLink}" style="background: #0284c7; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">Log In Instantly to Platform</a>
              </p>
              <p style="font-size: 12px; color: #94a3b8;">This Magic Link is valid for 1 hour and can only be used once. Once logged in, you can update your password anytime in User Settings.</p>
              <hr style="border: none; border-top: 1px solid #334155; margin: 24px 0;" />
              <p style="font-size: 11px; color: #64748b;">Comparative Legislative Data Platform &bull; Open Science Data Infrastructure</p>
            </div>
          `
        });
        emailSent = true;
      } catch (err: any) {
        console.error('Magic Link Resend API error:', err);
        emailError = err.message;
      }
    } else {
      emailError = 'RESEND_API_KEY not configured. Link generated for manual copy.';
    }

    return json({
      success: true,
      message: 'If an active account exists for this email, a Magic Link has been sent!',
      email_sent: emailSent,
      magic_link: magicLink
    });

  } catch (err: any) {
    console.error('Error in magic-link endpoint:', err);
    return json({ error: 'Failed to generate Magic Link.' }, { status: 500 });
  }
};
