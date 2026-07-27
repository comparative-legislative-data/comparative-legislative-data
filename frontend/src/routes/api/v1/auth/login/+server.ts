import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import pool from '$lib/server/db';
import crypto from 'crypto';

export const POST: RequestHandler = async ({ request, cookies }) => {
  try {
    const { email, password } = await request.json();

    if (!email || !password) {
      return json({ error: 'Email and password are required.' }, { status: 400 });
    }

    const cleanEmail = email.trim().toLowerCase();
    const superEmail = (process.env.SUPER_USER_EMAIL || 'admin@legislativedata.org').trim().toLowerCase();
    const superPassword = process.env.SUPER_USER_PASSWORD || 'SecureSuperPassword123!';

    // Check Super User Login
    if (cleanEmail === superEmail && password === superPassword) {
      const sessionPayload = {
        email: cleanEmail,
        name: 'Platform Super User',
        is_super_user: true,
        logged_in_at: new Date().toISOString()
      };

      const sessionToken = Buffer.from(JSON.stringify(sessionPayload)).toString('base64');
      cookies.set('session', sessionToken, {
        path: '/',
        httpOnly: true,
        sameSite: 'lax',
        maxAge: 60 * 60 * 24 * 7 // 7 days
      });

      return json({
        success: true,
        user: {
          user_id: 0,
          email: cleanEmail,
          name: 'Platform Super User',
          role: 'Platform Administrator',
          is_super_user: true
        }
      });
    }

    // Check Standard User Login
    const passHash = crypto.createHash('sha256').update(password).digest('hex');
    const res = await pool.query(
      'SELECT user_id, email, name, institution_role, is_super_user, is_active FROM users WHERE email = $1 AND password_hash = $2 AND is_active = TRUE',
      [cleanEmail, passHash]
    );

    if (res.rows.length === 0) {
      return json({ error: 'Invalid email or password.' }, { status: 401 });
    }

    const user = res.rows[0];
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
      user: {
        user_id: user.user_id,
        email: user.email,
        name: user.name,
        role: user.institution_role,
        is_super_user: Boolean(user.is_super_user)
      }
    });

  } catch (err: any) {
    console.error('Error in login endpoint:', err);
    return json({ error: 'Login failed due to a server error.' }, { status: 500 });
  }
};
