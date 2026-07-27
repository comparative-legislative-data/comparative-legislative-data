import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import pool from '$lib/server/db';
import crypto from 'crypto';

export const POST: RequestHandler = async ({ request, cookies }) => {
  try {
    const { token, email } = await request.json();

    if (!token || !email) {
      return json({ error: 'Token and email are required.' }, { status: 400 });
    }

    const cleanEmail = email.trim().toLowerCase();
    const tokenHash = crypto.createHash('sha256').update(token).digest('hex');

    const res = await pool.query(
      `SELECT token_id, email, token_type, expires_at, used_at
       FROM auth_tokens
       WHERE token_hash = $1 AND email = $2 AND used_at IS NULL AND expires_at > CURRENT_TIMESTAMP`,
      [tokenHash, cleanEmail]
    );

    if (res.rows.length === 0) {
      return json({ error: 'Invalid or expired access token.' }, { status: 400 });
    }

    const tokenRow = res.rows[0];

    // Mark token as used
    await pool.query('UPDATE auth_tokens SET used_at = CURRENT_TIMESTAMP WHERE token_id = $1', [tokenRow.token_id]);

    // Check if Super User
    const superEmail = (process.env.SUPER_USER_EMAIL || 'admin@legislativedata.org').trim().toLowerCase();
    const isSuper = cleanEmail === superEmail;

    let userObj = {
      user_id: 0,
      email: cleanEmail,
      name: isSuper ? 'Platform Super User' : 'Researcher',
      role: 'Beta Researcher',
      is_super_user: isSuper
    };

    if (!isSuper) {
      const uRes = await pool.query(
        'SELECT user_id, email, name, institution_role, is_super_user FROM users WHERE email = $1',
        [cleanEmail]
      );
      if (uRes.rows.length > 0) {
        const u = uRes.rows[0];
        userObj = {
          user_id: u.user_id,
          email: u.email,
          name: u.name,
          role: u.institution_role,
          is_super_user: Boolean(u.is_super_user)
        };
      }
    }

    // Set Session Cookie
    const sessionPayload = {
      email: userObj.email,
      name: userObj.name,
      is_super_user: userObj.is_super_user,
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
      user: userObj,
      token_type: tokenRow.token_type
    });

  } catch (err: any) {
    console.error('Error verifying token:', err);
    return json({ error: 'Token verification failed.' }, { status: 500 });
  }
};
