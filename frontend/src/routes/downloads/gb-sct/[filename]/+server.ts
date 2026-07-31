import { error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import fs from 'fs';
import path from 'path';

export const GET: RequestHandler = async ({ params }) => {
  const { filename } = params;

  if (!filename) {
    throw error(400, 'Filename is required');
  }

  // Prevent path traversal attacks
  const sanitizedFilename = path.basename(filename);
  const filePath = path.join('/home/chessadmin/comparativelegislativedata/downloads/gb-sct', sanitizedFilename);

  if (!fs.existsSync(filePath)) {
    throw error(404, `File not found: ${sanitizedFilename}`);
  }

  try {
    const fileStream = fs.createReadStream(filePath);
    
    // Explicitly serve as raw application binary attachments so browsers save the archive itself
    let contentType = 'application/octet-stream';
    if (sanitizedFilename.endsWith('.gz')) {
      contentType = 'application/gzip';
    } else if (sanitizedFilename.endsWith('.csv')) {
      contentType = 'text/csv';
    }

    return new Response(fileStream as any, {
      headers: {
        'Content-Type': contentType,
        'Content-Disposition': `attachment; filename="${sanitizedFilename}"`,
        'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
      }
    });
  } catch (err: any) {
    console.error(`Failed to stream download file '${sanitizedFilename}':`, err);
    throw error(500, 'Failed to download file');
  }
};
