import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import pool from '$lib/server/db';

export const POST: RequestHandler = async ({ request }) => {
  try {
    const body = await request.json();
    const { name, email, institution_role, research_reason } = body;

    if (!name || !email || !institution_role || !research_reason) {
      return json({ error: 'All fields (Name, Email, Role, Reason) are required.' }, { status: 400 });
    }

    const cleanEmail = email.trim().toLowerCase();

    // Check existing request or user
    const checkUser = await pool.query('SELECT user_id FROM users WHERE email = $1', [cleanEmail]);
    if (checkUser.rows.length > 0) {
      return json({ error: 'An active user account already exists with this email address.' }, { status: 400 });
    }

    const checkReq = await pool.query('SELECT request_id, status FROM beta_access_requests WHERE email = $1', [cleanEmail]);
    if (checkReq.rows.length > 0) {
      const existing = checkReq.rows[0];
      if (existing.status === 'PENDING') {
        return json({ message: 'Your request for beta access is already pending review by the platform administrator.', status: 'PENDING' });
      }
    }

    // Insert request
    await pool.query(
      `INSERT INTO beta_access_requests (name, email, institution_role, research_reason, status)
       VALUES ($1, $2, $3, $4, 'PENDING')
       ON CONFLICT (email) DO UPDATE SET
         name = EXCLUDED.name,
         institution_role = EXCLUDED.institution_role,
         research_reason = EXCLUDED.research_reason,
         status = 'PENDING',
         requested_at = CURRENT_TIMESTAMP`,
      [name.trim(), cleanEmail, institution_role.trim(), research_reason.trim()]
    );

    return json({
      success: true,
      message: 'Your beta access request has been submitted successfully! You will receive an email once your request is reviewed.',
      email: cleanEmail
    });

  } catch (err: any) {
    console.error('Error in request-access endpoint:', err);
    return json({ error: 'Failed to submit beta access request. Please try again.' }, { status: 500 });
  }
};
