<script lang="ts">
  import { ArrowLeft, CheckCircle2, FileText, Globe, Layers, ShieldCheck, Database, Server, Mail, MessageSquare, Tag, AlertCircle, Info } from 'lucide-svelte';
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();

  let bp = $derived(data.blueprint);
  let jurisdiction = $derived(data.jurisdiction);

  let datasetSchema = $derived({
    '@context': 'https://schema.org',
    '@type': 'Dataset',
    'name': `${jurisdiction} Parliamentary Open Data Audit & Mapping Blueprint`,
    'description': `Field-by-field provenance matrix, API access endpoints, and institutional variable schema for ${jurisdiction}.`,
    'url': `https://legislativedata.org/atlas/${jurisdiction}`,
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
        'name': jurisdiction,
        'item': `https://legislativedata.org/atlas/${jurisdiction}`
      }
    ]
  });

  // Extract all institutional variables from blueprint entities (Svelte 5 $derived.by)
  let allVariables = $derived.by(() => {
    if (!bp) return [];
    const bills = (bp.bill_entity_variables || []).map((v: any) => ({ ...v, entity: 'CanonicalBill (Macro Level)' }));
    const amendments = (bp.amendment_entity_variables || []).map((v: any) => ({ ...v, entity: 'CanonicalAmendment (Micro Level)' }));
    const committees = (bp.committee_entity_variables || []).map((v: any) => ({ ...v, entity: 'CommitteeContext (Roster Engine)' }));
    const proceedings = (bp.proceedings_variables || []).map((v: any) => ({ ...v, entity: 'ParsedProceedings (Hansard Text)' }));
    const gaps = (bp.procedural_hard_gaps || []).map((v: any) => ({ ...v, entity: 'Procedural Hard Gaps' }));
    return [...bills, ...amendments, ...committees, ...proceedings, ...gaps];
  });
</script>

