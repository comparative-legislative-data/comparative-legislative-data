import type { Handle } from '@sveltejs/kit';
import pool from '$lib/server/db';

export const handle: Handle = async ({ event, resolve }) => {
  const sessionCookie = event.cookies.get('session');
  event.locals.user = null;

  if (sessionCookie) {
    try {
      const sessionData = JSON.parse(Buffer.from(sessionCookie, 'base64').toString('utf-8'));
      
      // Check Super User match
      const superEmail = (process.env.SUPER_USER_EMAIL || 'admin@legislativedata.org').trim().toLowerCase();
      if (sessionData.email && sessionData.email.trim().toLowerCase() === superEmail && sessionData.is_super_user) {
        event.locals.user = {
          user_id: 0,
          email: sessionData.email,
          name: 'Platform Super User',
          role: 'Platform Administrator',
          is_super_user: true
        };
      } else {
        const res = await pool.query(
          'SELECT user_id, email, name, institution_role, is_super_user, is_active FROM users WHERE email = $1 AND is_active = TRUE',
          [sessionData.email]
        );
        if (res.rows.length > 0) {
          const row = res.rows[0];
          event.locals.user = {
            user_id: row.user_id,
            email: row.email,
            name: row.name,
            role: row.institution_role,
            is_super_user: Boolean(row.is_super_user)
          };
        }
      }
    } catch (e) {
      event.cookies.delete('session', { path: '/' });
    }
  }

  return resolve(event);
};
