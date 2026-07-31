<script lang="ts">
  import { ShieldCheck, Database, ArrowRight, ExternalLink, HelpCircle, AlertTriangle, ChevronDown, ChevronUp, BarChart2 } from 'lucide-svelte';
  import NativeEndpointModal from '$lib/components/NativeEndpointModal.svelte';
  import CanonicalEndpointModal from '$lib/components/CanonicalEndpointModal.svelte';
  import VariableInspectorModal from '$lib/components/VariableInspectorModal.svelte';

  let isModalOpen = $state(false);
  let selectedEndpoint = $state<any>(null);

  let isCanonicalModalOpen = $state(false);
  let selectedCanonicalEndpoint = $state<any>(null);

  let isVariableModalOpen = $state(false);
  let selectedVariable = $state<any>(null);

  const hubs = [
    {
      title: '🏛️ Bills Hub',
      description: 'Primary legislative tracking databases mapping Bill lifecycle events and progression.',
      endpoints: [
        {
          id: 'bills',
          name: 'Bills (Core Registry)',
          path: 'bills',
          description: 'Returns the master list of Bills introduced, including short titles, long titles, identifiers, and sponsor IDs.',
          params: '',
          quirks: 'Ignores $skip pagination. High volume dataset.'
        },
        {
          id: 'billstages',
          name: 'Bill Stages',
          path: 'billstages',
          description: 'Chronological progression milestones tracking when a Bill reached specific legislative steps (e.g. Stage 1, Stage 2).',
          params: '',
          quirks: 'Ignores $skip pagination. Requires joining with BillStageTypes.'
        },
        {
          id: 'billtypes',
          name: 'Bill Types',
          path: 'billtypes',
          description: 'Lookup list defining the categories of Bills (e.g., Executive/Government, Member\'s, Private, Hybrid).',
          params: '',
          quirks: 'Small static lookup list.'
        },
        {
          id: 'billstagetypes',
          name: 'Bill Stage Types',
          path: 'billstagetypes',
          description: 'Lookup definitions mapping stage IDs to human-readable names (e.g., Royal Assent, Introduced).',
          params: '',
          quirks: 'Static lookup list mapping sequence orders.'
        }
      ]
    },
    {
      title: '👥 Committees Hub',
      description: 'Mapping parliamentary committees, rolls, and member assignment durations.',
      endpoints: [
        {
          id: 'committees',
          name: 'Committees (Core Registry)',
          path: 'committees',
          description: 'Returns the definitions, emails, phones, and active date ranges for all parliamentary committees.',
          params: '',
          quirks: 'Ignores $skip pagination.'
        },
        {
          id: 'personcommitteeroles',
          name: 'Committee Memberships',
          path: 'personcommitteeroles',
          description: 'Junction mapping Members (PersonID) to Committees (CommitteeID) with specific roles and validity dates.',
          params: '',
          quirks: 'Primary source for analyzing committee scrutiny timelines.'
        },
        {
          id: 'committeeroles',
          name: 'Committee Roles',
          path: 'committeeroles',
          description: 'Lookup catalog defining roles on committees (e.g., Convener, Deputy Convener, Committee Member).',
          params: '',
          quirks: 'Small static lookup list.'
        },
        {
          id: 'committeetypes',
          name: 'Committee Types',
          path: 'committeetypes',
          description: 'Lookup catalog defining categories of committees (e.g., Select, Standing, Joint).',
          params: '',
          quirks: 'Static lookup list.'
        }
      ]
    },
    {
      title: '🗳️ Motions & Transcripts Hub',
      description: 'Chamber debate contributions, plenary motions, and member division votes.',
      endpoints: [
        {
          id: 'motionsquestionsanswersmotions',
          name: 'Motions (Plenary)',
          path: 'motionsquestionsanswersmotions',
          description: 'Catalog of plenary motions, including motion text, titles, dates, sponsor MSPs, and amendments.',
          params: '',
          quirks: 'Extremely slow host serialization (~25-30s latency). Contains over 84k records.'
        },
        {
          id: 'votesmotion',
          name: 'Division Votes',
          path: 'votesmotion',
          description: 'Record-by-record division voting results mapping how MSPs voted on specific plenary motions.',
          params: '?year=2024',
          quirks: 'Requires filtering by year (e.g. ?year=2024). Highly denormalized nested JSON.'
        },
        {
          id: 'orsplenarymeeting',
          name: 'Plenary Reports (Speeches)',
          path: 'orsplenarymeeting',
          description: 'Official Hansard contribution transcripts of spoken debates occurring inside the plenary chamber.',
          params: '?year=2024',
          quirks: 'Requires filtering by year. High latency. Nested SpeakerName text fields.'
        },
        {
          id: 'orscommitteemeeting',
          name: 'Committee Reports (Speeches)',
          path: 'orscommitteemeeting',
          description: 'Official Hansard contribution transcripts of spoken debates occurring during committee scrutiny meetings.',
          params: '?year=2024',
          quirks: 'Requires filtering by year. High latency. Nested text fields.'
        }
      ]
    }
  ];

  // Variables Metadata Registry for Interactive Badges
  const CANONICAL_VARIABLES: Record<string, { name: string; tier: string; span: string; description: string; sqlFormula: string; endpoint: string }> = {
    bill_id: {
      name: 'BillID',
      tier: 'Tier 1 (Native Direct)',
      span: '1999 - Present',
      description: 'Unique identifier of the Bill, mapped directly from the raw database.',
      sqlFormula: 'b.id AS bill_id',
      endpoint: 'bills'
    },
    short_name: {
      name: 'ShortName',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: "Standalone field copying the Bill's short text title to allow standalone querying without joining Database A.",
      sqlFormula: 'b.shortname AS short_name',
      endpoint: 'bills'
    },
    session_id: {
      name: 'SessionID',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Parliamentary session (1 to 6) resolved from the Bill\'s introduction date. Note: As of July 2026, the official upstream API does not yet expose Session 7 records.',
      sqlFormula: `COALESCE(s.id, 1) AS session_id -- joined dynamically from raw_gb_sct_sessions`,
      endpoint: 'bills'
    },
    introduction_date: {
      name: 'IntroductionDate',
      tier: 'Tier 1 (Native Direct)',
      span: '1999 - Present',
      description: "The resolved calendar date of the Bill's introduction, mapped to the earliest logged Stage Date.",
      sqlFormula: 'sd.intro_date AS introduction_date',
      endpoint: 'bills'
    },
    bill_type: {
      name: 'BillType',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: "Normalized bill type: Government (consolidating Executive, Government, and Budget), Member's, Committee, Private, Hybrid.",
      sqlFormula: `CASE \n    WHEN b.billtypeid IN (1, 3, 7) THEN 'Government'\n    WHEN b.billtypeid = 2 THEN 'Member''s'\n    WHEN b.billtypeid = 4 THEN 'Committee'\n    WHEN b.billtypeid = 5 THEN 'Private'\n    WHEN b.billtypeid = 6 THEN 'Hybrid'\n    ELSE 'Unknown'\nEND AS bill_type`,
      endpoint: 'bills'
    },
    sponsor_type: {
      name: 'SponsorType',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Classification of sponsor origin: GOVERNMENT (consolidating Executive, Government, and Budget types) or NON_GOVERNMENT.',
      sqlFormula: `CASE \n    WHEN b.billtypeid IN (1, 3, 7) THEN 'GOVERNMENT' \n    ELSE 'NON_GOVERNMENT' \nEND AS sponsor_type`,
      endpoint: 'bills'
    },
    sponsor_name: {
      name: 'SponsorName',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Parliamentary name of the sponsoring member of parliament, resolved Law Officer title, or External Private Promoter designation.',
      sqlFormula: `CASE \n    WHEN b.billtypeid = 5 THEN 'External Private Promoter'\n    WHEN m.personid IS NULL AND b.billtypeid IN (1, 3, 7) THEN 'Lord Advocate (Law Officer)'\n    ELSE COALESCE(m.parliamentaryname, 'Unknown')\nEND AS sponsor_name`,
      endpoint: 'bills'
    },
    sponsor_gender_id: {
      name: 'SponsorGenderID',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Gender code of the sponsoring member of parliament.',
      sqlFormula: 'm.gendertypeid AS sponsor_gender_id',
      endpoint: 'bills'
    },
    sponsor_party_id: {
      name: 'SponsorPartyID',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Political party identifier of the sponsor on date of introduction. Non-MSP government leads map to synthetic ID 99; Private bills map to synthetic ID 98.',
      sqlFormula: `CASE \n    WHEN b.billtypeid = 5 THEN 98\n    WHEN m.personid IS NULL AND b.billtypeid IN (1, 3, 7) THEN 99\n    ELSE sp.sponsor_party_id\nEND AS sponsor_party_id`,
      endpoint: 'bills'
    },
    sponsor_governing_status: {
      name: 'SponsorGoverningStatus',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Indicates whether the sponsor was a member of the governing party/coalition on the date of introduction.',
      sqlFormula: `CASE WHEN sp.is_governing = TRUE THEN 'GOVERNING' ELSE 'OPPOSITION' END AS sponsor_governing_status`,
      endpoint: 'bills'
    },
    gov_minority_status: {
      name: 'GovMinorityStatus',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Indicates whether the government held a majority or minority of seats on the date of introduction.',
      sqlFormula: `CASE WHEN g.is_minority = TRUE THEN 'MINORITY' ELSE 'MAJORITY' END AS gov_minority_status`,
      endpoint: 'bills'
    },
    sponsor_is_first_time: {
      name: 'SponsorIsFirstTime',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Indicates if the sponsoring member of parliament was in their first term of service when the bill was introduced.',
      sqlFormula: `CASE \n    WHEN MIN(mp.validfromdate) >= session_start_date THEN TRUE \n    ELSE FALSE \nEND AS sponsor_is_first_time`,
      endpoint: 'bills'
    },
    sessional_bill_load: {
      name: 'SessionalBillLoad',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Total number of bills introduced during the session, representing sessional workload.',
      sqlFormula: `(COUNT(*) OVER (PARTITION BY session_id))::integer AS sessional_bill_load`,
      endpoint: 'bills'
    },
    passed_stage_3: {
      name: 'PassedStage3',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Indicates if the bill successfully passed the Stage 3 completion vote.',
      sqlFormula: `CASE WHEN s3_date IS NOT NULL THEN TRUE ELSE FALSE END AS passed_stage_3`,
      endpoint: 'bills'
    },
    went_to_reconsideration: {
      name: 'WentToReconsideration',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Indicates if the bill was referred back for Reconsideration Stage.',
      sqlFormula: `CASE WHEN recon_date IS NOT NULL THEN TRUE ELSE FALSE END AS went_to_reconsideration`,
      endpoint: 'bills'
    },
    bill_outcome: {
      name: 'BillOutcome',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Normalized legislative result: PASSED (passed Stage 3) or FALLEN (failed to pass).',
      sqlFormula: `CASE \n    WHEN s3_date IS NOT NULL THEN 'PASSED'\n    ELSE 'FALLEN'\nEND AS bill_outcome`,
      endpoint: 'bills'
    },
    t1_duration_calendar: {
      name: 'T1DurationCalendar',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Calendar days between the introduction date (or earliest stage date fallback) and Stage 1 completion.',
      sqlFormula: `(sd.s1_date - sd.intro_date)::integer AS t1_duration_calendar`,
      endpoint: 'bills'
    },
    t2_duration_calendar: {
      name: 'T2DurationCalendar',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Calendar days between Stage 1 completion and Stage 2 completion.',
      sqlFormula: `(sd.s2_date - sd.s1_date)::integer AS t2_duration_calendar`,
      endpoint: 'bills'
    },
    t3_duration_calendar: {
      name: 'T3DurationCalendar',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Calendar days between Stage 2 completion and Stage 3 Passage.',
      sqlFormula: `(sd.s3_date - sd.s2_date)::integer AS t3_duration_calendar`,
      endpoint: 'bills'
    },
    viscosity_outlier: {
      name: 'ViscosityOutlier',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Outlier indicator highlighting bills experiencing abnormal delays, triggered by going to Reconsideration.',
      sqlFormula: `CASE WHEN recon_date IS NOT NULL THEN TRUE ELSE FALSE END AS viscosity_outlier`,
      endpoint: 'bills'
    },
    snapshot_date: {
      name: 'SnapshotDate',
      tier: 'Tier 1 (Native Direct)',
      span: '1999 - Present',
      description: 'First calendar day of the month for the snapshot date, generated natively in a monthly series.',
      sqlFormula: `generate_series('1999-05-01'::date, CURRENT_DATE::date, '1 month'::interval)::date AS snapshot_date`,
      endpoint: 'memberpartyhistory'
    },
    party_id: {
      name: 'PartyID',
      tier: 'Tier 1 (Native Direct)',
      span: '1999 - Present',
      description: 'Unique identifier of the political party mapping to the raw parties database.',
      sqlFormula: 'mp.partyid AS party_id',
      endpoint: 'memberpartyhistory'
    },
    party_name: {
      name: 'PartyName',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Preferred text name of the political party (e.g. Scottish Labour Party), defaulting to Independent.',
      sqlFormula: "COALESCE(p.preferredname, 'Independent') AS party_name",
      endpoint: 'memberpartyhistory'
    },
    member_count: {
      name: 'MemberCount',
      tier: 'Tier 2 (Derived Deterministic)',
      span: '1999 - Present',
      description: 'Number of active unique members holding seats for that party on the snapshot date.',
      sqlFormula: 'COUNT(DISTINCT mp.personid) AS member_count',
      endpoint: 'memberpartyhistory'
    }
  };

  const canonicalHubs = [
    {
      title: '📊 Canonical Research Datasets',
      description: 'Fully isolated derived variables layer computed strictly in Database B with 0% raw mirror contamination.',
      endpoints: [
        {
          id: 'canonical_bills',
          name: 'Canonical Bills (Stage Durations & Outcomes)',
          path: 'bills',
          isCanonical: true,
          description: 'Calculates calendar day durations for Stages 1, 2, and 3, sponsors\' temporal party affiliation, minority cabinet status, sessional bill load, and passage outcomes.',
          params: '',
          quirks: 'Comes from Database B. Supports standard OData query filters.',
          variables: ['bill_id', 'short_name', 'session_id', 'introduction_date', 'bill_type', 'sponsor_type', 'sponsor_name', 'sponsor_gender_id', 'sponsor_party_id', 'sponsor_governing_status', 'sponsor_is_first_time', 'gov_minority_status', 'sessional_bill_load', 'passed_stage_3', 'went_to_reconsideration', 'bill_outcome', 't1_duration_calendar', 't2_duration_calendar', 't3_duration_calendar', 'viscosity_outlier']
        },
        {
          id: 'canonical_memberpartyhistory',
          name: 'Canonical Monthly Party Seats Snapshots',
          path: 'memberpartyhistory',
          isCanonical: true,
          description: 'Monthly historical counts of active seats held by each political party in the Scottish Parliament since 1999.',
          params: '',
          quirks: 'Comes from Database B. Supports standard OData query filters.',
          variables: ['snapshot_date', 'party_id', 'party_name', 'member_count']
        }
      ]
    }
  ];

  let expandedHubs = $state<Record<string, boolean>>({
    'bills': false,
    'committees': false,
    'motions': false
  });

  let expandedCanonicalHub = $state(false);

  let showTransparency = $state(false);
  let showAudit = $state(false);

  const hubKeys: Record<string, string> = {
    '🏛️ Bills Hub': 'bills',
    '👥 Committees Hub': 'committees',
    '🗳️ Motions & Transcripts Hub': 'motions'
  };

  function toggleHub(title: string) {
    const key = hubKeys[title];
    expandedHubs[key] = !expandedHubs[key];
  }

  function openEndpoint(endpoint: any) {
    selectedEndpoint = endpoint;
    isModalOpen = true;
  }

  function openCanonicalEndpoint(endpoint: any) {
    selectedCanonicalEndpoint = endpoint;
    isCanonicalModalOpen = true;
  }

  function openVariable(varKey: string) {
    selectedVariable = CANONICAL_VARIABLES[varKey];
    isVariableModalOpen = true;
  }
