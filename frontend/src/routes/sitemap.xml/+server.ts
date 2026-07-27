import type { RequestHandler } from './$types';

export const GET: RequestHandler = async () => {
  const domain = 'https://legislativedata.org';
  const lastmod = new Date().toISOString().split('T')[0];
  const pages = [
    '',
    '/atlas',
    '/schema',
    '/api-docs',
    '/atlas/GB-UKP',
    '/atlas/GB-SCT',
    '/atlas/GB-WLS',
    '/atlas/GB-NIR',
    '/atlas/IM-TYN',
    '/atlas/JE-STJ',
    '/atlas/GG-STG',
    '/atlas/GI-GIB'
  ];

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages
  .map(
    (page) => `  <url>
    <loc>${domain}${page}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>${page === '' ? '1.0' : '0.8'}</priority>
  </url>`
  )
  .join('\n')}
</urlset>`;

  return new Response(sitemap, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, max-age=3600'
    }
  });
};
