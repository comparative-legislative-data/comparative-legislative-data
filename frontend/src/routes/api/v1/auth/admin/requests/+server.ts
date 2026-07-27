import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import pool from '$lib/server/db';

export const GET: RequestHandler = async ({ locals }) => {
  if (!locals.user || !locals.user.is_super_user) {
    return json({ error: 'Unauthorized. Super User access required.' }, { status: 403 });
  }

  try {
    const res = await pool.query(
      'SELECT request_id, name, email, institution_role, research_reason, status, requested_at, reviewed_at FROM beta_access_requests ORDER BY requested_at DESC'
    );

    return json({
      success: true,
      total: res.rows.length,
      requests: res.rows
    });
  } catch (err: any) {
    console.error('Error fetching access requests:', err);
    return json({ error: 'Failed to retrieve access requests.' }, { status: 500 });
  }
};
