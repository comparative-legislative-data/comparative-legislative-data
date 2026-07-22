<script lang="ts">
  import { ArrowLeft, CheckCircle2, FileText, Globe, Layers, ShieldCheck, Database } from 'lucide-svelte';
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();

  let datasetSchema = $derived({
    '@context': 'https://schema.org',
    '@type': 'Dataset',
    'name': `${data.jurisdiction} Parliamentary Open Data Audit & Mapping Blueprint`,
    'description': `Field-by-field 3-tier provenance matrix, Hansard transcript resolution rules, rate limits, and structural API schemas for ${data.jurisdiction}.`,
    'url': `https://legislativedata.org/atlas/${data.jurisdiction}`,
    'license': 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
    'publisher': {
      '@type': 'Organization',
      'name': 'Comparative Legislative Data Project'
    },
    'includedInDataCatalog': {
      '@type': 'DataCatalog',
      'name': 'Global Parliamentary Data Atlas',
      'url': 'https://legislativedata.org/atlas'
    }
  });

  let breadcrumbSchema = $derived({
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    'itemListElement': [
      {
        '@type': 'ListItem',
        'position': 1,
        'name': 'Home',
        'item': 'https://legislativedata.org/'
      },
      {
        '@type': 'ListItem',
        'position': 2,
        'name': 'Data Atlas',
        'item': 'https://legislativedata.org/atlas'
      },
      {
        '@type': 'ListItem',
        'position': 3,
        'name': data.jurisdiction,
        'item': `https://legislativedata.org/atlas/${data.jurisdiction}`
      }
    ]
  });
</script>

<svelte:head>
  <title>{data.jurisdiction} Assembly Data Audit — Global Parliamentary Data Atlas</title>
  <meta name="description" content="Field-by-field 3-tier provenance matrix, Hansard transcript resolution rules, rate limits, and 5-bill typology audit for {data.jurisdiction}." />
  <meta name="keywords" content="{data.jurisdiction} parliament data, {data.jurisdiction} API audit, parliamentary open data schema, legislative dataset {data.jurisdiction}" />

  <meta property="og:title" content="{data.jurisdiction} Assembly Data Audit — Global Parliamentary Data Atlas" />
  <meta property="og:description" content="Field-by-field 3-tier provenance matrix, Hansard transcript resolution rules, and structural API schema for {data.jurisdiction}." />

  <!-- Google Scholar / Academic Citation Meta Tags -->
  <meta name="citation_title" content="{data.jurisdiction} Parliamentary Data Mapping & Audit Profile" />
  <meta name="citation_publisher" content="Comparative Legislative Data Project" />
  <meta name="citation_technical_report_number" content="Phase 0 Audit Profile: {data.jurisdiction}" />
  <meta name="citation_language" content="en" />

  <!-- Page Structured Data (JSON-LD) -->
  {@html `<script type="application/ld+json">${JSON.stringify(datasetSchema)}</script>`}
  {@html `<script type="application/ld+json">${JSON.stringify(breadcrumbSchema)}</script>`}
</svelte:head>

<div class="container page-padding">
  <!-- Back Button -->
  <a href="/atlas" class="back-link">
    <ArrowLeft size={16} /> Back to Global Data Atlas
  </a>

  <!-- Audit Header Banner -->
  <div class="card header-card">
    <div class="header-top">
      <div class="badge-group">
        <span class="badge badge-bicd">{data.jurisdiction}</span>
        <span class="badge badge-live">Phase 0 Mapping</span>
        <span class="badge badge-direct">REST API / XML</span>
        <span class="badge badge-enriched">3-Tier Provenance</span>
      </div>
    </div>

    <h1 class="audit-title">{data.jurisdiction} Parliamentary Data Mapping & Audit Profile</h1>
    <p class="audit-sub">
      Field-by-field 3-tier provenance matrix, Hansard transcript resolution rules, rate limits, and 5-bill typology audit results.
    </p>

    <div class="audit-meta-grid">
      <div class="meta-item">
        <span class="meta-label">Audit Status</span>
        <span class="meta-value">Phase 0 Mapping Blueprint</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Open License</span>
        <span class="meta-value">Open Parliament Licence v3.0 / OGL v3.0</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Target Cohort</span>
        <span class="meta-value">2019–2024 BICD Cohort 1</span>
      </div>
    </div>
  </div>

  <!-- Markdown Audit Content -->
  {#if data.content}
    <div class="card content-card prose">
      <pre class="raw-markdown">{data.content}</pre>
    </div>
  {:else}
    <div class="card placeholder-card">
      <FileText size={48} color="#6366f1" />
      <h3>{data.jurisdiction} Audit Profile</h3>
      <p>{data.message}</p>
      <a href="/atlas" class="btn-secondary">Return to Atlas Directory</a>
    </div>
  {/if}
</div>

<style>
  .page-padding {
    padding: 3rem 1.5rem;
  }

  .back-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-muted);
    font-size: 0.9rem;
    font-weight: 500;
    text-decoration: none;
    margin-bottom: 1.5rem;
    transition: color 0.2s ease;
  }
  .back-link:hover { color: var(--accent-cyan); }

  .header-card {
    margin-bottom: 2rem;
    background: linear-gradient(135deg, rgba(31, 41, 55, 0.9) 0%, rgba(17, 24, 39, 0.95) 100%);
    border: 1px solid var(--border-subtle);
  }

  .header-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.25rem;
  }

  .badge-group {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .audit-title {
    font-size: 2.25rem;
    margin-bottom: 0.5rem;
  }

  .audit-sub {
    color: var(--text-muted);
    font-size: 1.05rem;
    margin-bottom: 1.75rem;
  }

  .audit-meta-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.25rem;
    background: rgba(11, 15, 25, 0.6);
    border: 1px solid var(--border-subtle);
    border-radius: 0.75rem;
    padding: 1.25rem;
  }

  .meta-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .meta-label {
    font-size: 0.75rem;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .meta-value {
    font-size: 0.9rem;
    color: var(--text-main);
    font-weight: 500;
  }

  .content-card {
    padding: 2.5rem;
  }

  .raw-markdown {
    white-space: pre-wrap;
    font-family: var(--font-body);
    font-size: 0.95rem;
    line-height: 1.7;
    color: #e5e7eb;
    background: transparent;
    border: none;
    padding: 0;
  }

  .placeholder-card {
    text-align: center;
    padding: 4rem 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  @media (max-width: 768px) {
    .audit-meta-grid { grid-template-columns: 1fr; }
  }
</style>