<svelte:head>
  <title>{jurisdiction} Assembly Data Audit — Global Parliamentary Data Atlas</title>
  <meta name="description" content="Field-by-field provenance matrix, native open data endpoints, and institutional variable schema for {jurisdiction}." />
  <meta property="og:title" content="{jurisdiction} Assembly Data Audit — Global Parliamentary Data Atlas" />

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
        <span class="badge badge-bicd">{jurisdiction}</span>
        <span class="badge badge-live">Dual-Layer v2.8.0 Baseline</span>
        <span class="badge badge-pending">Formal Audit Pending</span>
      </div>
      {#if bp}
        <span class="schema-version-badge">{bp.assembly_metadata?.name || jurisdiction} &bull; {bp.assembly_metadata?.chamber_type}</span>
      {/if}
    </div>

    <h1 class="audit-title">
      {bp?.assembly_metadata?.name || jurisdiction} Data Audit Blueprint
    </h1>
    <p class="audit-sub">
      Declarative field mappings, native open data API endpoints, 7-tier provenance matrix, and institutional variable definitions.
    </p>

    {#if bp?.assembly_metadata}
      <div class="audit-meta-grid">
        <div class="meta-item">
          <span class="meta-label">Location / Chamber</span>
          <span class="meta-value">{bp.assembly_metadata.location} ({bp.assembly_metadata.chamber_type})</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Statutory Seats</span>
          <span class="meta-value">{bp.assembly_metadata.statutory_seats_total} Seats ({bp.assembly_metadata.presiding_officer_neutral_count} Neutral PO)</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Audited Term</span>
          <span class="meta-value">{bp.audited_terms?.[0]?.name} ({bp.audited_terms?.[0]?.date_start} to {bp.audited_terms?.[0]?.date_end})</span>
        </div>
      </div>
    {/if}
  </div>

  <!-- Section 1: Native Data Sources & API Endpoints -->
  {#if bp?.native_data_sources}
    <section class="blueprint-section mt-8">
      <div class="section-title-row">
        <Server size={20} color="#38bdf8" />
        <h2>Official Native Data Sources & Open API Endpoints</h2>
      </div>

      <div class="table-card card">
        <table class="data-table">
          <thead>
            <tr>
              <th>Source Name</th>
              <th>Target API Endpoint URL</th>
              <th>Format</th>
              <th>Provenance Tier</th>
            </tr>
          </thead>
          <tbody>
            {#each bp.native_data_sources as ds}
              <tr>
                <td class="font-bold">{ds.name}</td>
                <td><code class="url-code">{ds.url}</code></td>
                <td><span class="badge badge-bicd">{ds.format}</span></td>
                <td>
                  <span class="badge badge-pending">{ds.provenance_tier}</span>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </section>
  {/if}

  <!-- Section 2: Assembly-Specific Institutional Variable Audit Catalog (Layer A) -->
  {#if bp}
    <section class="blueprint-section mt-10">
      <div class="section-title-row">
        <Layers size={20} color="#6366f1" />
        <h2>{bp.assembly_metadata?.name || jurisdiction} Institutional Variable Audit Catalog (Layer A)</h2>
      </div>

      <p class="text-muted mb-6">
        The high-resolution native variables defined for {bp.assembly_metadata?.name || jurisdiction} (total: <strong>{allVariables.length}</strong> variables). 
        All variables are set to <strong>NOT_YET_CATEGORISED</strong> pending the upcoming formal empirical audit.
      </p>

      <div class="variables-grid">
        {#each allVariables as varDef}
          <div class="var-card">
            <div class="var-header">
              <code class="var-name">{varDef.key}</code>
              <span 
                class="badge tier-badge" 
                class:tier-direct={varDef.provenance_tier === 'NATIVE_DIRECT'} 
                class:tier-derived={varDef.provenance_tier === 'DERIVED_DETERMINISTIC'} 
                class:tier-extracted={varDef.provenance_tier === 'DERIVED_EXTRACTED'} 
                class:tier-human={varDef.provenance_tier === 'DERIVED_HUMAN_CODED'} 
                class:tier-ai={varDef.provenance_tier === 'DERIVED_SYNTHETIC_AI'} 
                class:tier-gap={varDef.provenance_tier === 'UNAVAILABLE_HARD_GAP'} 
                class:tier-uncategorised={varDef.provenance_tier === 'NOT_YET_CATEGORISED'}
              >
                {varDef.provenance_tier}
              </span>
            </div>

            <div class="var-title">{varDef.name || varDef.key}</div>
            <div class="var-entity">{varDef.entity} &bull; <span class="var-category">{varDef.scientific_category}</span></div>
            
            <p class="var-desc">{varDef.description || 'Native assembly field mapped to canonical schema.'}</p>

            {#if varDef.allowed_values}
              <div class="allowed-values-box">
                <span class="box-label">Allowed Choice Values:</span>
                <div class="values-list">
                  {#each varDef.allowed_values as val}
                    <span class="val-tag">{val}</span>
                  {/each}
                </div>
              </div>
            {/if}

            <div class="mapping-line">
              <span class="map-label">Canonical Mapping:</span>
              <code class="map-code">{varDef.canonical_mapping || 'Unmapped'}</code>
            </div>

            <!-- Per-Variable Action Buttons for Country Experts -->
            <div class="var-actions">
              <a 
                href={`https://github.com/comparative-legislative-data/comparative-legislative-data/discussions/new?category=general&title=Feedback+on+${jurisdiction}+variable+${varDef.key}`} 
                target="_blank" 
                rel="noopener noreferrer" 
                class="action-btn btn-github"
              >
                <MessageSquare size={13} /> Discuss on GitHub
              </a>
              <a 
                href={`mailto:comparativelegislativedata@gmail.com?subject=Feedback on ${jurisdiction} Variable: ${varDef.key}`} 
                class="action-btn btn-email"
              >
                <Mail size={13} /> Email Feedback
              </a>
            </div>
          </div>
        {/each}
      </div>
    </section>
  {/if}
</div>

<style>
  .page-padding { padding-top: 2rem; padding-bottom: 5rem; }
  .mt-8 { margin-top: 2rem; }
  .mt-10 { margin-top: 2.5rem; }
  .mb-6 { margin-bottom: 1.5rem; }
  .text-muted { color: var(--text-muted); font-size: 0.95rem; }

  .back-link {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    color: var(--accent-cyan);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
  }
  .back-link:hover { text-decoration: underline; }

  .header-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: 0.75rem;
    padding: 1.75rem;
  }

  .header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .badge-group {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .badge-bicd { background: rgba(99, 102, 241, 0.15); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.3); }
  .badge-live { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
  .badge-pending { background: rgba(148, 163, 184, 0.15); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.3); }

  .schema-version-badge {
    font-size: 0.8rem;
    color: var(--text-muted);
  }

  .audit-title {
    font-family: var(--font-heading);
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.5rem;
  }

  .audit-sub {
    font-size: 1rem;
    color: var(--text-muted);
    line-height: 1.5;
    margin-bottom: 1.25rem;
  }

  .audit-meta-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border-subtle);
  }

  .meta-item {
    display: flex;
    flex-direction: column;
  }

  .meta-label {
    font-size: 0.75rem;
    color: var(--text-dim);
    text-transform: uppercase;
  }

  .meta-value {
    font-size: 0.9rem;
    font-weight: 600;
    color: #ffffff;
    margin-top: 0.15rem;
  }

  .section-title-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .section-title-row h2 {
    font-family: var(--font-heading);
    font-size: 1.35rem;
    font-weight: 700;
    color: #ffffff;
  }

  .data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
  }

  .data-table th, .data-table td {
    padding: 0.75rem 1rem;
    text-align: left;
    border-bottom: 1px solid var(--border-subtle);
  }

  .data-table th {
    background: rgba(15, 23, 42, 0.8);
    color: var(--text-muted);
    font-weight: 600;
    font-size: 0.775rem;
    text-transform: uppercase;
  }

  .url-code {
    font-family: var(--font-mono);
    font-size: 0.8rem;
    color: var(--accent-cyan);
    word-break: break-all;
  }

  .variables-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 1.25rem;
  }

  .var-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: 0.65rem;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
  }

  .var-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.4rem;
  }

  .var-name {
    font-family: var(--font-mono);
    font-size: 0.875rem;
    font-weight: 700;
    color: var(--accent-cyan);
    background: rgba(56, 189, 248, 0.1);
    padding: 0.15rem 0.4rem;
    border-radius: 0.25rem;
    word-break: break-all;
  }

  .tier-badge {
    font-size: 0.675rem;
    font-weight: 700;
    padding: 0.15rem 0.45rem;
    border-radius: 0.25rem;
  }
  .tier-direct { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
  .tier-derived { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
  .tier-extracted { background: rgba(45, 212, 191, 0.15); color: #2dd4bf; border: 1px solid rgba(45, 212, 191, 0.3); }
  .tier-human { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
  .tier-ai { background: rgba(251, 191, 36, 0.15); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3); }
  .tier-gap { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
  .tier-uncategorised { background: rgba(148, 163, 184, 0.15); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.3); }

  .var-title {
    font-family: var(--font-heading);
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.2rem;
  }

  .var-entity {
    font-size: 0.75rem;
    color: var(--accent-purple);
    font-weight: 600;
    margin-bottom: 0.5rem;
  }

  .var-category {
    color: var(--accent-gold);
  }

  .var-desc {
    font-size: 0.85rem;
    color: var(--text-muted);
    line-height: 1.45;
    margin-bottom: 0.75rem;
  }

  .allowed-values-box {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid var(--border-subtle);
    border-radius: 0.375rem;
    padding: 0.5rem;
    margin-bottom: 0.75rem;
  }

  .box-label {
    display: block;
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--text-dim);
    text-transform: uppercase;
    margin-bottom: 0.35rem;
  }

  .values-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.25rem;
  }

  .val-tag {
    font-family: var(--font-mono);
    font-size: 0.675rem;
    background: rgba(255, 255, 255, 0.05);
    color: var(--text-main);
    padding: 0.1rem 0.35rem;
    border-radius: 0.2rem;
  }

  .mapping-line {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
  }

  .map-label { font-weight: 600; }
  .map-code { font-family: var(--font-mono); color: var(--accent-indigo); }

  .var-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: auto;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
  }

  .action-btn {
    flex: 1;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.35rem;
    font-size: 0.725rem;
    font-weight: 600;
    padding: 0.35rem 0.45rem;
    border-radius: 0.375rem;
    text-decoration: none;
    transition: all 0.2s ease;
  }

  .btn-github {
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #818cf8;
  }
  .btn-github:hover {
    background: rgba(99, 102, 241, 0.2);
    color: #ffffff;
  }

  .btn-email {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid var(--border-subtle);
    color: var(--text-muted);
  }
  .btn-email:hover {
    background: rgba(255, 255, 255, 0.08);
    color: var(--text-main);
  }
</style>
