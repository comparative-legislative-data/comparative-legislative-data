<script lang="ts">
  import { FileCode2, Download, Clock, Check } from 'lucide-svelte';

  const breadcrumbSchema = {
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
        'name': 'API & Bulk Data Access',
        'item': 'https://legislativedata.org/api-docs'
      }
    ]
  };

  const techArticleSchema = {
    '@context': 'https://schema.org',
    '@type': 'TechArticle',
    'name': 'Comparative Legislative Data API & Bulk Data Access Specification',
    'url': 'https://legislativedata.org/api-docs',
    'description': 'Technical access specifications for high-speed JSON REST APIs and bulk Parquet dataset downloads.',
    'publisher': {
      '@type': 'Organization',
      'name': 'Comparative Legislative Data Project'
    }
  };
</script>

<svelte:head>
  <title>API & Bulk Data Specification — Comparative Legislative Data Platform</title>
  <meta name="description" content="Technical access specifications for high-speed JSON REST APIs and bulk Parquet dataset downloads for political scientists and data researchers." />
  <meta name="keywords" content="legislative API docs, bulk parliamentary data, Parquet legislative dataset, REST API comparative politics" />

  <meta property="og:title" content="API & Bulk Data Specification — Comparative Legislative Data Platform" />
  <meta property="og:description" content="Technical access specifications for REST APIs and bulk Parquet dataset downloads." />

  <!-- Page Structured Data (JSON-LD) -->
  {@html `<script type="application/ld+json">${JSON.stringify(breadcrumbSchema)}</script>`}
  {@html `<script type="application/ld+json">${JSON.stringify(techArticleSchema)}</script>`}
</svelte:head>

<div class="container page-padding">
  <!-- Page Header -->
  <div class="page-header">
    <div class="header-badge">
      <span class="badge badge-pending">Coming Soon &bull; Phase 1 Launch</span>
      <span>API & Bulk Data Specification</span>
    </div>
    <h1 class="page-title">API & Bulk Dataset Access</h1>
    <p class="page-sub">
      We are currently in <strong>Phase 0 (Data Availability Audit & Mapping Mode)</strong>. Live REST API endpoints and bulk Parquet/CSV dataset downloads will launch in Phase 1 upon completion of the BICD group ingestion.
    </p>
  </div>

  <!-- Phase 0 Status Banner -->
  <div class="card status-banner-card">
    <div class="status-icon">
      <Clock size={28} color="#f59e0b" />
    </div>
    <div class="status-text">
      <h3>Current Project Phase: Phase 0 (Data Mapping & Audit Atlas)</h3>
      <p>
        The platform is currently auditing API structures, rate limits, data schemas, and 3-tier provenance for all 8 BICD assemblies. Once mapping blueprints are completed, Phase 1 will mirror 2019–2024 data and launch live API endpoints.
      </p>
    </div>
  </div>

  <!-- Planned Access Specifications -->
  <h2 class="section-heading">Planned Data Access Modes</h2>

  <div class="specs-grid">
    <div class="card spec-card">
      <div class="spec-top">
        <FileCode2 size={24} color="#6366f1" />
        <h3>REST API Queries</h3>
      </div>
      <p class="spec-desc">High-speed JSON responses serving dual-layer payloads (`normalized.*` and `native.*`).</p>
      <ul class="spec-list">
        <li><Check size={16} color="#10b981" /> Standard REST endpoints</li>
        <li><Check size={16} color="#10b981" /> Dual-layer schema payloads</li>
        <li><Check size={16} color="#10b981" /> Filtering by jurisdiction, term, & date</li>
      </ul>
    </div>

    <div class="card spec-card">
      <div class="spec-top">
        <Download size={24} color="#38bdf8" />
        <h3>Bulk Parquet & CSV Downloads</h3>
      </div>
      <p class="spec-desc">Full snapshot releases formatted for R, Python, and Stata statistical workflows.</p>
      <ul class="spec-list">
        <li><Check size={16} color="#10b981" /> Open Parquet data releases</li>
        <li><Check size={16} color="#10b981" /> Complete annual legislative archives</li>
        <li><Check size={16} color="#10b981" /> Permanent Zenodo DOI citations</li>
      </ul>
    </div>
  </div>
</div>

<style>
  .page-padding { padding: 3rem 1.5rem; }
  .page-header { text-align: center; max-width: 800px; margin: 0 auto 2.5rem; }
  .header-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    background: rgba(31, 41, 55, 0.6);
    border: 1px solid var(--border-subtle);
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
    margin-bottom: 1rem;
    font-size: 0.85rem;
    color: var(--text-muted);
  }
  .page-title { font-size: 2.75rem; margin-bottom: 0.75rem; }
  .page-sub { font-size: 1.05rem; color: var(--text-muted); }

  .status-banner-card {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(17, 24, 39, 0.95) 100%);
    border: 1px solid rgba(245, 158, 11, 0.3);
    padding: 1.75rem;
    margin-bottom: 3.5rem;
  }

  .status-text h3 { font-size: 1.25rem; color: #ffffff; margin-bottom: 0.35rem; }
  .status-text p { color: var(--text-muted); font-size: 0.9rem; }

  .section-heading { font-size: 1.5rem; margin-bottom: 1.5rem; }

  .specs-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.75rem;
  }

  .spec-card {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .spec-top {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .spec-top h3 { font-size: 1.25rem; color: #ffffff; }
  .spec-desc { font-size: 0.875rem; color: var(--text-muted); }

  .spec-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
    margin-top: 0.5rem;
  }

  .spec-list li {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    font-size: 0.85rem;
    color: var(--text-main);
  }

  @media (max-width: 768px) {
    .specs-grid { grid-template-columns: 1fr; }
    .status-banner-card { flex-direction: column; text-align: center; }
  }
</style>
