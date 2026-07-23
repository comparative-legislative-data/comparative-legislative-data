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

  return {
    jurisdiction: code,
    blueprint,
    content: rawContent,
    liveDatasetMetrics: null,
    message: blueprint || rawContent ? null : `Audit blueprint for ${code} is currently being compiled under Phase 0.`
  };
};
