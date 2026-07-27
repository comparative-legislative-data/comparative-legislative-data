import type { RequestHandler } from './$types';

export const GET: RequestHandler = async () => {
  const robots = `User-agent: *
Allow: /

Sitemap: https://legislativedata.org/sitemap.xml
`;

  return new Response(robots, {
    headers: {
      'Content-Type': 'text/plain'
    }
  });
};
