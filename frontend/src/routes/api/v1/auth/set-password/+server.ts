import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import pool from '$lib/server/db';
import crypto from 'crypto';

export const POST: RequestHandler = async ({ request, cookies, locals }) => {
  try {
    const { email, password } = await request.json();

    const targetEmail = (email || locals.user?.email || '').trim().toLowerCase();

    if (!targetEmail) {
      return json({ error: 'User email is required to set password.' }, { status: 400 });
    }

    if (!password || password.length < 6) {
      return json({ error: 'Password must be at least 6 characters long.' }, { status: 400 });
    }

    const passHash = crypto.createHash('sha256').update(password).digest('hex');

    // Update password in users table
    const res = await pool.query(
      'UPDATE users SET password_hash = $1 WHERE email = $2 RETURNING user_id, email, name, institution_role, is_super_user',
      [passHash, targetEmail]
    );

    if (res.rows.length === 0) {
      return json({ error: 'Account not found for email address.' }, { status: 404 });
    }

    const user = res.rows[0];

    // Automatically log user in by setting session cookie
    const sessionPayload = {
      email: user.email,
      name: user.name,
      is_super_user: Boolean(user.is_super_user),
      logged_in_at: new Date().toISOString()
    };

    const sessionToken = Buffer.from(JSON.stringify(sessionPayload)).toString('base64');
    cookies.set('session', sessionToken, {
      path: '/',
      httpOnly: true,
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 7
    });

    return json({
      success: true,
      message: 'Password set successfully! Logging you in now...',
      user: {
        user_id: user.user_id,
        email: user.email,
        name: user.name,
        role: user.institution_role,
        is_super_user: Boolean(user.is_super_user)
      }
    });

  } catch (err: any) {
    console.error('Error setting password:', err);
    return json({ error: 'Failed to set password.' }, { status: 500 });
  }
};
