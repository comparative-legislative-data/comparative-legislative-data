import { error } from '@sveltejs/kit';
import { load as parseYaml } from 'js-yaml';
import fs from 'fs';
import path from 'path';
import type { PageServerLoad } from './$types';

// Vite eager raw imports — bundles YAML audit blueprints directly into production JS!
const yamlModules = import.meta.glob('../../../../institutions/*/AUDIT_BLUEPRINT.yaml', { query: '?raw', eager: true }) as Record<string, { default: string } | string>;

export const load: PageServerLoad = async ({ params }) => {
  const { jurisdiction } = params;
  const code = jurisdiction.toUpperCase();

  let blueprint: any = null;

  // 1. Try Vite static bundle import (Production safe)
  const globKey = `../../../../institutions/${code}/AUDIT_BLUEPRINT.yaml`;
  const rawGlob = yamlModules[globKey];

  if (rawGlob) {
    try {
      const rawYaml = typeof rawGlob === 'string' ? rawGlob : rawGlob.default;
      blueprint = parseYaml(rawYaml) as any;
    } catch (e) {
      console.error(`Failed to parse bundled YAML for ${code}:`, e);
    }
  }

  // 2. Fallback to filesystem resolution if running in local dev or VPS
  if (!blueprint) {
    const candidatePaths = [
      path.resolve(process.cwd(), '../institutions', code, 'AUDIT_BLUEPRINT.yaml'),
      path.resolve(process.cwd(), 'institutions', code, 'AUDIT_BLUEPRINT.yaml'),
      path.resolve(process.cwd(), '../../institutions', code, 'AUDIT_BLUEPRINT.yaml'),
      path.resolve('/home/chessadmin/comparativelegislativedata/institutions', code, 'AUDIT_BLUEPRINT.yaml'),
      // Fallback legacy paths
      path.resolve(process.cwd(), '../docs/audits', `${code}.yaml`),
      path.resolve(process.cwd(), 'docs/audits', `${code}.yaml`),
      path.resolve('/home/chessadmin/comparativelegislativedata/docs/audits', `${code}.yaml`)
    ];

    for (const yamlPath of candidatePaths) {
      if (fs.existsSync(yamlPath)) {
        try {
          const rawYaml = fs.readFileSync(yamlPath, 'utf-8');
          blueprint = parseYaml(rawYaml) as any;
          if (blueprint) break;
        } catch (e) {
          console.error(`Failed to read filesystem YAML from ${yamlPath}:`, e);
        }
      }
    }
  }

  return {
    jurisdiction: code,
    blueprint,
    liveDatasetMetrics: null,
    message: blueprint ? null : `Audit blueprint for ${code} is currently being compiled under Phase 0.`
  };
};
