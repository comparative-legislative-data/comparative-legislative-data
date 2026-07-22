<script lang="ts">
  import { Globe, Database, Cpu, ShieldCheck, ArrowRight, Layers, FileSpreadsheet, CheckCircle2, Clock } from 'lucide-svelte';

  const assemblies = [
    { code: 'GB-UKP', name: 'UK Parliament', location: 'Westminster', type: 'Sovereign Bicameral', status: 'In Audit', tier: 'Tier 1' },
    { code: 'GB-SCT', name: 'Scottish Parliament', location: 'Holyrood', type: 'Devolved Unicameral', status: 'In Audit', tier: 'Tier 1' },
    { code: 'GB-WLS', name: 'Senedd Cymru', location: 'Cardiff', type: 'Devolved Unicameral', status: 'Planned', tier: 'Tier 1' },
    { code: 'GB-NIR', name: 'Northern Ireland Assembly', location: 'Stormont', type: 'Devolved Assembly', status: 'Planned', tier: 'Tier 1' },
    { code: 'IM-TYN', name: 'Isle of Man Tynwald', location: 'Douglas', type: 'Crown Dependency Bicameral', status: 'Planned', tier: 'Tier 1' },
    { code: 'JE-STJ', name: 'States of Jersey', location: 'St Helier', type: 'Crown Dependency Consensus', status: 'Planned', tier: 'Tier 1' },
    { code: 'GG-STG', name: 'States of Guernsey', location: 'St Peter Port', type: 'Crown Dependency Consensus', status: 'Planned', tier: 'Tier 1' },
    { code: 'GI-GIB', name: 'Gibraltar Parliament', location: 'Gibraltar', type: 'Overseas Territory', status: 'Planned', tier: 'Tier 1' }
  ];

  const dataCatalogSchema = {
    '@context': 'https://schema.org',
    '@type': 'DataCatalog',
    'name': 'Global Parliamentary Data Audit & Mapping Atlas',
    'description': 'Comparative audit and data availability atlas mapping structural schemas, rate limits, and API endpoints across international legislative assemblies.',
    'url': 'https://legislativedata.org',
    'publisher': {
      '@type': 'Organization',
      'name': 'Comparative Legislative Data Project'
    },
    'dataset': assemblies.map(a => ({
      '@type': 'Dataset',
      'name': `${a.name} (${a.code}) Legislative Open Data Blueprint`,
      'url': `https://legislativedata.org/atlas/${a.code}`,
      'spatialCoverage': a.location
    }))
  };
</script>

<svelte:head>
  <title>Comparative Legislative Data Platform — Open Data Audit & Mapping Atlas</title>
  <meta name="description" content="Mapping data availability, API access endpoints, rate limits, and structural schemas across international legislatures to establish a clean, harmonised research foundation." />
  <meta name="keywords" content="legislative data, parliamentary API, comparative politics, open data atlas, UK Parliament schema, Senedd data, Holyrood data, legislative dataset" />
  
  <meta property="og:title" content="Comparative Legislative Data Platform — Open Data Audit & Mapping Atlas" />
  <meta property="og:description" content="Mapping data availability, API access, and structural schemas across international legislatures." />

  <!-- Page Structured Data (JSON-LD) -->
  {@html `<script type="application/ld+json">${JSON.stringify(dataCatalogSchema)}</script>`}
</svelte:head>

<!-- Hero Section -->
<section class="hero-section">
  <div class="container hero-content">
    <div class="hero-badge">
      <span class="badge badge-bicd">Phase 0 Status</span>
      <span class="hero-badge-text">Data Availability Audit & Mapping Atlas</span>
    </div>

    <h1 class="hero-title">
      Comparative Legislative Data <br />
      <span class="text-gradient">Open Audit & Mapping Atlas</span>
    </h1>

    <p class="hero-subtitle">
      Mapping data availability, API endpoints, rate limits, and structural schemas across international assemblies to establish a clean, harmonised foundation for legislative research.
    </p>

    <div class="hero-cta">
      <a href="/atlas" class="btn-primary btn-lg">
        <Globe size={18} /> Explore Data Atlas
      </a>
      <a href="/schema" class="btn-secondary btn-lg">
        <Layers size={18} /> View Canonical Schema
      </a>
    </div>

    <!-- Stats Bar -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-num">30+</div>
        <div class="stat-label">Parliaments Audited</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">8</div>
        <div class="stat-label">BICD Assemblies (Wave 1)</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">Phase 0</div>
        <div class="stat-label">Current Project Phase</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">Open</div>
        <div class="stat-label">Academic Access</div>
      </div>
    </div>
  </div>
</section>

