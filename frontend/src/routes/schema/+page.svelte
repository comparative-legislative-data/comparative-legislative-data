<script lang="ts">
  import { Layers, Search, Filter, ShieldCheck, Database, Code, CheckCircle, Tag } from 'lucide-svelte';

  let searchQuery = $state('');
  let selectedDomain = $state('ALL');

  interface VariableDef {
    name: string;
    domain: string;
    domainCode: string;
    type: string;
    primaryTier: string;
    description: string;
    notes?: string;
  }

  const domains = [
    { code: 'ALL', name: 'All 8 Research Domains' },
    { code: 'D1', name: 'Domain 1: Assembly, Electoral & Executive Context' },
    { code: 'D2', name: 'Domain 2: Bill Identification, Sponsorship & Temporal Origin' },
    { code: 'D3', name: 'Domain 3: Progression, Timelines & Procedural Control' },
    { code: 'D4', name: 'Domain 4: Final Disposition & Inter-Chamber Mechanisms' },
    { code: 'D5', name: 'Domain 5: Bill Documentation & Impact Papers' },
    { code: 'D6', name: 'Domain 6: Committee Scrutiny & Evidence' },
    { code: 'D7', name: 'Domain 7: Decision-Point Amendments & Text Alteration' },
    { code: 'D8', name: 'Domain 8: Temporal Divisions & Voting Coalitions' }
  ];

  const variables: VariableDef[] = [
    // Domain 1
    { name: 'jurisdiction_code', domainCode: 'D1', domain: 'Domain 1: Assembly & Executive', type: 'String (ISO 3166-2)', primaryTier: 'NATIVE_DIRECT', description: 'Unique assembly identifier (e.g. GB-UKP, GB-SCT, DE-BT, US-HR).' },
    { name: 'parliament_term', domainCode: 'D1', domain: 'Domain 1: Assembly & Executive', type: 'String', primaryTier: 'NATIVE_DIRECT', description: 'Macro electoral legislative period (e.g. Session 6, 58th Parliament).' },
    { name: 'chamber_type', domainCode: 'D1', domain: 'Domain 1: Assembly & Executive', type: 'Enum', primaryTier: 'DERIVED_DETERMINISTIC', description: 'Constitutional chamber structure (SOVEREIGN_BICAMERAL, DEVOLVED_UNICAMERAL, FEDERAL_UPPER, etc).' },
    { name: 'government_type', domainCode: 'D1', domain: 'Domain 1: Assembly & Executive', type: 'Enum', primaryTier: 'LINKED_EXTERNAL_AUTHORITY', description: 'Executive arrangement typology (SINGLE_PARTY_MAJORITY, SINGLE_PARTY_MINORITY, FORMAL_COALITION, COOPERATION_AGREEMENT).', notes: 'Mapped to ParlGov database.' },
    { name: 'parlgov_cabinet_id', domainCode: 'D1', domain: 'Domain 1: Assembly & Executive', type: 'String', primaryTier: 'LINKED_EXTERNAL_AUTHORITY', description: 'Canonical cabinet identifier linked from ParlGov.' },

    // Domain 2
    { name: 'local_bill_id', domainCode: 'D2', domain: 'Domain 2: Sponsorship & Origin', type: 'String', primaryTier: 'NATIVE_DIRECT', description: 'Native reference code assigned by host legislature (e.g. SP Bill 13, H.R. 815).' },
    { name: 'title_canonical', domainCode: 'D2', domain: 'Domain 2: Sponsorship & Origin', type: 'String', primaryTier: 'NATIVE_DIRECT', description: 'Standardized English short title.' },
    { name: 'initiator_type', domainCode: 'D2', domain: 'Domain 2: Sponsorship & Origin', type: 'Enum', primaryTier: 'DERIVED_DETERMINISTIC', description: 'Globally neutral sponsor type (EXECUTIVE, INDIVIDUAL_MEMBER, GROUP_MEMBERS, COMMITTEE).' },
    { name: 'initiator_party_governance_role', domainCode: 'D2', domain: 'Domain 2: Sponsorship & Origin', type: 'Enum', primaryTier: 'DERIVED_DETERMINISTIC', description: 'Primary sponsor alignment (GOVERNING_PARTY, OPPOSITION_PARTY, CROSS_PARTY) evaluated on introduction date.' },
    { name: 'initiator_member_id', domainCode: 'D2', domain: 'Domain 2: Sponsorship & Origin', type: 'String (Wikidata QID)', primaryTier: 'LINKED_EXTERNAL_AUTHORITY', description: 'Disambiguated persistent identifier for primary sponsor MP/MSP.' },

    // Domain 3
    { name: 'date_introduced', domainCode: 'D3', domain: 'Domain 3: Progression & Control', type: 'Date (ISO 8601)', primaryTier: 'NATIVE_DIRECT', description: 'Formal introduction date of the bill.' },
    { name: 'date_final_outcome', domainCode: 'D3', domain: 'Domain 3: Progression & Control', type: 'Date (ISO 8601)', primaryTier: 'NATIVE_DIRECT', description: 'Date of final passage, defeat, or withdrawal.' },
    { name: 'duration_calendar_days', domainCode: 'D3', domain: 'Domain 3: Progression & Control', type: 'Integer', primaryTier: 'DERIVED_DETERMINISTIC', description: 'Calendar days elapsed from introduction to final outcome.' },
    { name: 'duration_sitting_days', domainCode: 'D3', domain: 'Domain 3: Progression & Control', type: 'Integer', primaryTier: 'DERIVED_DETERMINISTIC', description: 'Formal parliamentary sitting days elapsed.' },
    { name: 'programme_motion_flag', domainCode: 'D3', domain: 'Domain 3: Progression & Control', type: 'Boolean', primaryTier: 'DERIVED_DETERMINISTIC', description: 'Indicates whether a formal timetabling or programme motion was imposed.' },
    { name: 'guillotine_invoked_flag', domainCode: 'D3', domain: 'Domain 3: Progression & Control', type: 'Boolean', primaryTier: 'DERIVED_DETERMINISTIC', description: 'Indicates whether a debate closure or guillotine motion was invoked.' },
    { name: 'emergency_procedure_flag', domainCode: 'D3', domain: 'Domain 3: Progression & Control', type: 'Boolean', primaryTier: 'NATIVE_DIRECT', description: 'Indicates whether the bill passed under fast-track or urgency procedures.' },
    { name: 'prior_executive_consent_required_flag', domainCode: 'D3', domain: 'Domain 3: Progression & Control', type: 'Boolean', primaryTier: 'DERIVED_HUMAN_CODED', description: 'Indicates whether prior executive or Crown consent was required.' },

    // Domain 4
    { name: 'final_status', domainCode: 'D4', domain: 'Domain 4: Disposition & Ping-Pong', type: 'Enum', primaryTier: 'NATIVE_DIRECT', description: 'Terminal procedural status (ENACTED, DEFEATED, WITHDRAWN, LAPSED, PENDING, VETOED).' },
    { name: 'termination_mechanism', domainCode: 'D4', domain: 'Domain 4: Disposition & Ping-Pong', type: 'Enum', primaryTier: 'DERIVED_DETERMINISTIC', description: 'Specific procedural event terminating consideration (ENACTMENT, VOTE_DEFEAT, EXECUTIVE_WITHDRAWAL).' },
    { name: 'head_of_state_promulgation_date', domainCode: 'D4', domain: 'Domain 4: Disposition & Ping-Pong', type: 'Date (ISO 8601)', primaryTier: 'NATIVE_DIRECT', description: 'Date of Royal Assent, Presidential Signature, or Promulgation. (Alias: royal_assent_date).' },
    { name: 'chamber_ping_pong_count', domainCode: 'D4', domain: 'Domain 4: Disposition & Ping-Pong', type: 'Integer', primaryTier: 'DERIVED_DETERMINISTIC', description: 'For bicameral systems: number of amendment exchanges between chambers.' },

    // Domain 5
    { name: 'doc_as_introduced_url', domainCode: 'D5', domain: 'Domain 5: Documentation & Impact', type: 'URL', primaryTier: 'NATIVE_DIRECT', description: 'Official text of the Bill as introduced.' },
    { name: 'doc_as_passed_url', domainCode: 'D5', domain: 'Domain 5: Documentation & Impact', type: 'URL', primaryTier: 'NATIVE_DIRECT', description: 'Official text of the Bill as enacted or passed.' },
    { name: 'cap_topic_code', domainCode: 'D5', domain: 'Domain 5: Documentation & Impact', type: 'String', primaryTier: 'LINKED_EXTERNAL_AUTHORITY', description: 'Policy topic code mapped to Comparative Agendas Project taxonomy.' },
    { name: 'fiscal_impact_flag', domainCode: 'D5', domain: 'Domain 5: Documentation & Impact', type: 'Boolean', primaryTier: 'DERIVED_SYNTHETIC_AI', description: 'Flag indicating binding fiscal expenditure or taxation impact.', notes: 'Carries AI Validation Lifecycle badge.' },

    // Domain 6
    { name: 'lead_committee_name', domainCode: 'D6', domain: 'Domain 6: Committee Scrutiny', type: 'String', primaryTier: 'NATIVE_DIRECT', description: 'Name of the primary scrutinising committee assigned.' },
    { name: 'committee_evidence_submissions_count', domainCode: 'D6', domain: 'Domain 6: Committee Scrutiny', type: 'Integer', primaryTier: 'NATIVE_DIRECT', description: 'Total published written evidence submissions received.' },

    // Domain 7
    { name: 'amendments_tabled_count', domainCode: 'D7', domain: 'Domain 7: Amendments & Alteration', type: 'Integer', primaryTier: 'NATIVE_DIRECT', description: 'Total count of formal amendments tabled across all stages.' },
    { name: 'amendments_agreed_count', domainCode: 'D7', domain: 'Domain 7: Amendments & Alteration', type: 'Integer', primaryTier: 'NATIVE_DIRECT', description: 'Total count of amendments formally adopted into the bill text.' },
    { name: 'amendments_non_executive_count', domainCode: 'D7', domain: 'Domain 7: Amendments & Alteration', type: 'Integer', primaryTier: 'DERIVED_DETERMINISTIC', description: 'Count of amendments tabled by non-executive members evaluated on tabling date.' },
    { name: 'committee_amendments_executive_acceptance_rate', domainCode: 'D7', domain: 'Domain 7: Amendments & Alteration', type: 'Float (0-1)', primaryTier: 'DERIVED_HUMAN_CODED', description: 'Proportion of non-executive committee amendments supported by government.', notes: 'PhD Dissertation Dataset.' },
    { name: 'bill_text_alteration_score', domainCode: 'D7', domain: 'Domain 7: Amendments & Alteration', type: 'Float (0-1)', primaryTier: 'DERIVED_SYNTHETIC_AI', description: 'Similarity metric comparing introduced vs enacted text.' },

    // Domain 8
    { name: 'divisions_count', domainCode: 'D8', domain: 'Domain 8: Divisions & Coalitions', type: 'Integer', primaryTier: 'NATIVE_DIRECT', description: 'Total recorded roll-call division votes held on the bill.' },
    { name: 'effective_majority_margin_at_event_date', domainCode: 'D8', domain: 'Domain 8: Divisions & Coalitions', type: 'Integer', primaryTier: 'DERIVED_DETERMINISTIC', description: 'Mathematical floor majority margin (Governing Seats - Opposition Seats) on vote date.' },
    { name: 'voting_coalition_type', domainCode: 'D8', domain: 'Domain 8: Divisions & Coalitions', type: 'Enum', primaryTier: 'DERIVED_DETERMINISTIC', description: 'Voting alignment classification (UNANIMOUS, GOVERNMENT_PARTY_LINE, CROSS_PARTY_MAJORITY) evaluated on vote date.' }
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
  <meta name="description" content="Master Wishlist Catalog defining ~40 target quantitative research variables across 8 legislative domains." />
</svelte:head>

<div class="container py-8">
  <div class="page-header">
    <div class="header-badge">
      <Layers size={14} /> Wishlist Catalog v2.3.0
    </div>
    <h1>Master Canonical Variable Catalog</h1>
    <p class="lead">
      The universal target wishlist of quantitative variables sought by legislative scholars across 8 research domains. 
      Variable values are instantiated and evaluated per assembly and per decision point against our 6-tier provenance spectrum.
    </p>

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

        <div class="var-footer">
          <span class="provenance-tag tier-{varDef.primaryTier.toLowerCase()}">
            {varDef.primaryTier}
          </span>
        </div>
      </div>
    {/each}
  </div>
</div>

<style>
  .py-8 { padding-top: 2rem; padding-bottom: 4rem; }
  
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
    justify-content: space-between;
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
    margin-bottom: 0.75rem;
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
    margin-bottom: 0.75rem;
  }

  .var-footer {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    margin-top: auto;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
  }

  .provenance-tag {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    padding: 0.2rem 0.5rem;
    border-radius: 0.25rem;
  }

  .tier-native_direct { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
  .tier-derived_deterministic { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
  .tier-derived_human_coded { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
  .tier-derived_synthetic_ai { background: rgba(234, 179, 8, 0.15); color: #facc15; border: 1px solid rgba(234, 179, 8, 0.3); }
  .tier-linked_external_authority { background: rgba(99, 102, 241, 0.15); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.3); }
</style>
