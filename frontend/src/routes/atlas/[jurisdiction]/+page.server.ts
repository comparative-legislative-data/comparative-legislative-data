import { error } from '@sveltejs/kit';
import fs from 'fs';
import path from 'path';
import { load as parseYaml } from 'js-yaml';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params }) => {
  const { jurisdiction } = params;
  const code = jurisdiction.toUpperCase();

  const yamlPath = path.resolve(`../docs/audits/${code}.yaml`);
  const mdPath = path.resolve(`../docs/mappings/${code}.md`);

  let blueprint: any = null;
  if (fs.existsSync(yamlPath)) {
    try {
      const rawYaml = fs.readFileSync(yamlPath, 'utf-8');
      blueprint = parseYaml(rawYaml) as any;
    } catch (e) {
      console.error(`Failed to parse YAML audit blueprint for ${code}:`, e);
    }
  }

  let rawContent: string | null = null;
  if (!blueprint && fs.existsSync(mdPath)) {
    try {
      rawContent = fs.readFileSync(mdPath, 'utf-8');
    } catch (e) {
      throw error(500, `Failed to load audit guide for ${code}`);
    }
  }

  // Simulated / Server-side DB metrics for vertical slice
  let liveDatasetMetrics: any = null;
  if (code === 'GB-SCT') {
    liveDatasetMetrics = {
      status: 'PHASE_1_INGESTED',
      total_bills_cohort: 101,
      enacted_acts: 89,
      pending_bills: 12,
      cohort_window: '2019–2024 (Session 5 & 6)',
      last_ingestion_sync: '2026-07-22 21:11 UTC',
      provenance_hashes_count: 101,
      license: 'Open Government Licence v3.0 / Open Data Senedd/Holyrood'
    };
  }

  return {
    jurisdiction: code,
    blueprint,
    content: rawContent,
    liveDatasetMetrics,
    message: blueprint || rawContent ? null : `Audit blueprint for ${code} is currently being compiled under Phase 0.`
  };
};
