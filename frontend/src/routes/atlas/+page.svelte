<script lang="ts">
  import { Search, Globe, Filter, ExternalLink, CheckCircle, Clock, ArrowRight, Layers } from 'lucide-svelte';

  let searchQuery = $state('');
  let selectedFilter = $state('ALL');

  const parliamentList = [
    { code: 'GB-SCT', name: 'Scottish Parliament', location: 'Holyrood', region: 'BICD', access: 'REST API / JSON', provenance: 'NATIVE_DIRECT (v2.7.0)', status: 'ACTIVE_AUDIT', docs: '/atlas/GB-SCT', active: true },
    { code: 'GB-UKP', name: 'UK Parliament', location: 'Westminster', region: 'BICD', access: 'REST API', provenance: 'ENRICHED_BY_PIPELINE', status: 'PLANNED', docs: '/atlas/GB-UKP', active: false },
    { code: 'GB-WLS', name: 'Senedd Cymru', location: 'Cardiff', region: 'BICD', access: 'REST API', provenance: 'ENRICHED_BY_PIPELINE', status: 'PLANNED', docs: '/atlas/GB-WLS', active: false },
    { code: 'GB-NIR', name: 'Northern Ireland Assembly', location: 'Stormont', region: 'BICD', access: 'XML / HTML', provenance: 'ENRICHED_BY_PIPELINE', status: 'PLANNED', docs: '/atlas/GB-NIR', active: false },
    { code: 'IM-TYN', name: 'Isle of Man Tynwald', location: 'Douglas', region: 'BICD', access: 'HTML Portal', provenance: 'ENRICHED_BY_PIPELINE', status: 'PLANNED', docs: '/atlas/IM-TYN', active: false },
    { code: 'JE-STJ', name: 'States of Jersey', location: 'St Helier', region: 'BICD', access: 'HTML Portal', provenance: 'ENRICHED_BY_PIPELINE', status: 'PLANNED', docs: '/atlas/JE-STJ', active: false },
    { code: 'GG-STG', name: 'States of Guernsey', location: 'St Peter Port', region: 'BICD', access: 'HTML Portal', provenance: 'ENRICHED_BY_PIPELINE', status: 'PLANNED', docs: '/atlas/GG-STG', active: false },
    { code: 'GI-GIB', name: 'Gibraltar Parliament', location: 'Gibraltar', region: 'BICD', access: 'HTML / PDF', provenance: 'ENRICHED_BY_PIPELINE', status: 'PLANNED', docs: '/atlas/GI-GIB', active: false },
    { code: 'US-FED', name: 'US Congress', location: 'Washington D.C.', region: 'GLOBAL', access: 'REST API', provenance: 'NATIVE_DIRECT', status: 'PLANNED', docs: '/atlas/US-FED', active: false },
    { code: 'DE-BT', name: 'German Bundestag', location: 'Berlin', region: 'GLOBAL', access: 'DIP REST API', provenance: 'NATIVE_DIRECT', status: 'PLANNED', docs: '/atlas/DE-BT', active: false },
    { code: 'CA-PARL', name: 'Parliament of Canada', location: 'Ottawa', region: 'GLOBAL', access: 'XML / JSON', provenance: 'NATIVE_DIRECT', status: 'PLANNED', docs: '/atlas/CA-PARL', active: false },
    { code: 'AU-PARL', name: 'Parliament of Australia', location: 'Canberra', region: 'GLOBAL', access: 'XML / HTML', provenance: 'ENRICHED_BY_PIPELINE', status: 'PLANNED', docs: '/atlas/AU-PARL', active: false },
    { code: 'FR-AN', name: 'French National Assembly', location: 'Paris', region: 'GLOBAL', access: 'Open Data JSON', provenance: 'NATIVE_DIRECT', status: 'PLANNED', docs: '/atlas/FR-AN', active: false },
    { code: 'EU-EP', name: 'European Parliament', location: 'Brussels/Strasbourg', region: 'GLOBAL', access: 'EP Open Data API', provenance: 'NATIVE_DIRECT', status: 'PLANNED', docs: '/atlas/EU-EP', active: false }
  ];

  let filteredParliaments = $derived(
    parliamentList.filter(p => {
      const matchesSearch = p.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                            p.code.toLowerCase().includes(searchQuery.toLowerCase()) ||
                            p.location.toLowerCase().includes(searchQuery.toLowerCase());
      if (selectedFilter === 'ALL') return matchesSearch;
      if (selectedFilter === 'BICD') return matchesSearch && p.region === 'BICD';
      if (selectedFilter === 'GLOBAL') return matchesSearch && p.region === 'GLOBAL';
      return matchesSearch;
    })
  );

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
        'name': 'Data Atlas',
        'item': 'https://legislativedata.org/atlas'
      }
    ]
  };