</script>

<svelte:head>
  <title>Native API Explorer | Scottish Parliament (GB-SCT)</title>
  <meta name="description" content="Academic explorer mapping raw Scottish Parliament OData endpoints into relational hubs with dynamic schema audits." />
</svelte:head>

<div class="explorer-container">
  <div class="container py-12">
    
    <!-- Header Section -->
    <div class="header-section text-center mb-8">
      <div class="badge-row mb-4">
        <span class="badge badge-pilot">Pilot Phase: GB-SCT</span>
        <span class="badge badge-transparent"><ShieldCheck size={12} /> 100% Raw Passthrough</span>
      </div>
      <h1 class="page-title">Native API Explorer</h1>
      <h2 class="page-subtitle text-indigo-400">Scottish Parliament (data.parliament.scot)</h2>


    </div>

    <!-- Main Workspace Grid (3-Column Hubs) -->
    <div class="hubs-grid mt-8">
      {#each hubs as hub}
        {@const key = hubKeys[hub.title]}
        <section class="hub-card">
          <div class="hub-header">
            <h2>{hub.title}</h2>
            <p class="hub-desc mt-2">{hub.description}</p>
          </div>
          <button class="btn-toggle mt-4 w-full" onclick={() => toggleHub(hub.title)}>
            {#if expandedHubs[key]}
              Hide Endpoints <ChevronUp size={16} />
            {:else}
              Show Endpoints <ChevronDown size={16} />
            {/if}
          </button>

          {#if expandedHubs[key]}
            <div class="endpoints-list mt-4">
            {#each hub.endpoints as ep}
              <button class="endpoint-item" onclick={() => openEndpoint(ep)}>
                <div class="endpoint-main">
                  <div class="endpoint-name-row">
                    <Database size={16} class="text-indigo-400" />
                    <h3>{ep.name}</h3>
                  </div>
                  <p class="endpoint-desc">{ep.description}</p>
                  
                  {#if ep.params}
                    <div class="param-badge mt-2">
                      <span class="text-muted">Query Required:</span>
                      <code>{ep.params}</code>
                    </div>
                  {/if}
                  
                  {#if ep.quirks}
                    <div class="quirk-badge mt-2">
                      <HelpCircle size={12} class="text-amber-400" />
                      <span>{ep.quirks}</span>
                    </div>
                  {/if}
                </div>
                <div class="endpoint-action">
                  <span class="btn-action">Inspect <ArrowRight size={14} /></span>
                </div>
              </button>
            {/each}
            </div>
          {/if}
        </section>
      {/each}
    </div>

    <!-- Canonical Research Hub Section (Visually distinct with emerald accent) -->
    <div class="canonical-hub-container mt-12">
      {#each canonicalHubs as hub}
        <section class="hub-card hub-card-canonical">
          <div class="hub-header">
            <span class="badge badge-canonical mb-2">Academic Research Layer</span>
            <h2>{hub.title}</h2>
            <p class="hub-desc mt-2">{hub.description}</p>
          </div>
          <button class="btn-toggle btn-toggle-canonical mt-4 w-full" onclick={() => expandedCanonicalHub = !expandedCanonicalHub}>
            {#if expandedCanonicalHub}
              Hide Research Datasets <ChevronUp size={16} />
            {:else}
              Show Research Datasets <ChevronDown size={16} />
            {/if}
          </button>

          {#if expandedCanonicalHub}
            <div class="endpoints-list-canonical mt-6">
              {#each hub.endpoints as ep}
                <div class="endpoint-item-canonical">
                  <div class="endpoint-main w-full">
                    <div class="endpoint-name-row">
                      <Database size={16} class="text-emerald-400" />
                      <h3>{ep.name}</h3>
                    </div>
                    <p class="endpoint-desc">{ep.description}</p>

                    <!-- Variable-level Clickable Badges -->
                    <div class="variables-badges-container mt-4">
                      <span class="variables-label">Click Variables to Inspect Math & Codebook:</span>
                      <div class="variables-grid mt-2">
                        {#each ep.variables as varKey}
                          {@const variableInfo = CANONICAL_VARIABLES[varKey]}
                          <button 
                            class="variable-badge" 
                            class:variable-tier1={variableInfo.tier.includes('Tier 1')}
                            class:variable-tier2={variableInfo.tier.includes('Tier 2')}
                            onclick={() => openVariable(varKey)}
                          >
                            {variableInfo.name}
                          </button>
                        {/each}
                      </div>
                    </div>
                  </div>
                  <div class="endpoint-action mt-4">
                    <button class="btn-action btn-action-canonical" onclick={() => openCanonicalEndpoint(ep)}>
                      Inspect Dataset API & Downloads <ArrowRight size={14} />
                    </button>
                  </div>
                </div>
              {/each}
            </div>
          {/if}

        </section>
      {/each}
    </div>

    <!-- Stage 3 Navigation Banner to Charts Dashboard (Full-Width Block) -->
    <div class="charts-nav-banner mt-12 w-full">
      <div class="banner-content">
        <div class="banner-icon-col">
          <span class="pulse-dot"></span>
          <BarChart2 size={20} class="text-emerald-400" />
        </div>
        <div class="banner-text-col">
          <h4>Holyrood Research Charts & Analytics Dashboard</h4>
          <p>Visual trends, workload heatmaps, sessional volumes, and OLS/Logistic regression models.</p>
        </div>
      </div>
      <a href="/pilot/gb-sct/charts" class="btn-banner-link">
        Open Analytics Dashboard <ArrowRight size={14} />
      </a>
    </div>


    <!-- Collapsible Explainers Section Below -->
    <div class="explainers-grid mt-8">
      <!-- Transparency Proxy Card -->
      <div class="sidebar-card">
        <button class="sidebar-card-header" onclick={() => showTransparency = !showTransparency} aria-expanded={showTransparency}>
          <div class="header-left">
            <HelpCircle size={16} class="text-indigo-400" />
            <h3>Academic Transparency</h3>
          </div>
          {#if showTransparency}
            <ChevronUp size={16} class="text-slate-400" />
          {:else}
            <ChevronDown size={16} class="text-slate-400" />
          {/if}
        </button>
        
        {#if showTransparency}
          <div class="sidebar-card-content mt-3">
            <p class="sidebar-desc">
              This explorer provides raw, direct access to the OData feeds served by the Scottish Parliament.
              Our un-gated CORS proxy acts as a transparent relay to bypass browser restrictions.
            </p>
            <div class="alert-border-box mt-3">
              <strong>OData Pagination Note:</strong> The host API ignores <code>$skip</code>. High-volume resources must be queried by filters (e.g. <code>?year=YYYY</code>) rather than standard skips to prevent infinite retrieval loops.
            </div>
          </div>
        {/if}
      </div>

      <!-- Academic Integrity & Parity Card -->
      <div class="sidebar-card">
        <button class="sidebar-card-header" onclick={() => showAudit = !showAudit} aria-expanded={showAudit}>
          <div class="header-left">
            <ShieldCheck size={16} class="text-emerald-400" />
            <h3>Parity & Trust Audit</h3>
          </div>
          {#if showAudit}
            <ChevronUp size={16} class="text-slate-400" />
          {:else}
            <ChevronDown size={16} class="text-slate-400" />
          {/if}
        </button>

        {#if showAudit}
          <div class="sidebar-card-content mt-3">
            <p class="sidebar-desc">
              To ensure peer-review reliability, our database mirror undergoes automated field-by-field audits against the live OData endpoints.
              Normalizations are strictly restricted to type casting (e.g. mapping empty strings to PostgreSQL <code>NULL</code>).
            </p>
            <div class="integrity-links mt-4 flex flex-col gap-2">
              <a href="https://github.com/stevenmacgregor/comparativelegislativedata/blob/main/scripts/sync_gb_sct.py" target="_blank" rel="noopener noreferrer" class="integrity-link">
                View Sync Pipeline Script <ExternalLink size={10} />
              </a>
              <a href="https://github.com/stevenmacgregor/comparativelegislativedata/blob/main/scripts/audit_gb_sct_parity.py" target="_blank" rel="noopener noreferrer" class="integrity-link">
                View Parity Audit Script <ExternalLink size={10} />
              </a>
              <div class="mt-2">
                <span class="audit-status-badge">Last Parity Audit: 100% Passed</span>
              </div>
            </div>
          </div>
        {/if}
      </div>
    </div>

  </div>
</div>

<NativeEndpointModal bind:isOpen={isModalOpen} endpoint={selectedEndpoint} />
<CanonicalEndpointModal bind:isOpen={isCanonicalModalOpen} endpoint={selectedCanonicalEndpoint} />
<VariableInspectorModal bind:isOpen={isVariableModalOpen} variable={selectedVariable} />

<style>
  .explorer-container {
    min-height: calc(100vh - 4.25rem);
    background: #090d16;
    color: #f8fafc;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }

  .py-12 { padding-top: 3.5rem; padding-bottom: 3.5rem; }
  .mb-12 { margin-bottom: 3rem; }
  .mt-4 { margin-top: 1rem; }
  .mt-6 { margin-top: 1.5rem; }
  .mt-12 { margin-top: 3rem; }
  .mb-4 { margin-bottom: 1rem; }
  .mx-auto { margin-left: auto; margin-right: auto; }
  .mt-2 { margin-top: 0.5rem; }

  .text-center { text-align: center; }
  .text-indigo-400 { color: #818cf8; }

  .badge-row {
    display: inline-flex;
    gap: 0.75rem;
    justify-content: center;
  }

  .badge {
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
  }

  .badge-pilot { background: rgba(99, 102, 241, 0.15); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.3); }
  .badge-transparent { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }

  .sidebar-card {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 0.85rem;
    padding: 1rem 1.25rem;
    text-align: left;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
  }
  .sidebar-card:hover {
    border-color: rgba(99, 102, 241, 0.2);
  }
  .sidebar-card-header {
    width: 100%;
    background: transparent;
    border: none;
    padding: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    color: #ffffff;
  }
  .header-left {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .header-left h3 {
    margin: 0;
    font-size: 0.875rem;
    font-weight: 600;
    color: #ffffff;
  }
  .sidebar-desc {
    color: #94a3b8;
    font-size: 0.75rem;
    line-height: 1.5;
    margin: 0;
  }
  .integrity-links {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
  }
  .integrity-link {
    color: #38bdf8;
    text-decoration: none;
    font-size: 0.75rem;
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    font-weight: 600;
  }
  .integrity-link:hover {
    text-decoration: underline;
    color: #0ea5e9;
  }
  .divider {
    color: rgba(255,255,255,0.15);
    font-size: 0.75rem;
  }

  .audit-status-badge {
    background: rgba(52, 211, 153, 0.15);
    color: #34d399;
    border: 1px solid rgba(52, 211, 153, 0.25);
    padding: 0.15rem 0.45rem;
    border-radius: 0.25rem;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
  }

  .page-title {
    font-family: var(--font-heading);
    font-size: 2.75rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
    line-height: 1.1;
  }

  .page-subtitle {
    font-family: var(--font-mono);
    font-size: 1.1rem;
    margin-top: 0.5rem;
    font-weight: normal;
  }

  .alert-border-box {
    border-left: 2px solid #fbbf24;
    background: rgba(251, 191, 36, 0.03);
    padding: 0.6rem 0.8rem;
    border-radius: 0 0.375rem 0.375rem 0;
    font-size: 0.725rem;
    color: #cbd5e1;
    line-height: 1.45;
  }
  .alert-border-box code {
    background: rgba(0, 0, 0, 0.3);
    padding: 0.1rem 0.25rem;
    border-radius: 0.25rem;
    color: #fbbf24;
  }

  .hubs-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    align-items: start;
    text-align: left;
  }

  .explainers-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    align-items: start;
    text-align: left;
  }

  @media (max-width: 1024px) {
    .hubs-grid {
      grid-template-columns: 1fr;
    }
    .explainers-grid {
      grid-template-columns: 1fr;
    }
  }

  .hub-card {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 0.85rem;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 200px;
  }

  .hub-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1.5rem;
  }

  .btn-toggle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    background: rgba(99, 102, 241, 0.1);
    color: #a5b4fc;
    border: 1px solid rgba(99, 102, 241, 0.25);
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
    width: 100%;
    position: relative;
    z-index: 10;
  }
  .btn-toggle:hover {
    background: rgba(99, 102, 241, 0.2);
    border-color: #818cf8;
    color: #ffffff;
  }

  .hub-header h2 {
    font-family: var(--font-heading);
    font-size: 1.25rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
  }

  .hub-desc {
    color: #94a3b8;
    font-size: 0.8rem;
    line-height: 1.45;
    margin: 0.5rem 0 0 0;
  }

  .endpoints-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1.5rem;
  }

  .endpoint-item {
    background: rgba(2, 6, 23, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 0.65rem;
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    text-align: left;
    cursor: pointer;
    transition: all 0.2s ease;
    width: 100%;
    gap: 0.75rem;
  }

  .endpoint-item:hover {
    background: rgba(15, 23, 42, 0.7);
    border-color: rgba(99, 102, 241, 0.35);
    transform: translateX(4px);
  }

  .endpoint-name-row {
    display: flex;
    align-items: center;
    gap: 0.65rem;
  }

  .endpoint-name-row h3 {
    margin: 0;
    font-size: 0.95rem;
    font-weight: 700;
    color: #ffffff;
  }

  .endpoint-desc {
    color: #94a3b8;
    font-size: 0.75rem;
    margin: 0.35rem 0 0 0;
    line-height: 1.4;
  }

  .param-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.75rem;
    background: rgba(255,255,255,0.03);
    padding: 0.2rem 0.5rem;
    border-radius: 0.25rem;
    border: 1px solid rgba(255,255,255,0.05);
  }
  .param-badge code {
    color: #38bdf8;
    font-family: var(--font-mono);
  }

  .quirk-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.75rem;
    color: #fbbf24;
    background: rgba(251, 191, 36, 0.05);
    padding: 0.2rem 0.5rem;
    border-radius: 0.25rem;
    border: 1px solid rgba(251, 191, 36, 0.15);
  }

  .btn-action {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(99, 102, 241, 0.1);
    color: #a5b4fc;
    border: 1px solid rgba(99, 102, 241, 0.25);
    padding: 0.45rem 1rem;
    border-radius: 0.5rem;
    font-size: 0.8rem;
    font-weight: 600;
    transition: all 0.2s ease;
  }

  .endpoint-item:hover .btn-action {
    background: #4f46e5;
    color: #ffffff;
    border-color: #4f46e5;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
  }

  /* Canonical Hub Accents & Styles */
  .canonical-hub-container {
    width: 100%;
    margin-top: 3rem;
  }
  .hub-card-canonical {
    border-color: rgba(16, 185, 129, 0.2) !important;
    background: rgba(4, 6, 10, 0.4) !important;
    box-shadow: 0 4px 30px rgba(16, 185, 129, 0.05);
  }
  .btn-toggle-canonical {
    background: rgba(16, 185, 129, 0.1) !important;
    color: #a7f3d0 !important;
    border-color: rgba(16, 185, 129, 0.25) !important;
  }
  .btn-toggle-canonical:hover {
    background: rgba(16, 185, 129, 0.2) !important;
    border-color: #10b981 !important;
    color: #ffffff !important;
  }
  .badge-canonical {
    background: rgba(16, 185, 129, 0.15) !important;
    color: #34d399 !important;
    border: 1px solid rgba(16, 185, 129, 0.3) !important;
  }

  .endpoints-list-canonical {
    display: grid !important;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-top: 1.5rem;
  }
  @media (max-width: 768px) {
    .endpoints-list-canonical {
      grid-template-columns: 1fr;
    }
  }

  .endpoint-item-canonical {
    background: rgba(2, 6, 23, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.04) !important;
    border-radius: 0.85rem !important;
    padding: 1.5rem !important;
    display: flex;
    flex-direction: column !important;
    align-items: flex-start !important;
    cursor: default !important;
    transition: all 0.2s ease;
    text-align: left;
    height: 100%;
  }
  .endpoint-item-canonical:hover {
    border-color: rgba(16, 185, 129, 0.3) !important;
    background: rgba(15, 23, 42, 0.6) !important;
    transform: none !important;
  }

  /* Interactive Variables Grid */
  .variables-badges-container {
    width: 100%;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    padding-top: 1rem;
  }
  .variables-label {
    font-size: 0.75rem;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .variables-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  .variable-badge {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    color: #cbd5e1;
    padding: 0.25rem 0.65rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .variable-badge:hover {
    transform: scale(1.05);
    color: #ffffff;
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.15);
  }
  .variable-tier1 {
    border-color: rgba(56, 189, 248, 0.3);
    background: rgba(56, 189, 248, 0.05);
    color: #38bdf8;
  }
  .variable-tier1:hover {
    border-color: #38bdf8;
    background: rgba(56, 189, 248, 0.12);
  }
  .variable-tier2 {
    border-color: rgba(16, 185, 129, 0.3);
    background: rgba(16, 185, 129, 0.05);
    color: #34d399;
  }
  .variable-tier2:hover {
    border-color: #10b981;
    background: rgba(16, 185, 129, 0.12);
  }

  .btn-action-canonical {
    background: rgba(16, 185, 129, 0.1) !important;
    color: #a7f3d0 !important;
    border-color: rgba(16, 185, 129, 0.25) !important;
    padding: 0.5rem 1.25rem !important;
    font-size: 0.85rem !important;
    cursor: pointer;
    align-self: flex-start;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    border-radius: 0.5rem;
    font-weight: 600;
    transition: all 0.2s ease;
  }
  .btn-action-canonical:hover {
    background: #059669 !important;
    color: #ffffff !important;
    border-color: #059669 !important;
    box-shadow: 0 4px 12px rgba(5, 150, 105, 0.25) !important;
  }
  .w-full { width: 100%; }

  /* Navigation Banner to Charts Dashboard */
  .charts-nav-banner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(16, 185, 129, 0.05);
    border: 1px solid rgba(16, 185, 129, 0.15);
    box-shadow: 0 4px 20px rgba(16, 185, 129, 0.03);
    border-radius: 1rem;
    padding: 1.25rem 1.75rem;
    gap: 1.5rem;
    flex-wrap: wrap;
    text-align: left;
    width: 100%;
    box-sizing: border-box;
    position: relative;
    z-index: 5;
  }
  .banner-content {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex: 1;
    min-width: 250px;
  }
  .banner-icon-col {
    position: relative;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.2);
    padding: 0.65rem;
    border-radius: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #10b981;
  }
  .pulse-dot {
    position: absolute;
    top: -2px;
    right: -2px;
    width: 6px;
    height: 6px;
    background: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10b981;
    animation: pulse 1.5s infinite;
  }
  @keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
  }
  .banner-text-col {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
  }
  .banner-text-col h4 {
    margin: 0;
    font-size: 0.95rem;
    font-weight: 700;
    color: #ffffff;
  }
  .banner-text-col p {
    margin: 0;
    font-size: 0.75rem;
    color: #94a3b8;
    line-height: 1.4;
  }
  .btn-banner-link {
    background: #10b981;
    color: #040815;
    border: none;
    padding: 0.55rem 1.25rem;
    border-radius: 0.5rem;
    font-size: 0.85rem;
    font-weight: 700;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    text-decoration: none;
    transition: all 0.2s ease;
  }
  .btn-banner-link:hover {
    background: #059669;
    color: #ffffff;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.25);
    transform: translateY(-1px);
  }
</style>
