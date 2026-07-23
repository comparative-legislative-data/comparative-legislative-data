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
    const text = await response.text();

    let data: any;
    let isJson = false;

    // Holyrood API returns application/octet-stream for some JSON endpoints
    const trimmed = text.trim();
    if (trimmed.startsWith('{') || trimmed.startsWith('[')) {
      try {
        data = JSON.parse(trimmed);
        isJson = true;
      } catch {
        data = text.substring(0, 5000) + (text.length > 5000 ? '\n...[truncated HTML/text]' : '');
      }
    } else {
      data = text.substring(0, 5000) + (text.length > 5000 ? '\n...[truncated HTML/text]' : '');
    }

    let totalRecords = 1;
    let sampleData = data;
    let isTruncated = false;

    if (Array.isArray(data)) {
      totalRecords = data.length;
      if (data.length > 20) {
        sampleData = data.slice(0, 20);
        isTruncated = true;
      }
    }

    return json({
      status: response.status,
      statusText: response.statusText,
      elapsedMs,
      contentType,
      isJson,
      totalRecords,
      isTruncated,
      payloadBytes: text.length,
      data: sampleData
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
