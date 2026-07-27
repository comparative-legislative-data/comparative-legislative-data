import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import pool from '$lib/server/db';

export const POST: RequestHandler = async ({ request, locals }) => {
  if (!locals.user || !locals.user.is_super_user) {
    return json({ error: 'Unauthorized. Super User access required.' }, { status: 403 });
  }

  try {
    const { request_id } = await request.json();
    if (!request_id) {
      return json({ error: 'request_id is required.' }, { status: 400 });
    }

    await pool.query(
      "UPDATE beta_access_requests SET status = 'REJECTED', reviewed_at = CURRENT_TIMESTAMP WHERE request_id = $1",
      [request_id]
    );

    return json({
      success: true,
      message: 'Access request has been rejected.'
    });

  } catch (err: any) {
    console.error('Error rejecting request:', err);
    return json({ error: 'Failed to reject access request.' }, { status: 500 });
  }
};
