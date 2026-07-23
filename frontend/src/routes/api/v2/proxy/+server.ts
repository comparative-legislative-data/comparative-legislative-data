import { json, type RequestHandler } from '@sveltejs/kit';

export const GET: RequestHandler = async ({ url }) => {
  const targetUrl = url.searchParams.get('url');

  if (!targetUrl) {
    return json({ error: 'Missing target URL parameter' }, { status: 400 });
  }

  // Security check: Only allow http and https protocols
  try {
    const parsed = new URL(targetUrl);
    if (!['http:', 'https:'].includes(parsed.protocol)) {
      return json({ error: 'Invalid URL protocol' }, { status: 400 });
    }
  } catch (err) {
    return json({ error: 'Invalid URL format' }, { status: 400 });
  }

  const startTime = Date.now();

  try {
    const response = await fetch(targetUrl, {
      headers: {
        'User-Agent': 'ComparativeLegislativeDataPlatform/2.8.0 (+https://legislativedata.org)',
        'Accept': 'application/json, text/plain, */*'
      }
    });

    const elapsedMs = Date.now() - startTime;
    const contentType = response.headers.get('content-type') || '';

    let data: any;
    let isJson = false;

    if (contentType.includes('application/json') || contentType.includes('json')) {
      data = await response.json();
      isJson = true;
    } else {
      const text = await response.text();
      try {
        data = JSON.parse(text);
        isJson = true;
      } catch {
        data = text.substring(0, 5000) + (text.length > 5000 ? '\n...[truncated HTML/text]' : '');
      }
    }

    return json({
      status: response.status,
      statusText: response.statusText,
      elapsedMs,
      contentType,
      isJson,
      data
    });
  } catch (error: any) {
    return json({
      status: 500,
      statusText: 'Fetch Failed',
      elapsedMs: Date.now() - startTime,
      error: error?.message || 'Network fetch error'
    }, { status: 500 });
  }
};