</script>

<svelte:head>
  <title>Parliament Data Atlas — Comparative Legislative Data Platform</title>
  <meta name="description" content="Searchable atlas auditing API endpoints, data availability, rate limits, and structural schemas across 30+ international legislative assemblies." />
  <meta name="keywords" content="parliament data atlas, legislative API directory, UK Parliament data, Holyrood API, Senedd open data, parliamentary datasets" />

  <meta property="og:title" content="Parliament Data Atlas — Comparative Legislative Data Platform" />
  <meta property="og:description" content="Auditing API access, rate limits, data structures, and 3-tier provenance across international assemblies." />

  <!-- Breadcrumb Structured Data (JSON-LD) -->
  {@html `<script type="application/ld+json">${JSON.stringify(breadcrumbSchema)}</script>`}
</svelte:head>

<div class="container page-padding">
  <!-- Page Header -->
  <div class="page-header">
    <div class="header-badge">
      <span class="badge badge-direct">Scottish Parliament Audit Active</span>
      <span>Global Parliamentary Data Atlas</span>
    </div>
    <h1 class="page-title">Parliament Data Atlas</h1>
    <p class="page-sub">
      Auditing native open data API feeds, rate limits, data structures, and 6-tier provenance across international legislative assemblies.
    </p>
  </div>

  <!-- Search & Filter Bar -->
  <div class="card control-card">
    <div class="search-input-wrapper">
      <Search size={18} class="search-icon" />
      <input 
        type="text" 
        placeholder="Search assembly by name, code, or location (e.g. Scottish Parliament, GB-SCT, Holyrood)..." 
        bind:value={searchQuery}
        class="search-input"
      />
    </div>

    <div class="filter-buttons">
      <button 
        class="filter-btn {selectedFilter === 'ALL' ? 'active' : ''}" 
        onclick={() => selectedFilter = 'ALL'}
      >
        All Assemblies ({parliamentList.length})
      </button>
      <button 
        class="filter-btn {selectedFilter === 'BICD' ? 'active' : ''}" 
        onclick={() => selectedFilter = 'BICD'}
      >
        British-Irish Assemblies
      </button>
      <button 
        class="filter-btn {selectedFilter === 'GLOBAL' ? 'active' : ''}" 
        onclick={() => selectedFilter = 'GLOBAL'}
      >
        Global Assemblies
      </button>
    </div>
  </div>

  <!-- Parliaments Grid -->
  <div class="parliaments-grid">
    {#each filteredParliaments as p}
      <a href={p.docs} class="parliament-card card {p.active ? 'active-card' : 'muted-card'}">
        <div class="card-header">
          <div class="title-group">
            <span class="badge {p.active ? 'badge-direct' : 'badge-grey'}">{p.code}</span>
            <h3>{p.name}</h3>
          </div>
          {#if p.active}
            <span class="status-badge active-status"><span class="pulse-dot"></span> ACTIVE AUDIT</span>
          {:else}
            <span class="status-badge grey-status">PLANNED</span>
          {/if}
        </div>

        <div class="card-meta">
          <div class="meta-row">
            <span class="meta-label">Location / Chamber:</span>
            <span class="meta-val">{p.location}</span>
          </div>
          <div class="meta-row">
            <span class="meta-label">Native API Access:</span>
            <span class="meta-val">{p.access}</span>
          </div>
          <div class="meta-row">
            <span class="meta-label">Provenance Tier:</span>
            <span class="meta-val font-mono">{p.provenance}</span>
          </div>
        </div>

        <div class="card-footer">
          <span class="view-link">
            {#if p.active}
              View Institutional Blueprint <ArrowRight size={14} />
            {:else}
              View Assembly Profile <ArrowRight size={14} />
            {/if}
          </span>
        </div>
      </a>
    {/each}
  </div>
</div>

<style>
  .page-padding { padding-top: 2rem; padding-bottom: 5rem; }
  .page-header { margin-bottom: 2rem; }

  .header-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(99, 102, 241, 0.1);
    color: var(--accent-indigo);
    border: 1px solid rgba(99, 102, 241, 0.2);
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    margin-bottom: 1rem;
  }

  .badge-direct { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
  .badge-grey { background: rgba(255, 255, 255, 0.05); color: #64748b; border: 1px solid rgba(255, 255, 255, 0.1); }

  .page-title {
    font-family: var(--font-heading);
    font-size: 2.25rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.5rem;
  }

  .page-sub {
    font-size: 1.05rem;
    color: var(--text-muted);
    max-width: 48rem;
    line-height: 1.5;
  }

  .control-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: 0.75rem;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .search-input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
  }

  .search-input {
    width: 100%;
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid var(--border-subtle);
    border-radius: 0.5rem;
    padding: 0.75rem 1rem 0.75rem 2.75rem;
    color: #ffffff;
    font-size: 0.95rem;
    outline: none;
  }

  :global(.search-icon) {
    position: absolute;
    left: 0.85rem;
    color: var(--text-muted);
  }

  .filter-buttons {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .filter-btn {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border-subtle);
    color: var(--text-muted);
    font-size: 0.825rem;
    font-weight: 500;
    padding: 0.4rem 0.85rem;
    border-radius: 0.375rem;
    cursor: pointer;
  }
  .filter-btn.active {
    background: rgba(99, 102, 241, 0.15);
    border-color: var(--accent-indigo);
    color: #ffffff;
    font-weight: 600;
  }

  .parliaments-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.25rem;
  }

  .parliament-card {
    border-radius: 0.75rem;
    padding: 1.25rem;
    text-decoration: none;
    display: flex;
    flex-direction: column;
    transition: all 0.2s ease;
  }

  .active-card {
    background: rgba(15, 23, 42, 0.95);
    border: 2px solid rgba(34, 197, 94, 0.6);
    box-shadow: 0 0 20px rgba(34, 197, 94, 0.15);
  }
  .active-card:hover {
    transform: translateY(-3px);
    border-color: rgba(34, 197, 94, 0.9);
  }

  .muted-card {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    opacity: 0.65;
  }
  .muted-card:hover {
    opacity: 0.9;
    border-color: rgba(255, 255, 255, 0.2);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .title-group h3 {
    font-family: var(--font-heading);
    font-size: 1.15rem;
    font-weight: 700;
    color: #ffffff;
    margin-top: 0.35rem;
  }

  .active-status {
    background: rgba(34, 197, 94, 0.15);
    color: #4ade80;
    border: 1px solid rgba(34, 197, 94, 0.3);
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.2rem 0.5rem;
    border-radius: 9999px;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
  }

  .pulse-dot {
    width: 6px;
    height: 6px;
    background: #4ade80;
    border-radius: 50%;
    box-shadow: 0 0 8px #4ade80;
  }

  .grey-status {
    background: rgba(255, 255, 255, 0.05);
    color: #64748b;
    border: 1px solid rgba(255, 255, 255, 0.1);
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.2rem 0.5rem;
    border-radius: 9999px;
  }

  .card-meta {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    margin-bottom: 1rem;
  }

  .meta-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
  }

  .meta-label { color: var(--text-dim); }
  .meta-val { color: var(--text-main); font-weight: 500; }

  .card-footer {
    margin-top: auto;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
  }

  .view-link {
    font-size: 0.825rem;
    font-weight: 600;
    color: var(--accent-cyan);
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
  }
</style>
