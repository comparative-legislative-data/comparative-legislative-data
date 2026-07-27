import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

const SP_API_BASE = 'https://data.parliament.scot/api';

export const GET: RequestHandler = async ({ params, url, fetch }) => {
  const { endpoint } = params;

  if (!endpoint) {
    return json({ error: 'Endpoint parameter is required' }, { status: 400 });
  }

  try {
    // Construct target URL using exact casing from route parameters and appending search query parameters
    const targetUrl = `${SP_API_BASE}/${endpoint}${url.search}`;

    const response = await fetch(targetUrl, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    });

    if (!response.ok) {
      return json({ 
        error: `Host assembly returned status ${response.status}`,
        details: await response.text()
      }, { status: response.status });
    }

    const data = await response.json();

    // Zero transformation: Return JSON exactly as received from host.
    return json(data, {
      headers: {
        'Cache-Control': 'public, max-age=3600',
        'Access-Control-Allow-Origin': '*'
      }
    });

  } catch (error: any) {
    console.error(`Proxy error fetching ${endpoint}:`, error);
    return json({ error: 'Failed to fetch from host assembly', details: error.message }, { status: 500 });
  }
};