<!-- Methodological Core -->
<section class="section">
  <div class="container">
    <div class="section-header">
      <h2 class="section-title">Project Approach & Core Architecture</h2>
      <p class="section-sub">Establishing a transparent, citable foundation for legislative data.</p>
    </div>

    <div class="pillars-grid">
      <div class="card pillar-card">
        <div class="pillar-icon">
          <Layers size={24} color="#6366f1" />
        </div>
        <h3>Dual-Layer Schema</h3>
        <p>
          Separates <code>normalized.*</code> comparative fields (for cross-national statistical analysis) from <code>native.*</code> raw detail (for single-country specialists).
        </p>
      </div>

      <div class="card pillar-card">
        <div class="pillar-icon">
          <ShieldCheck size={24} color="#38bdf8" />
        </div>
        <h3>3-Tier Data Provenance</h3>
        <p>
          Classifies every field as <code>NATIVE_DIRECT</code>, <code>ENRICHED_BY_PIPELINE</code>, or <code>UNAVAILABLE_GAP</code> to maintain complete academic transparency.
        </p>
      </div>

      <div class="card pillar-card">
        <div class="pillar-icon">
          <Cpu size={24} color="#10b981" />
        </div>
        <h3>Atomic Building Blocks</h3>
        <p>
          Focuses on generating clean, raw variables (sitting days, termination mechanisms, division counts) so researchers construct custom indices.
        </p>
      </div>

      <div class="card pillar-card">
        <div class="pillar-icon">
          <Database size={24} color="#a855f7" />
        </div>
        <h3>BICD-First Phasing</h3>
        <p>
          Beginning with the 8 British Isles & Crown Dependency assemblies before expanding sequentially to global parliaments.
        </p>
      </div>
    </div>
  </div>
</section>

<!-- BICD Cohort 1 Grid -->
<section class="section bg-card-section">
  <div class="container">
    <div class="section-header flex-header">
      <div>
        <h2 class="section-title">Wave 1 Focus: British Isles & Crown Dependencies</h2>
        <p class="section-sub">Auditing data availability across 8 assemblies in the BICD region.</p>
      </div>
      <a href="/atlas" class="btn-secondary">View All Audits <ArrowRight size={15} /></a>
    </div>

    <div class="assembly-grid">
      {#each assemblies as item}
        <a href="/atlas/{item.code}" class="card assembly-card">
          <div class="assembly-top">
            <span class="badge badge-bicd">{item.code}</span>
            {#if item.status === 'In Audit'}
              <span class="badge badge-live">{item.status}</span>
            {:else}
              <span class="badge badge-pending">{item.status}</span>
            {/if}
          </div>
          <h3 class="assembly-name">{item.name}</h3>
          <p class="assembly-location">{item.location} &bull; {item.type}</p>
          <div class="assembly-footer">
            <span class="tier-label">{item.tier} Mapping</span>
            <span class="view-link">View Blueprint &rarr;</span>
          </div>
        </a>
      {/each}
    </div>
  </div>
</section>

<style>
  .hero-section {
    padding: 4rem 0 3.5rem;
    text-align: center;
    position: relative;
  }

  .hero-content {
    max-width: 850px;
  }

  .hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.65rem;
    background: rgba(31, 41, 55, 0.6);
    border: 1px solid var(--border-subtle);
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
    margin-bottom: 1.25rem;
  }

  .hero-badge-text {
    font-size: 0.825rem;
    color: var(--text-muted);
    font-weight: 500;
  }

  .hero-title {
    font-size: 3rem;
    line-height: 1.15;
    margin-bottom: 1.25rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
    color: var(--text-muted);
    max-width: 720px;
    margin: 0 auto 2rem;
  }

  .hero-cta {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 3rem;
  }

  .btn-lg {
    padding: 0.85rem 1.6rem;
    font-size: 0.95rem;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.25rem;
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: 1rem;
    padding: 1.25rem;
  }

  .stat-card {
    text-align: center;
  }

  .stat-num {
    font-family: var(--font-heading);
    font-size: 1.75rem;
    font-weight: 700;
    color: #ffffff;
  }

  .stat-label {
    font-size: 0.775rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-top: 0.2rem;
  }

  .section {
    padding: 3.5rem 0;
  }

  .bg-card-section {
    background: rgba(17, 24, 39, 0.4);
    border-top: 1px solid var(--border-subtle);
    border-bottom: 1px solid var(--border-subtle);
  }

  .section-header {
    text-align: center;
    margin-bottom: 2.5rem;
  }

  .flex-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    text-align: left;
  }

  .section-title {
    font-size: 1.85rem;
    margin-bottom: 0.35rem;
  }

  .section-sub {
    color: var(--text-muted);
    font-size: 0.95rem;
  }

  .pillars-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.25rem;
  }

  .pillar-card {
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
  }

  .pillar-card h3 {
    font-size: 1.05rem;
  }

  .pillar-card p {
    font-size: 0.85rem;
    color: var(--text-muted);
  }

  .assembly-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.25rem;
  }

  .assembly-card {
    text-decoration: none;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 150px;
  }

  .assembly-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .assembly-name {
    font-size: 1.05rem;
    color: #ffffff;
    margin-top: 0.65rem;
  }

  .assembly-location {
    font-size: 0.775rem;
    color: var(--text-muted);
    margin-bottom: 0.85rem;
  }

  .assembly-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-top: 1px solid var(--border-subtle);
    padding-top: 0.65rem;
    font-size: 0.75rem;
  }

  .tier-label {
    color: var(--text-dim);
  }

  .view-link {
    color: var(--accent-cyan);
    font-weight: 600;
  }

  @media (max-width: 1024px) {
    .stats-grid, .pillars-grid, .assembly-grid { grid-template-columns: repeat(2, 1fr); }
  }

  @media (max-width: 640px) {
    .hero-title { font-size: 2.25rem; }
    .stats-grid, .pillars-grid, .assembly-grid { grid-template-columns: 1fr; }
    .flex-header { flex-direction: column; align-items: flex-start; gap: 1rem; }
  }
</style>
