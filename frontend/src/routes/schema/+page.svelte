<script lang="ts">
  import { Layers, Search, Globe, Tag, Info, MessageSquare, Mail } from 'lucide-svelte';

  let searchQuery = $state('');
  let selectedDomain = $state('ALL');

  interface VariableDef {
    name: string;
    domain: string;
    domainCode: string;
    type: string;
    description: string;
    notes?: string;
  }

  const domains = [
    { code: 'ALL', name: 'All 11 Research Domains' },
    { code: 'D1', name: 'Domain 1: Assembly, Electoral & Executive Context' },
    { code: 'D2', name: 'Domain 2: Bill Identification, Sponsorship & Temporal Origin' },
    { code: 'D3', name: 'Domain 3: Progression, Timelines & Stage Milestones' },
    { code: 'D4', name: 'Domain 4: Financial Resolutions & Procedural Motions' },
    { code: 'D5', name: 'Domain 5: Plenary Roll-Call Motions & Voting Coalitions' },
    { code: 'D6', name: 'Domain 6: Accompanying Bill Documents & Text Size' },
    { code: 'D7', name: 'Domain 7: Final Disposition & Inter-Chamber Mechanisms' },
    { code: 'D8', name: 'Domain 8: Macro Amendment Aggregates & Text Alteration' },
    { code: 'D9', name: 'Domain 9: Micro Amendment Entity Records (CanonicalAmendment)' },
    { code: 'D10', name: 'Domain 10: Committee Context & Roster Engine (CommitteeContext)' },
    { code: 'D11', name: 'Domain 11: Parsed Proceedings & Official Report Analytics' }
  ];

  const variables: VariableDef[] = [
    // Domain 1
    { name: 'jurisdiction_code', domainCode: 'D1', domain: 'Domain 1: Assembly & Executive', type: 'String (ISO 3166-2)', description: 'Unique assembly identifier (e.g. GB-UKP, GB-SCT, DE-BT, US-HR).' },
    { name: 'parliament_term', domainCode: 'D1', domain: 'Domain 1: Assembly & Executive', type: 'String', description: 'Macro electoral legislative period (e.g. Session 6, 58th Parliament).' },
    { name: 'term_start_date', domainCode: 'D1', domain: 'Domain 1: Assembly & Executive', type: 'Date (ISO 8601)', description: 'Statutory start date of parliamentary term (from /api/sessions).' },
    { name: 'term_end_date', domainCode: 'D1', domain: 'Domain 1: Assembly & Executive', type: 'Date (ISO 8601)', description: 'Statutory end date of parliamentary term (from /api/sessions).' },
    { name: 'chamber_type', domainCode: 'D1', domain: 'Domain 1: Assembly & Executive', type: 'Enum', description: 'Constitutional chamber structure (SOVEREIGN_BICAMERAL, DEVOLVED_UNICAMERAL, FEDERAL_UPPER, etc).' },
    { name: 'devolved_executive_name', domainCode: 'D1', domain: 'Domain 1: Assembly & Executive', type: 'String', description: 'Historical executive entity name ("Scottish Executive" 1999-2007; "Scottish Government" 2007-Present).' },
    { name: 'government_type', domainCode: 'D1', domain: 'Domain 1: Assembly & Executive', type: 'Enum', description: 'Executive arrangement typology (SINGLE_PARTY_MAJORITY, SINGLE_PARTY_MINORITY, FORMAL_COALITION, COOPERATION_AGREEMENT).', notes: 'Linked to ParlGov cabinet typology.' },
    { name: 'parlgov_cabinet_id', domainCode: 'D1', domain: 'Domain 1: Assembly & Executive', type: 'String', description: 'Canonical cabinet identifier linked from ParlGov authority dataset.' },

    // Domain 2
    { name: 'local_bill_id', domainCode: 'D2', domain: 'Domain 2: Sponsorship & Origin', type: 'String', description: 'Native reference code assigned by host legislature (e.g. SP Bill 13, H.R. 815).' },
    { name: 'title_canonical', domainCode: 'D2', domain: 'Domain 2: Sponsorship & Origin', type: 'String', description: 'Standardized English short title.' },
    { name: 'initiator_type', domainCode: 'D2', domain: 'Domain 2: Sponsorship & Origin', type: 'Enum', description: 'Globally neutral sponsor type (EXECUTIVE, INDIVIDUAL_MEMBER, GROUP_MEMBERS, COMMITTEE).' },
    { name: 'initiator_party_governance_role', domainCode: 'D2', domain: 'Domain 2: Sponsorship & Origin', type: 'Enum', description: 'Primary sponsor alignment (GOVERNING_PARTY, OPPOSITION_PARTY, CROSS_PARTY) evaluated dynamically on introduction date.' },
    { name: 'initiator_member_id', domainCode: 'D2', domain: 'Domain 2: Sponsorship & Origin', type: 'String (Wikidata QID)', description: 'Disambiguated persistent identifier for primary sponsor MP/MSP.' },
    { name: 'ministerial_portfolio_title', domainCode: 'D2', domain: 'Domain 2: Sponsorship & Origin', type: 'String', description: 'Lead Minister exact portfolio title from /api/GovernmentRoles (e.g. Cabinet Secretary for Health).' },
    { name: 'third_party_organisation', domainCode: 'D2', domain: 'Domain 2: Sponsorship & Origin', type: 'String', description: 'External non-governmental promoter organisation from /api/bills (for Private Bills).' },

    // Domain 3
    { name: 'date_introduced', domainCode: 'D3', domain: 'Domain 3: Progression & Control', type: 'Date (ISO 8601)', description: 'Formal introduction date of the bill.' },
    { name: 'date_final_outcome', domainCode: 'D3', domain: 'Domain 3: Progression & Control', type: 'Date (ISO 8601)', description: 'Date of final passage, defeat, or withdrawal.' },
    { name: 'duration_calendar_days', domainCode: 'D3', domain: 'Domain 3: Progression & Control', type: 'Integer', description: 'Calendar days elapsed from introduction to final outcome.' },
    { name: 'duration_sitting_days', domainCode: 'D3', domain: 'Domain 3: Progression & Control', type: 'Integer', description: 'Formal parliamentary sitting days elapsed.' },
    { name: 'stage_1_debate_days_count', domainCode: 'D3', domain: 'Domain 3: Progression & Control', type: 'Integer', description: 'Number of sitting days Stage 1 debate straddled.' },
    { name: 'stage_3_debate_days_count', domainCode: 'D3', domain: 'Domain 3: Progression & Control', type: 'Integer', description: 'Number of sitting days Stage 3 debate straddled.' },
    { name: 'emergency_procedure_flag', domainCode: 'D3', domain: 'Domain 3: Progression & Control', type: 'Boolean', description: 'Indicates whether the bill passed under Emergency procedure under Rule 9.21.' },
    { name: 'section_35_order_triggered_flag', domainCode: 'D3', domain: 'Domain 3: Progression & Control', type: 'Boolean', description: 'Indicates whether Secretary of State Section 35 Scotland Act Order was issued blocking Royal Assent.' },

    // Domain 4: Financial Resolutions
    { name: 'financial_resolution_required_flag', domainCode: 'D4', domain: 'Domain 4: Financial Resolutions', type: 'Boolean', description: 'Financial Resolution required under Rule 9.12 before Stage 2.' },
    { name: 'financial_resolution_approved_flag', domainCode: 'D4', domain: 'Domain 4: Financial Resolutions', type: 'Boolean', description: 'Financial Resolution approved by Parliament.' },
    { name: 'financial_resolution_aye_count', domainCode: 'D4', domain: 'Domain 4: Financial Resolutions', type: 'Integer', description: 'Financial Resolution Aye vote tally.' },

    // Domain 5: Plenary Roll-Call Motions
    { name: 'decision_point_motion_type', domainCode: 'D5', domain: 'Domain 5: Plenary Motions', type: 'Enum', description: 'Plenary motion classification (STAGE_1_AGREEMENT, FINANCIAL_RESOLUTION, EMERGENCY_BILL_DESIGNATION, STAGE_3_PASSAGE).' },
    { name: 'decision_point_party_cohesion_rate', domainCode: 'D5', domain: 'Domain 5: Plenary Motions', type: 'Float (0-1)', description: 'Governing party voting unity rate on division date T.' },

    // Domain 6: Accompanying Documents
    { name: 'doc_as_introduced_url', domainCode: 'D6', domain: 'Domain 6: Accompanying Documents', type: 'URL', description: 'Official text of the Bill as introduced.' },
    { name: 'policy_memorandum_url', domainCode: 'D6', domain: 'Domain 6: Accompanying Documents', type: 'URL', description: 'Policy Memorandum document URL.' },
    { name: 'financial_memorandum_url', domainCode: 'D6', domain: 'Domain 6: Accompanying Documents', type: 'URL', description: 'Standalone Financial Memorandum document URL.' },
    { name: 'explanatory_notes_url', domainCode: 'D6', domain: 'Domain 6: Accompanying Documents', type: 'URL', description: 'Standalone Explanatory Notes document URL.' },
    { name: 'word_count_introduced', domainCode: 'D6', domain: 'Domain 6: Accompanying Documents', type: 'Integer', description: 'Word count of official bill text at introduction.' },
    { name: 'word_count_enacted', domainCode: 'D6', domain: 'Domain 6: Accompanying Documents', type: 'Integer', description: 'Word count of final enacted Act.' },
    { name: 'text_expansion_ratio', domainCode: 'D6', domain: 'Domain 6: Accompanying Documents', type: 'Float', description: 'Ratio of enacted text size vs introduced text size.' },

    // Domain 7
    { name: 'final_status', domainCode: 'D7', domain: 'Domain 7: Disposition & Ping-Pong', type: 'Enum', description: 'Terminal procedural status (ENACTED, DEFEATED, WITHDRAWN, LAPSED, PENDING, VETOED).' },
    { name: 'termination_mechanism', domainCode: 'D7', domain: 'Domain 7: Disposition & Ping-Pong', type: 'Enum', description: 'Specific procedural event terminating consideration (ENACTMENT, VOTE_DEFEAT, EXECUTIVE_WITHDRAWAL).' },

    // Domain 8
    { name: 'amendments_tabled_count', domainCode: 'D8', domain: 'Domain 8: Macro Amendments', type: 'Integer', description: 'Total count of formal amendments tabled across all stages.' },
    { name: 'amendments_agreed_count', domainCode: 'D8', domain: 'Domain 8: Macro Amendments', type: 'Integer', description: 'Total count of amendments formally adopted into the bill text.' },
    { name: 'committee_amendments_executive_acceptance_rate', domainCode: 'D8', domain: 'Domain 8: Macro Amendments', type: 'Float (0-1)', description: 'Proportion of non-executive committee amendments supported by government.' },

    // Domain 9: Micro Amendment Entity Records
    { name: 'canonical_amendment_id', domainCode: 'D9', domain: 'Domain 9: Micro Amendment Records', type: 'String (UUID/URN)', description: 'Unique persistent canonical amendment identifier (e.g. GB-SCT-S6-SPB13-AMD-042).' },
    { name: 'local_amendment_number', domainCode: 'D9', domain: 'Domain 9: Micro Amendment Records', type: 'String', description: 'Native marshaled amendment number (e.g. Amd 42, LOD 104).' },
    { name: 'sponsor_governance_role', domainCode: 'D9', domain: 'Domain 9: Micro Amendment Records', type: 'Enum', description: 'Amendment sponsor alignment (EXECUTIVE_MINISTER, GOVERNING_BACKBENCH, OPPOSITION_MEMBER, CROSS_PARTY).' },
    { name: 'amendment_action_type', domainCode: 'D9', domain: 'Domain 9: Micro Amendment Records', type: 'Enum', description: 'Proposed text alteration type (INSERTION, DELETION, SUBSTITUTION).' },
    { name: 'government_position', domainCode: 'D9', domain: 'Domain 9: Micro Amendment Records', type: 'Enum', description: 'Executive stance during debate (SUPPORTED, OPPOSED, NEUTRAL_NO_STANCE, MINISTERIAL_OWN_AMENDMENT).' },
    { name: 'disposition_canonical', domainCode: 'D9', domain: 'Domain 9: Micro Amendment Records', type: 'Enum', description: 'Final amendment disposition outcome (AGREED_TO, DEFEATED, WITHDRAWN, NOT_MOVED, FALLEN).' },
    { name: 'party_dissent_rate_on_amendment', domainCode: 'D9', domain: 'Domain 9: Micro Amendment Records', type: 'Float (0-1)', description: 'Proportion of governing party members rebelling against frontbench whip on this amendment division.' },

    // Domain 10: Committee Context & Roster Engine
    { name: 'committee_convener_member_id', domainCode: 'D10', domain: 'Domain 10: Committee Roster', type: 'String (Wikidata QID)', description: 'MSP ID of Committee Convener evaluated on date T.' },
    { name: 'committee_deputy_convener_member_id', domainCode: 'D10', domain: 'Domain 10: Committee Roster', type: 'String (Wikidata QID)', description: 'MSP ID of Deputy Convener evaluated on date T.' },
    { name: 'committee_membership_roster', domainCode: 'D10', domain: 'Domain 10: Committee Roster', type: 'Array of Objects', description: 'Complete array of MSP members assigned to committee from /api/PersonCommitteeRoles with active date bounds.' },

    // Domain 11: Parsed Proceedings & Official Report Analytics
    { name: 'official_report_proceedings_url', domainCode: 'D11', domain: 'Domain 11: Parsed Proceedings', type: 'URL', description: 'Official Report Hansard transcript URL for bill debate.' },
    { name: 'proceedings_total_word_count', domainCode: 'D11', domain: 'Domain 11: Parsed Proceedings', type: 'Integer', description: 'Total word count of debate proceedings for the bill.' },
    { name: 'proceedings_interventions_count', domainCode: 'D11', domain: 'Domain 11: Parsed Proceedings', type: 'Integer', description: 'Total recorded speech interventions during debate.' },
    { name: 'proceedings_msps_speaking_count', domainCode: 'D11', domain: 'Domain 11: Parsed Proceedings', type: 'Integer', description: 'Count of unique MSPs participating in debate.' },
    { name: 'executive_ministers_word_count_share', domainCode: 'D11', domain: 'Domain 11: Parsed Proceedings', type: 'Float (0-1)', description: 'Proportion of debate word count spoken by Executive Ministers.' }
  ];

  let filteredVariables = $derived(
    variables.filter(v => {
      const matchesDomain = selectedDomain === 'ALL' || v.domainCode === selectedDomain;
      const matchesSearch = searchQuery === '' || 
        v.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
        v.description.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesDomain && matchesSearch;
    })
  );
