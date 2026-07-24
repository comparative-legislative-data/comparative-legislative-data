import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import fs from 'fs';
import path from 'path';

export const GET: RequestHandler = async ({ url }) => {
  const limit = parseInt(url.searchParams.get('limit') || '50');
  const initiatorType = url.searchParams.get('initiator_type');

  const jsonPaths = [
    path.resolve(process.cwd(), 'static/data/GB-SCT_canonical_bills.json'),
    path.resolve(process.cwd(), 'client/data/GB-SCT_canonical_bills.json'),
    path.resolve('/home/chessadmin/comparativelegislativedata/frontend/static/data/GB-SCT_canonical_bills.json')
  ];

  let rawData: any[] = [];
  const targetPath = jsonPaths.find(p => fs.existsSync(p));

  if (targetPath) {
    try {
      rawData = JSON.parse(fs.readFileSync(targetPath, 'utf-8'));
    } catch (e) {
      console.error('Failed to parse static JSON bills dataset:', e);
    }
  }

  if (initiatorType) {
    rawData = rawData.filter(b => b.initiator_type === initiatorType);
  }

  const slicedData = rawData.slice(0, limit);

  return json({
    jurisdiction: 'GB-SCT',
    legislative_body: 'Scottish Parliament (Pàrlamaid na h-Alba)',
    total_records: rawData.length,
    returned_records: slicedData.length,
    limit,
    schema_version: 'v2.8.0',
    provenance_baseline: 'Pass 1 Ground-Truth Baseline (51 Native + 21 Derived Deterministic)',
    data: slicedData
  });
};
