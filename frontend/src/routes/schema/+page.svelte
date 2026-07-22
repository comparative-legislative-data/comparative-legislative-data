<script lang="ts">
  import { Layers, FileCode2, CheckCircle2, Copy } from 'lucide-svelte';

  const schemaExample = `{
  "canonical_id": "GB-SCT-S6-SPB13",
  "jurisdiction_code": "GB-SCT",
  
  "normalized": {
    "title": "Gender Recognition Reform (Scotland) Bill",
    "parliament_term": "Session 6",
    "session_subperiod": "Session 6",
    "session_start_date": "2021-05-13",
    "session_end_date": "2026-05-07",
    "initiator_type": "EXECUTIVE",
    "initiator_party_governance_role": "GOVERNING_PARTY",
    "date_introduced": "2022-03-03",
    "date_final_outcome": "2022-12-22",
    "duration_calendar_days": 294,
    "duration_sitting_days": 82,
    "suspension_interrupted": false,
    "final_status": "ENACTED",
    "termination_mechanism": "ENACTMENT",
    "rebellions_flag": false,
    "cross_party_sponsorship_count": 0,
    "derivation_confidence": "HIGH",
    "stage_milestones": [
      {
        "stage_canonical": "FIRST_READING",
        "stage_raw": "Introduced",
        "chamber": "DEVOLVED_UNICAMERAL",
        "date_stage": "2022-03-03",
        "proceedings_url": "https://www.parliament.scot/bills/5"
      },
      {
        "stage_canonical": "COMMITTEE_STAGE",
        "stage_raw": "Stage 1 (Committee Consideration)",
        "chamber": "DEVOLVED_UNICAMERAL",
        "date_stage": "2022-10-06",
        "proceedings_url": "https://www.parliament.scot/bills/5#stage1"
      },
      {
        "stage_canonical": "FINAL_PASSAGE",
        "stage_raw": "Stage 3 (Passed)",
        "chamber": "DEVOLVED_UNICAMERAL",
        "date_stage": "2022-12-22",
        "proceedings_url": "https://www.parliament.scot/bills/5#stage3"
      }
    ]
  },
  
  "native": {
    "local_bill_id": "SP Bill 13",
    "title_native": "Gender Recognition Reform (Scotland) Bill",
    "initiator_raw": "Cabinet Secretary for Social Justice",
    "initiator_name": "Shona Robison MSP",
    "initiator_member_id": "Q59385108",
    "initiator_party": "Scottish National Party",
    "raw_status": "Passed (Subject to Section 35 Order)",
    "parliament_term_raw": "Session 6 (2021-2026)",
    "official_proceedings_url": "https://www.parliament.scot/bills-and-laws/bills/gender-recognition-reform-scotland-bill",
    "official_publication_ref": "SP Bill 13 Session 6 (2022)"
  },
  
  "provenance": {
    "source_url": "https://www.parliament.scot/api/bills/5",
    "retrieved_at": "2026-07-22T08:30:00Z",
    "raw_payload_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "scraper_version": "0.1.0-gb-sct",
    "zenodo_doi": "10.5281/zenodo.1234567",
    "license": "Open Government Licence v3.0"
  }
}`;

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
        'name': 'Schema',
        'item': 'https://legislativedata.org/schema'
      }
    ]
  };

  const termSetSchema = {
    '@context': 'https://schema.org',
    '@type': 'DefinedTermSet',
    'name': 'Canonical Dual-Layer Legislative Data Schema',
    'url': 'https://legislativedata.org/schema',
    'description': 'Dual-layer data schema standardizing cross-national comparative legislative variables alongside native national fields.',
    'hasDefinedTerm': [
      { '@type': 'DefinedTerm', 'name': 'Bill', 'description': 'Canonical legislative proposal model.' },
      { '@type': 'DefinedTerm', 'name': 'Sponsor', 'description': 'Primary initiator and cross-party sponsorship metadata.' },
      { '@type': 'DefinedTerm', 'name': 'StageMilestone', 'description': 'Standardized parliamentary stage progression sequence.' }
    ]
  };
</script>

<svelte:head>
  <title>Canonical Data Schema Specification — Comparative Legislative Data Platform</title>
  <meta name="description" content="Canonical dual-layer data schema specification mapping normalized comparative legislative variables alongside native country fields and 3-tier provenance metadata." />
  <meta name="keywords" content="legislative schema, parliamentary data model, dual layer schema, Pydantic bill model, legislative variables" />

  <meta property="og:title" content="Canonical Data Schema Specification — Comparative Legislative Data Platform" />
  <meta property="og:description" content="Dual-layer data schema standardizing cross-national comparative legislative variables." />

  <!-- Page Structured Data (JSON-LD) -->
  {@html `<script type="application/ld+json">${JSON.stringify(breadcrumbSchema)}</script>`}
  {@html `<script type="application/ld+json">${JSON.stringify(termSetSchema)}</script>`}
</svelte:head>

<div class="container page-padding">
  <!-- Page Header -->
  <div class="page-header">
    <div class="header-badge">
      <span class="badge badge-bicd">Single Source of Truth</span>
      <span>Pydantic v2 & JSON Schema</span>
    </div>
    <h1 class="page-title">Canonical Legislative Schema SSOT</h1>
    <p class="page-sub">
      Delivering dual-layer payloads with explicit <code>normalized.*</code> comparative fields, <code>native.*</code> country-specific details, and <code>provenance.*</code> audit metadata.
    </p>
  </div>

  <!-- Interactive Code Viewer -->
  <div class="card schema-card">
    <div class="schema-header">
      <div class="schema-title">
        <FileCode2 size={18} color="#38bdf8" />
        <span>Canonical Bill Response Payload (`Bill`)</span>
      </div>
      <span class="badge badge-live">v2.0 Peer-Reviewed</span>
    </div>

    <pre class="schema-code">{schemaExample}</pre>
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

  .schema-card { padding: 0; overflow: hidden; max-width: 950px; margin: 0 auto; }
  
  .schema-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.5rem;
    background: #0d1117;
    border-bottom: 1px solid var(--border-subtle);
  }

  .schema-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
    font-size: 0.95rem;
  }

  .schema-code {
    padding: 1.5rem;
    margin: 0;
    border: none;
    border-radius: 0;
    font-size: 0.875rem;
    line-height: 1.6;
    color: #e5e7eb;
  }
</style>
