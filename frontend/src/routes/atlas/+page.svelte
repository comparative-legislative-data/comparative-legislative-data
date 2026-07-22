<script lang="ts">
  import { Search, Globe, Filter, ExternalLink, CheckCircle, Clock, ArrowRight } from 'lucide-svelte';

  let searchQuery = $state('');
  let selectedFilter = $state('ALL');

  const parliamentList = [
    { code: 'GB-UKP', name: 'UK Parliament', location: 'Westminster', region: 'BICD', access: 'REST API', provenance: 'ENRICHED_BY_PIPELINE', status: 'IN_AUDIT', docs: '/atlas/GB-UKP' },
    { code: 'GB-SCT', name: 'Scottish Parliament', location: 'Holyrood', region: 'BICD', access: 'REST API / XML', provenance: 'ENRICHED_BY_PIPELINE', status: 'IN_AUDIT', docs: '/atlas/GB-SCT' },
    { code: 'GB-WLS', name: 'Senedd Cymru', location: 'Cardiff', region: 'BICD', access: 'REST API', provenance: 'ENRICHED_BY_PIPELINE', status: 'PLANNED', docs: '/atlas/GB-WLS' },
    { code: 'GB-NIR', name: 'Northern Ireland Assembly', location: 'Stormont', region: 'BICD', access: 'XML / HTML', provenance: 'ENRICHED_BY_PIPELINE', status: 'PLANNED', docs: '/atlas/GB-NIR' },
    { code: 'IM-TYN', name: 'Isle of Man Tynwald', location: 'Douglas', region: 'BICD', access: 'HTML Portal', provenance: 'ENRICHED_BY_PIPELINE', status: 'PLANNED', docs: '/atlas/IM-TYN' },
    { code: 'JE-STJ', name: 'States of Jersey', location: 'St Helier', region: 'BICD', access: 'HTML Portal', provenance: 'ENRICHED_BY_PIPELINE', status: 'PLANNED', docs: '/atlas/JE-STJ' },
    { code: 'GG-STG', name: 'States of Guernsey', location: 'St Peter Port', region: 'BICD', access: 'HTML Portal', provenance: 'ENRICHED_BY_PIPELINE', status: 'PLANNED', docs: '/atlas/GG-STG' },
    { code: 'GI-GIB', name: 'Gibraltar Parliament', location: 'Gibraltar', region: 'BICD', access: 'HTML / PDF', provenance: 'ENRICHED_BY_PIPELINE', status: 'PLANNED', docs: '/atlas/GI-GIB' },
    { code: 'US-FED', name: 'US Congress', location: 'Washington D.C.', region: 'GLOBAL', access: 'REST API', provenance: 'NATIVE_DIRECT', status: 'PLANNED', docs: '/atlas/US-FED' },
    { code: 'DE-BT', name: 'German Bundestag', location: 'Berlin', region: 'GLOBAL', access: 'DIP REST API', provenance: 'NATIVE_DIRECT', status: 'PLANNED', docs: '/atlas/DE-BT' },
    { code: 'CA-PARL', name: 'Parliament of Canada', location: 'Ottawa', region: 'GLOBAL', access: 'XML / JSON', provenance: 'NATIVE_DIRECT', status: 'PLANNED', docs: '/atlas/CA-PARL' },
    { code: 'AU-PARL', name: 'Parliament of Australia', location: 'Canberra', region: 'GLOBAL', access: 'XML / HTML', provenance: 'ENRICHED_BY_PIPELINE', status: 'PLANNED', docs: '/atlas/AU-PARL' },
    { code: 'FR-AN', name: 'French National Assembly', location: 'Paris', region: 'GLOBAL', access: 'Open Data JSON', provenance: 'NATIVE_DIRECT', status: 'PLANNED', docs: '/atlas/FR-AN' },
    { code: 'EU-EP', name: 'European Parliament', location: 'Brussels/Strasbourg', region: 'GLOBAL', access: 'EP Open Data API', provenance: 'NATIVE_DIRECT', status: 'PLANNED', docs: '/atlas/EU-EP' }
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
      <span class="badge badge-bicd">Phase 0 Status</span>
      <span>Data Availability & API Mapping Atlas</span>
    </div>
    <h1 class="page-title">Parliament Data Atlas</h1>
    <p class="page-sub">
      Auditing API access, rate limits, data structures, and 3-tier provenance across international assemblies.
    </p>
  </div>

  <!-- Search & Filter Bar -->
  <div class="card control-card">
    <div class="search-input-wrapper">
      <Search size={18} class="search-icon" />
      <input 
        type="text" 
        placeholder="Search assembly by name, code, or location (e.g. UK Parliament, GB-SCT, Holyrood)..." 
        bind:value={searchQuery}
        class="search-input"
      />
    </div>

    <div class="filter-buttons">
      <button 
        class="filter-btn {selectedFilter === 'ALL' ? 'active' : ''}" 
        onclick={() => selectedFilter = 'ALL'}
      >
        All Parliaments ({parliamentList.length})
      </button>
      <button 
        class="filter-btn {selectedFilter === 'BICD' ? 'active' : ''}" 
        onclick={() => selectedFilter = 'BICD'}
      >
        BICD Group (8)
      </button>
      <button 
        class="filter-btn {selectedFilter === 'GLOBAL' ? 'active' : ''}" 
        onclick={() => selectedFilter = 'GLOBAL'}
      >
        Major Global (6+)
      </button>
    </div>
  </div>

  <!-- Parliaments Grid -->
  <div class="atlas-grid">
    {#each filteredParliaments as item}
      <div class="card atlas-card">
        <div class="card-top">
          <span class="badge badge-bicd">{item.code}</span>
          {#if item.status === 'IN_AUDIT'}
            <span class="badge badge-live">In Audit</span>
          {:else}
            <span class="badge badge-pending">Planned</span>
          {/if}
        </div>

        <div class="card-body">
          <h3 class="parliament-title">{item.name}</h3>
          <p class="parliament-meta">{item.location} &bull; {item.region} Group</p>

          <div class="specs-list">
            <div class="spec-row">
              <span class="spec-key">Access Method</span>
              <span class="spec-val">{item.access}</span>
            </div>
            <div class="spec-row">
              <span class="spec-key">Provenance Model</span>
              <span class="spec-val">{item.provenance}</span>
            </div>
          </div>
        </div>

        <div class="card-footer">
          <a href={item.docs} class="btn-secondary btn-full">
            View Audit Blueprint <ArrowRight size={14} />
          </a>
        </div>
      </div>
    {/each}
  </div>
</div>

<style>
  .page-padding { padding: 3rem 1.5rem; }
  .page-header { text-align: center; max-width: 800px; margin: 0 auto 3rem; }
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
  .page-sub { font-size: 1.1rem; color: var(--text-muted); }

  .control-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
    margin-bottom: 2.5rem;
    padding: 1rem 1.5rem;
  }

  .search-input-wrapper {
    position: relative;
    flex: 1;
    display: flex;
    align-items: center;
  }

  .search-input-wrapper :global(.search-icon) {
    position: absolute;
    left: 1rem;
    color: var(--text-dim);
  }

  .search-input {
    width: 100%;
    background: #0b0f19;
    border: 1px solid var(--border-subtle);
    border-radius: 0.65rem;
    padding: 0.75rem 1rem 0.75rem 2.75rem;
    color: var(--text-main);
    font-size: 0.95rem;
  }
  .search-input:focus { outline: none; border-color: var(--accent-indigo); }

  .filter-buttons { display: flex; gap: 0.5rem; }
  .filter-btn {
    background: rgba(31, 41, 55, 0.6);
    border: 1px solid var(--border-subtle);
    color: var(--text-muted);
    padding: 0.6rem 1rem;
    border-radius: 0.5rem;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .filter-btn:hover { color: var(--text-main); background: var(--bg-card-hover); }
  .filter-btn.active { background: var(--accent-indigo); color: #ffffff; border-color: var(--accent-indigo); }

  .atlas-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
  }

  .atlas-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .card-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; }
  .parliament-title { font-size: 1.25rem; color: #ffffff; }
  .parliament-meta { font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.25rem; }

  .specs-list {
    background: rgba(11, 15, 25, 0.6);
    border: 1px solid var(--border-subtle);
    border-radius: 0.65rem;
    padding: 0.85rem;
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    margin-bottom: 1.25rem;
  }

  .spec-row { display: flex; align-items: center; justify-content: space-between; font-size: 0.8rem; }
  .spec-key { color: var(--text-dim); }
  .spec-val { color: var(--text-main); font-weight: 500; }
  .btn-full { width: 100%; justify-content: center; }

  @media (max-width: 1024px) {
    .atlas-grid { grid-template-columns: repeat(2, 1fr); }
    .control-card { flex-direction: column; align-items: stretch; }
  }
  @media (max-width: 640px) {
    .atlas-grid { grid-template-columns: 1fr; }
  }
</style>
