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

  // Check if declarative YAML blueprint exists
  if (fs.existsSync(yamlPath)) {
    try {
      const rawYaml = fs.readFileSync(yamlPath, 'utf-8');
      const blueprint = parseYaml(rawYaml) as any;
      return {
        jurisdiction: code,
        blueprint,
        content: null,
        message: null
      };
    } catch (e) {
      console.error(`Failed to parse YAML audit blueprint for ${code}:`, e);
    }
  }

  // Fallback to Markdown guide if available
  if (fs.existsSync(mdPath)) {
    try {
      const rawContent = fs.readFileSync(mdPath, 'utf-8');
      return {
        jurisdiction: code,
        blueprint: null,
        content: rawContent,
        message: null
      };
    } catch (e) {
      throw error(500, `Failed to load audit guide for ${code}`);
    }
  }

  return {
    jurisdiction: code,
    blueprint: null,
    content: null,
    message: `Audit blueprint for ${code} is currently being compiled under Phase 0.`
  };
};