</script>

<svelte:head>
  <title>Master Canonical Variable Catalog — Comparative Legislative Data</title>
  <meta name="description" content="Master Wishlist Catalog defining target quantitative research variables across 11 legislative domains." />
  <script src="https://giscus.app/client.js"
        data-repo="comparative-legislative-data/comparative-legislative-data"
        data-category="General"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="transparent_dark"
        data-lang="en"
        crossorigin="anonymous"
        async>
  </script>
</svelte:head>

<div class="container py-8">
  <div class="page-header">
    <div class="header-badge">
      <Layers size={14} /> Wishlist Catalog v2.7.0 (Multi-Entity Architecture)
    </div>
    <h1>Master Canonical Variable Catalog</h1>
    <p class="lead">
      The universal target wishlist of quantitative variables sought by legislative scholars across 11 research domains, modeling <strong>CanonicalBill</strong>, <strong>CanonicalAmendment</strong>, <strong>CommitteeContext</strong>, and <strong>ParsedProceedings</strong> entities.
    </p>

    <!-- Provenance Architecture Clarification Banner -->
    <div class="info-banner">
      <div class="info-icon">
        <Info size={20} color="#38bdf8" />
      </div>
      <div class="info-text">
        <strong>Methodological Note on Data Provenance:</strong>
        This catalog defines the abstract target research variables. Provenance tiers (<code>NATIVE_DIRECT</code>, <code>DERIVED_DETERMINISTIC</code>, <code>DERIVED_HUMAN_CODED</code>, <code>UNAVAILABLE_HARD_GAP</code>, etc.) are <em>institution-specific</em> and evaluated per assembly and decision point within the <a href="/atlas" class="info-link"><Globe size={13} /> Parliament Data Atlas</a>.
      </div>
    </div>

    <!-- Search & Filter Controls -->
    <div class="controls-card">
      <div class="search-box">
        <Search size={18} class="search-icon" />
        <input 
          type="text" 
          placeholder="Search variables, descriptions, or data types..." 
          bind:value={searchQuery} 
        />
      </div>

      <div class="domain-tabs">
        {#each domains as domain}
          <button 
            class="domain-tab" 
            class:active={selectedDomain === domain.code}
            onclick={() => selectedDomain = domain.code}
          >
            {domain.name}
          </button>
        {/each}
      </div>
    </div>
  </div>

  <!-- Results Stats -->
  <div class="results-meta">
    Showing <strong>{filteredVariables.length}</strong> of <strong>{variables.length}</strong> canonical target variables
  </div>

  <!-- Variables Grid -->
  <div class="variables-grid">
    {#each filteredVariables as varDef}
      <div class="var-card">
        <div class="var-header">
          <code class="var-name">{varDef.name}</code>
          <span class="var-type">{varDef.type}</span>
        </div>

        <div class="var-domain">{varDef.domain}</div>
        <p class="var-desc">{varDef.description}</p>

        {#if varDef.notes}
          <div class="var-notes">
            <Tag size={12} /> {varDef.notes}
          </div>
        {/if}

        <!-- Per-Variable Action Buttons -->
        <div class="var-actions">
          <a 
            href={`https://github.com/comparative-legislative-data/comparative-legislative-data/discussions/new?category=general&title=Feedback+on+variable+${varDef.name}`} 
            target="_blank" 
            rel="noopener noreferrer" 
            class="action-btn btn-github"
          >
            <MessageSquare size={13} /> Discuss on GitHub
          </a>
          <a 
            href={`mailto:comparativelegislativedata@gmail.com?subject=Feedback on Variable: ${varDef.name}`} 
            class="action-btn btn-email"
          >
            <Mail size={13} /> Email Feedback
          </a>
        </div>
      </div>
    {/each}
  </div>

  <!-- Embedded GitHub Comment Section -->
  <section class="card comment-section mt-12">
    <h2 class="section-title"><MessageSquare size={20} color="#38bdf8" /> General Methodological Feedback & Comments</h2>
    <p class="mb-4 text-muted">
      Leave questions, proposals for new quantitative variables, or suggestions for definition adjustments. Comments automatically sync to our GitHub Organization Discussions.
    </p>
    <div class="giscus"></div>
  </section>
</div>

<style>
  .py-8 { padding-top: 2rem; padding-bottom: 4rem; }
  .mt-12 { margin-top: 3rem; }
  
  .page-header { margin-bottom: 2rem; }

  .header-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(99, 102, 241, 0.1);
    color: var(--accent-indigo);
    border: 1px solid rgba(99, 102, 241, 0.2);
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    margin-bottom: 1rem;
  }

  h1 {
    font-family: var(--font-heading);
    font-size: 2.25rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.75rem;
  }

  .lead {
    font-size: 1.05rem;
    color: var(--text-muted);
    max-width: 52rem;
    line-height: 1.6;
    margin-bottom: 1.5rem;
  }

  .info-banner {
    background: rgba(56, 189, 248, 0.08);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 0.65rem;
    padding: 1rem 1.25rem;
    display: flex;
    gap: 0.85rem;
    align-items: flex-start;
    margin-bottom: 1.5rem;
  }

  .info-icon {
    margin-top: 0.15rem;
  }

  .info-text {
    font-size: 0.875rem;
    color: var(--text-main);
    line-height: 1.5;
  }

  .info-link {
    color: var(--accent-cyan);
    text-decoration: none;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
  }
  .info-link:hover { text-decoration: underline; }

  .controls-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: 0.75rem;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .search-box {
    position: relative;
    display: flex;
    align-items: center;
  }

  .search-box input {
    width: 100%;
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid var(--border-subtle);
    border-radius: 0.5rem;
    padding: 0.75rem 1rem 0.75rem 2.75rem;
    color: #ffffff;
    font-size: 0.95rem;
    outline: none;
    transition: border-color 0.2s ease;
  }
  .search-box input:focus {
    border-color: var(--accent-indigo);
  }

  :global(.search-icon) {
    position: absolute;
    left: 0.85rem;
    color: var(--text-muted);
  }

  .domain-tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .domain-tab {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border-subtle);
    color: var(--text-muted);
    font-size: 0.8rem;
    font-weight: 500;
    padding: 0.35rem 0.75rem;
    border-radius: 0.375rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .domain-tab:hover {
    background: rgba(255, 255, 255, 0.08);
    color: var(--text-main);
  }
  .domain-tab.active {
    background: rgba(99, 102, 241, 0.15);
    border-color: var(--accent-indigo);
    color: #ffffff;
    font-weight: 600;
  }

  .results-meta {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-bottom: 1.25rem;
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
    transition: transform 0.2s ease, border-color 0.2s ease;
  }
  .var-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99, 102, 241, 0.4);
  }

  .var-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .var-name {
    font-family: var(--font-mono);
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--accent-cyan);
    background: rgba(56, 189, 248, 0.1);
    padding: 0.15rem 0.45rem;
    border-radius: 0.25rem;
    word-break: break-all;
  }

  .var-type {
    font-size: 0.725rem;
    color: var(--text-dim);
    font-family: var(--font-mono);
  }

  .var-domain {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--accent-purple);
    margin-bottom: 0.5rem;
  }

  .var-desc {
    font-size: 0.875rem;
    color: var(--text-muted);
    line-height: 1.5;
  }

  .var-notes {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.75rem;
    color: var(--accent-gold);
    background: rgba(234, 179, 8, 0.1);
    padding: 0.35rem 0.5rem;
    border-radius: 0.25rem;
    margin-top: 0.75rem;
  }

  .var-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
  }

  .action-btn {
    flex: 1;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.35rem;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.35rem 0.5rem;
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

  .comment-section {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: 0.75rem;
    padding: 1.75rem;
  }

  .section-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: var(--font-heading);
    font-size: 1.25rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.5rem;
  }

  .text-muted { color: var(--text-muted); font-size: 0.9rem; }

  .giscus {
    margin-top: 1rem;
    min-height: 150px;
  }
</style>
