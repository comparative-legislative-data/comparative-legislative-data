<script lang="ts">
  import { ArrowLeft, CheckCircle2, FileText, Globe, Layers, ShieldCheck, Database, Server, Cpu, Check, AlertCircle, RefreshCw } from 'lucide-svelte';
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();

  let bp = $derived(data.blueprint);
  let metrics = $derived(data.liveDatasetMetrics);

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

  <!-- Google Scholar Citation Meta Tags -->
  <meta name="citation_title" content="{data.jurisdiction} Parliamentary Data Mapping & Audit Profile" />
  <meta name="citation_publisher" content="Comparative Legislative Data Project" />
  <meta name="citation_technical_report_number" content="Phase 0 Audit Profile: {data.jurisdiction}" />
  <meta name="citation_language" content="en" />

  <!-- Structured Data (JSON-LD) -->
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
        <span class="badge badge-live">Option 3 Hybrid Blueprint</span>
        <span class="badge badge-direct">API & DB Probed</span>
        {#if metrics}
          <span class="badge badge-enriched">Phase 1 Live Ingested</span>
        {/if}
      </div>
      {#if bp}
        <span class="schema-version-badge">Schema v{bp.schema_version} &bull; Updated {bp.last_updated}</span>
      {/if}
    </div>

    <h1 class="audit-title">
      {bp ? bp.assembly.name : data.jurisdiction} Data Audit Blueprint
    </h1>
    <p class="audit-sub">
      Declarative field mappings, API endpoints, rate limits, Hansard disambiguation rules, and continuous drift health probe status.
    </p>

    <div class="audit-meta-grid">
      <div class="meta-item">
        <span class="meta-label">Location / Chamber</span>
        <span class="meta-value">{bp ? `${bp.assembly.location} (${bp.assembly.chamber_type})` : 'Phase 0 Audit'}</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Open License</span>
        <span class="meta-value">{bp ? bp.assembly.license_type : 'Open Parliament Licence v3.0 / OGL v3.0'}</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Target Cohort</span>
        <span class="meta-value">{bp ? bp.assembly.target_cohort : '2019–2024 BICD Cohort 1'}</span>
      </div>
    </div>
  </div>

  <!-- Live Ingested Dataset Stats Card (Vertical Slice Active) -->
  {#if metrics}
    <section class="blueprint-section">
      <div class="card live-metrics-card">
        <div class="live-metrics-header">
          <div class="title-with-icon">
            <Database size={22} color="#10b981" />
            <h3>Phase 1 Live Ingested Database Metrics (PostgreSQL Mirror)</h3>
          </div>
          <span class="live-status-badge">
            <span class="pulse-dot"></span> LIVE INGESTED
          </span>
        </div>

        <div class="metrics-grid">
          <div class="metric-box">
            <span class="metric-num text-accent">{metrics.total_bills_cohort}</span>
            <span class="metric-title">2019–2024 Total Bills Ingested</span>
          </div>
          <div class="metric-box">
            <span class="metric-num text-success">{metrics.enacted_acts}</span>
            <span class="metric-title">Enacted Acts (Stage 3 Passed)</span>
          </div>
          <div class="metric-box">
            <span class="metric-num text-warning">{metrics.pending_bills}</span>
            <span class="metric-title">In Progress / Defeated / Pending</span>
          </div>
          <div class="metric-box">
            <span class="metric-num text-purple">{metrics.provenance_hashes_count}</span>
            <span class="metric-title">SHA-256 Provenance Audit Hashes</span>
          </div>
        </div>

        <div class="live-metrics-footer">
          <span><RefreshCw size={14} /> Last Ingestion Sync: <strong>{metrics.last_ingestion_sync}</strong></span>
          <span>Cohort Boundary: <strong>{metrics.cohort_window}</strong></span>
        </div>
      </div>
    </section>
  {/if}

  <!-- Structured Declarative Blueprint Render -->
  {#if bp}
    <!-- Section 1: Endpoints & Rate Limits -->
    <section class="blueprint-section">
      <div class="section-title-row">
        <Server size={20} color="#38bdf8" />
        <h2>API Endpoints & Access Specifications</h2>
      </div>

      <div class="table-card card">
        <table class="data-table">
          <thead>
            <tr>
              <th>Endpoint Name</th>
              <th>Target URL</th>
              <th>Method</th>
              <th>Rate Limit</th>
              <th>Format</th>
            </tr>
          </thead>
          <tbody>
            {#each bp.endpoints as ep}
              <tr>
                <td class="font-bold">{ep.name}</td>
                <td><code class="url-code">{ep.url}</code></td>
                <td><span class="badge badge-direct">{ep.http_method}</span></td>
                <td>{ep.rate_limit_per_min ? `${ep.rate_limit_per_min} req/min` : 'Unspecified'}</td>
                <td><span class="badge badge-bicd">{ep.response_format}</span></td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </section>

    <!-- Section 2: Dual-Layer Field Mappings -->
    <section class="blueprint-section">
      <div class="section-title-row">
        <Layers size={20} color="#6366f1" />
        <h2>Dual-Layer Field Mappings & Provenance Matrix</h2>
      </div>

      <div class="table-card card">
        <table class="data-table">
          <thead>
            <tr>
              <th>Canonical Field</th>
              <th>Native Key Path</th>
              <th>Provenance Tier</th>
              <th>Confidence</th>
              <th>Notes / Transformation</th>
            </tr>
          </thead>
          <tbody>
            {#each bp.field_mappings as fm}
              <tr>
                <td class="font-mono font-bold text-accent">{fm.canonical_field}</td>
                <td class="font-mono">{fm.native_key}</td>
                <td>
                  {#if fm.provenance_tier === 'NATIVE_DIRECT'}
                    <span class="badge badge-direct">NATIVE_DIRECT</span>
                  {:else if fm.provenance_tier === 'ENRICHED_BY_PIPELINE'}
                    <span class="badge badge-enriched">ENRICHED</span>
                  {:else}
                    <span class="badge badge-pending">UNAVAILABLE_GAP</span>
                  {/if}
                </td>
                <td><span class="confidence-tag">{fm.derivation_confidence}</span></td>
                <td class="text-subtle">{fm.notes || '—'}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </section>

    <!-- Section 3: Hansard & Typology Tests Grid -->
    <div class="two-col-grid">
      <!-- Hansard Disambiguation -->
      <section class="blueprint-section">
        <div class="section-title-row">
          <FileText size={20} color="#10b981" />
          <h2>Hansard Resolution</h2>
        </div>
        <div class="card spec-box">
          <div class="spec-line"><span class="spec-label">Format:</span> <strong>{bp.hansard.transcript_format}</strong></div>
          <div class="spec-line"><span class="spec-label">Disambiguation:</span> <strong>{bp.hansard.speaker_disambiguation_method}</strong></div>
          <div class="spec-line"><span class="spec-label">Timestamp Granularity:</span> <strong>{bp.hansard.timestamp_granularity}</strong></div>
          <div class="spec-line"><span class="spec-label">Interruption Flags:</span> <strong>{bp.hansard.interruption_flags_available ? 'Available' : 'None'}</strong></div>
        </div>
      </section>

      <!-- Procedural Notes -->
      <section class="blueprint-section">
        <div class="section-title-row">
          <ShieldCheck size={20} color="#a855f7" />
          <h2>Procedural Rules</h2>
        </div>
        <div class="card spec-box">
          <ul class="notes-list">
            {#each bp.procedural_notes as note}
              <li><Check size={15} color="#10b981" /> {note}</li>
            {/each}
          </ul>
        </div>
      </section>
    </div>

    <!-- Section 4: Typology Test Cohorts -->
    <section class="blueprint-section">
      <div class="section-title-row">
        <Cpu size={20} color="#f59e0b" />
        <h2>5-Bill Typology Empirical Audit Tests</h2>
      </div>
      <div class="assembly-grid">
        {#each bp.typology_tests as test}
          <div class="card test-card">
            <div class="test-top">
              <span class="badge badge-bicd">{test.bill_id}</span>
              <span class="badge badge-live">{test.expected_stages_count} Stages</span>
            </div>
            <h3 class="test-title">{test.title}</h3>
            <p class="test-category">{test.typology_category}</p>
            <p class="test-notes">{test.notes || ''}</p>
          </div>
        {/each}
      </div>
    </section>

  {:else if data.content}
    <!-- Raw Markdown Audit Fallback -->
    <div class="card content-card prose">
      <pre class="raw-markdown">{data.content}</pre>
    </div>
  {:else}
    <!-- Placeholder Card -->
    <div class="card placeholder-card">
      <FileText size={48} color="#6366f1" />
      <h3>{data.jurisdiction} Audit Profile</h3>
      <p>{data.message}</p>
      <a href="/atlas" class="btn-secondary">Return to Atlas Directory</a>
    </div>
  {/if}
</div>

<style>
  .page-padding { padding: 3rem 1.5rem; }

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

  .badge-group { display: flex; gap: 0.5rem; flex-wrap: wrap; }
  .schema-version-badge { font-size: 0.8rem; color: var(--text-dim); }

  .audit-title { font-size: 2.25rem; margin-bottom: 0.5rem; }
  .audit-sub { color: var(--text-muted); font-size: 1.05rem; margin-bottom: 1.75rem; }

  .audit-meta-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.25rem;
    background: rgba(11, 15, 25, 0.6);
    border: 1px solid var(--border-subtle);
    border-radius: 0.75rem;
    padding: 1.25rem;
  }

  .meta-item { display: flex; flex-direction: column; gap: 0.25rem; }
  .meta-label { font-size: 0.75rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.05em; }
  .meta-value { font-size: 0.9rem; color: var(--text-main); font-weight: 500; }

  .live-metrics-card {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(17, 24, 39, 0.95) 100%);
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 1.5rem;
    margin-bottom: 2.5rem;
  }

  .live-metrics-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.25rem;
  }

  .title-with-icon { display: flex; align-items: center; gap: 0.65rem; }
  .title-with-icon h3 { font-size: 1.15rem; color: #ffffff; }

  .live-status-badge {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(16, 185, 129, 0.2);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.4);
    padding: 0.25rem 0.65rem;
    border-radius: 1rem;
    font-size: 0.75rem;
    font-weight: 700;
  }

  .pulse-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background-color: #10b981;
    box-shadow: 0 0 8px #10b981;
  }

  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.25rem;
  }

  .metric-box {
    background: rgba(11, 15, 25, 0.6);
    border: 1px solid var(--border-subtle);
    border-radius: 0.65rem;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 0.25rem;
  }

  .metric-num { font-size: 2rem; font-weight: 800; line-height: 1; }
  .metric-title { font-size: 0.775rem; color: var(--text-muted); font-weight: 500; }

  .text-success { color: #10b981; }
  .text-warning { color: #f59e0b; }
  .text-purple { color: #a855f7; }

  .live-metrics-footer {
    display: flex;
    justify-content: space-between;
    font-size: 0.825rem;
    color: var(--text-dim);
    border-top: 1px solid var(--border-subtle);
    padding-top: 0.85rem;
  }

  .blueprint-section { margin-bottom: 2.5rem; }

  .section-title-row {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin-bottom: 1rem;
  }
  .section-title-row h2 { font-size: 1.35rem; }

  .table-card { padding: 0; overflow-x: auto; }

  .data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
    text-align: left;
  }

  .data-table th, .data-table td {
    padding: 0.85rem 1.25rem;
    border-bottom: 1px solid var(--border-subtle);
  }

  .data-table th {
    background: #0d1117;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.04em;
  }

  .font-mono { font-family: monospace; }
  .font-bold { font-weight: 600; }
  .text-accent { color: var(--accent-cyan); }
  .text-subtle { color: var(--text-muted); font-size: 0.825rem; }
  .url-code { background: #0d1117; padding: 0.2rem 0.4rem; border-radius: 0.35rem; color: #38bdf8; font-size: 0.825rem; }
  .confidence-tag { background: rgba(16, 185, 129, 0.15); color: #10b981; padding: 0.15rem 0.5rem; border-radius: 0.35rem; font-size: 0.75rem; font-weight: 600; }

  .two-col-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
    margin-bottom: 2.5rem;
  }

  .spec-box { display: flex; flex-direction: column; gap: 0.85rem; padding: 1.25rem; }
  .spec-line { display: flex; justify-content: space-between; font-size: 0.875rem; border-bottom: 1px solid var(--border-subtle); padding-bottom: 0.5rem; }
  .spec-label { color: var(--text-muted); }

  .notes-list { list-style: none; display: flex; flex-direction: column; gap: 0.65rem; }
  .notes-list li { display: flex; align-items: flex-start; gap: 0.5rem; font-size: 0.875rem; color: var(--text-main); }

  .assembly-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.25rem;
  }

  .test-card { display: flex; flex-direction: column; gap: 0.5rem; }
  .test-top { display: flex; align-items: center; justify-content: space-between; }
  .test-title { font-size: 1.05rem; color: #ffffff; }
  .test-category { font-size: 0.8rem; color: var(--accent-cyan); font-weight: 500; }
  .test-notes { font-size: 0.825rem; color: var(--text-muted); }

  .content-card { padding: 2.5rem; }
  .raw-markdown { white-space: pre-wrap; font-family: var(--font-body); font-size: 0.95rem; line-height: 1.7; color: #e5e7eb; background: transparent; border: none; padding: 0; }
  .placeholder-card { text-align: center; padding: 4rem 2rem; display: flex; flex-direction: column; align-items: center; gap: 1rem; }

  @media (max-width: 1024px) {
    .audit-meta-grid, .two-col-grid, .assembly-grid, .metrics-grid { grid-template-columns: 1fr; }
  }
</style>
