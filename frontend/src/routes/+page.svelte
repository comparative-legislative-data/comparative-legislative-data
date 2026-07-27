<script lang="ts">
  import { Globe, Database, BookOpen, ShieldCheck, ArrowRight, Layers, FileCode2, CheckCircle2, Mail, Sparkles, AlertTriangle, Code2 } from 'lucide-svelte';

  const assemblies = [
    { code: 'GB-SCT', name: 'Scottish Parliament', location: 'Holyrood', type: 'Devolved Unicameral', status: 'Active Audit (v2.8.0 Baseline)', tier: 'Layer A Audit' },
    { code: 'GB-UKP', name: 'UK Parliament', location: 'Westminster', type: 'Sovereign Bicameral', status: 'Planned', tier: 'Phase 0' },
    { code: 'GB-WLS', name: 'Senedd Cymru', location: 'Cardiff', type: 'Devolved Unicameral', status: 'Planned', tier: 'Phase 0' },
    { code: 'GB-NIR', name: 'Northern Ireland Assembly', location: 'Stormont', type: 'Devolved Assembly', status: 'Planned', tier: 'Phase 0' },
    { code: 'IM-TYN', name: 'Isle of Man Tynwald', location: 'Douglas', type: 'Crown Dependency Bicameral', status: 'Planned', tier: 'Phase 0' },
    { code: 'JE-STJ', name: 'States of Jersey', location: 'St Helier', type: 'Crown Dependency Consensus', status: 'Planned', tier: 'Phase 0' },
    { code: 'GG-STG', name: 'States of Guernsey', location: 'St Peter Port', type: 'Crown Dependency Consensus', status: 'Planned', tier: 'Phase 0' },
    { code: 'GI-GIB', name: 'Gibraltar Parliament', location: 'Gibraltar', type: 'Overseas Territory', status: 'Planned', tier: 'Phase 0' }
  ];

  const dataCatalogSchema = {
    '@context': 'https://schema.org',
    '@type': 'DataCatalog',
    'name': 'Global Parliamentary Data Audit & Mapping Atlas',
    'description': 'Comparative academic research engine mapping data availability, API endpoints, rate limits, and 7-tier provenance schemas across international assemblies.',
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
  <title>Comparative Legislative Data Platform — Open Research Engine & Mapping Atlas</title>
  <meta name="description" content="Open academic research engine mapping data availability, API access endpoints, and 7-tier provenance schemas across international legislatures." />
  
  <meta property="og:title" content="Comparative Legislative Data Platform — Open Research Engine" />
  <meta property="og:description" content="Standardising, auditing, and mapping quantitative legislative data across international parliamentary and presidential assemblies." />

  <!-- Page Structured Data (JSON-LD) -->
  {@html `<script type="application/ld+json">${JSON.stringify(dataCatalogSchema)}</script>`}
</svelte:head>

<!-- Hero Section -->
<section class="hero-section">
  <div class="container hero-content">
    <div class="hero-badge">
      <span class="badge badge-bicd">Pilot Rebuild Underway</span>
      <span class="hero-badge-text">Enforcing Zero-Trust Deterministic Data Extraction</span>
    </div>

    <h1 class="hero-title">
      Comparative Legislative Data <br />
      <span class="text-gradient">Research Infrastructure & Mapping Atlas</span>
    </h1>

    <p class="hero-subtitle">
      Standardising, mirroring, and auditing quantitative legislative data across international parliamentary and presidential assemblies. 
      Built around a <strong>Dual-Layer Data Architecture</strong> and multi-entity decision tracking.
    </p>

    <div class="hero-cta">
      <div class="alert-box">
        <AlertTriangle size={20} color="#facc15" />
        <span><strong>Pilot Rebuild in Progress:</strong> The Scottish Parliament data pilot is currently being rebuilt to enforce strict mathematically provable deterministic data extraction. All frontend data views are temporarily disabled.</span>
      </div>
    </div>


  </div>
</section>

<!-- Rest of page content removed during purge -->

<style>
  .hero-section {
    padding: 5rem 0 4rem;
    background: radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.15), transparent 70%);
    text-align: center;
  }

  .hero-content {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.25);
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
    margin-bottom: 1.5rem;
  }

  .badge-bicd {
    background: var(--accent-indigo);
    color: #ffffff;
    font-weight: 700;
    font-size: 0.725rem;
    padding: 0.15rem 0.5rem;
    border-radius: 9999px;
    text-transform: uppercase;
  }

  .hero-badge-text {
    font-size: 0.825rem;
    color: var(--accent-cyan);
    font-weight: 600;
  }

  .hero-title {
    font-family: var(--font-heading);
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.15;
    color: #ffffff;
    margin-bottom: 1.25rem;
  }

  .text-gradient {
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .hero-subtitle {
    font-size: 1.15rem;
    color: var(--text-muted);
    max-width: 46rem;
    line-height: 1.6;
    margin-bottom: 2rem;
  }

  .hero-cta {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
    margin-bottom: 3.5rem;
  }

  .btn-lg {
    padding: 0.85rem 1.5rem;
    font-size: 0.95rem;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1.25rem;
    width: 100%;
    max-width: 56rem;
  }

  .stat-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: 0.75rem;
    padding: 1.25rem;
    text-align: center;
  }

  .stat-num {
    font-family: var(--font-heading);
    font-size: 2rem;
    font-weight: 800;
    color: var(--accent-cyan);
  }

  .stat-label {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: 0.25rem;
    font-weight: 500;
  }

  .section { padding: 4.5rem 0; }
  .section-dark { background: rgba(15, 23, 42, 0.6); border-top: 1px solid var(--border-subtle); border-bottom: 1px solid var(--border-subtle); }

  .section-header {
    text-align: center;
    max-width: 44rem;
    margin: 0 auto 3rem;
  }

  .section-title {
    font-family: var(--font-heading);
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.75rem;
  }

  .section-sub {
    font-size: 1rem;
    color: var(--text-muted);
    line-height: 1.5;
  }

  .layers-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
    gap: 1.5rem;
  }

  .layer-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: 0.85rem;
    padding: 2rem;
    position: relative;
  }

  .layer-native { border-top: 4px solid #22c55e; }
  .layer-canonical { border-top: 4px solid #38bdf8; }

  .layer-badge {
    position: absolute;
    top: 1.25rem;
    right: 1.25rem;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.25rem 0.6rem;
    border-radius: 0.25rem;
    background: rgba(255, 255, 255, 0.05);
    color: var(--text-dim);
  }

  .layer-card h3 {
    font-family: var(--font-heading);
    font-size: 1.25rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.75rem;
  }

  .layer-desc {
    font-size: 0.9rem;
    color: var(--text-muted);
    line-height: 1.55;
    margin-bottom: 1.25rem;
  }

  .layer-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
  }

  .layer-list li {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    color: var(--text-main);
  }

  .typology-display {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 1.25rem;
  }

  .typology-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: 0.75rem;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .tier-indicator {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    padding: 0.15rem 0.45rem;
    border-radius: 0.25rem;
    align-self: flex-start;
  }

  .tier-1 { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
  .tier-2 { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
  .tier-3 { background: rgba(45, 212, 191, 0.15); color: #2dd4bf; border: 1px solid rgba(45, 212, 191, 0.3); }
  .tier-4 { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
  .tier-5 { background: rgba(251, 191, 36, 0.15); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3); }
  .tier-6 { background: rgba(96, 165, 250, 0.15); color: #60a5fa; border: 1px solid rgba(96, 165, 250, 0.3); }
  .tier-7 { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }

  .typology-card h3 {
    font-family: var(--font-mono);
    font-size: 0.95rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
  }

  .typology-card p {
    font-size: 0.825rem;
    color: var(--text-muted);
    line-height: 1.45;
    margin: 0;
  }

  .callout-box {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.12), rgba(56, 189, 248, 0.08));
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 1rem;
    padding: 2.5rem;
    max-width: 50rem;
    margin: 0 auto;
    text-align: center;
  }

  .callout-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.775rem;
    font-weight: 600;
    color: var(--accent-cyan);
    background: rgba(56, 189, 248, 0.1);
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    margin-bottom: 1rem;
  }

  .callout-box h2 {
    font-family: var(--font-heading);
    font-size: 1.75rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.75rem;
  }

  .callout-box p {
    font-size: 0.95rem;
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 1.75rem;
  }

  .callout-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
  }
</style>
