import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import pool from '$lib/server/db';
import crypto from 'crypto';

export const POST: RequestHandler = async ({ request, locals }) => {
  if (!locals.user) {
    return json({ error: 'Unauthorized. Login required.' }, { status: 401 });
  }

  try {
    const { new_password } = await request.json();

    if (!new_password || new_password.length < 6) {
      return json({ error: 'New password must be at least 6 characters long.' }, { status: 400 });
    }

    const passHash = crypto.createHash('sha256').update(new_password).digest('hex');

    if (locals.user.is_super_user) {
      return json({ message: 'Super User password is managed securely via environment variables (.env.local).' });
    }

    await pool.query(
      'UPDATE users SET password_hash = $1 WHERE email = $2',
      [passHash, locals.user.email]
    );

    return json({
      success: true,
      message: 'Your password has been updated successfully!'
    });

  } catch (err: any) {
    console.error('Error changing password:', err);
    return json({ error: 'Failed to update password.' }, { status: 500 });
  }
};
