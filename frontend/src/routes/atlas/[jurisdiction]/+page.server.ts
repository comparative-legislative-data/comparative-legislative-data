import { error } from '@sveltejs/kit';
import fs from 'fs';
import path from 'path';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params }) => {
  const { jurisdiction } = params;
  const docsDir = path.resolve('../docs/mappings');
  const filePath = path.join(docsDir, `${jurisdiction.toUpperCase()}.md`);

  if (!fs.existsSync(filePath)) {
    return {
      jurisdiction: jurisdiction.toUpperCase(),
      content: null,
      message: `Audit guide for ${jurisdiction.toUpperCase()} is currently being compiled under Phase 0 Sub-Task 0.2.`
    };
  }

  try {
    const rawContent = fs.readFileSync(filePath, 'utf-8');
    return {
      jurisdiction: jurisdiction.toUpperCase(),
      content: rawContent,
      message: null
    };
  } catch (e) {
    throw error(500, `Failed to load audit guide for ${jurisdiction}`);
  }
};
