import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async () => {
  return json({
    jurisdiction: 'GB-SCT',
    export_format: 'Apache Parquet (Columnar Storage)',
    download_url: 'https://legislativedata.org/exports/GB-SCT_canonical_bills.parquet',
    duckdb_wasm_import_snippet: "SELECT * FROM read_parquet('https://legislativedata.org/exports/GB-SCT_canonical_bills.parquet');",
    last_modified: '2026-07-24T17:00:00Z',
    records_count: 473
  });
};
