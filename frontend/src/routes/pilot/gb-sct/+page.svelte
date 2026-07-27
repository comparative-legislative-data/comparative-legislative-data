<script lang="ts">
  import { ShieldCheck, Database, ArrowRight, ExternalLink, HelpCircle, AlertTriangle, ChevronDown, ChevronUp } from 'lucide-svelte';
  import NativeEndpointModal from '$lib/components/NativeEndpointModal.svelte';

  let isModalOpen = $state(false);
  let selectedEndpoint = $state<any>(null);

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

  let expandedHubs = $state<Record<string, boolean>>({
    'bills': false,
    'committees': false,
    'motions': false
  });

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
</script>

<svelte:head>
  <title>Native API Explorer | Scottish Parliament (GB-SCT)</title>
  <meta name="description" content="Academic explorer mapping raw Scottish Parliament OData endpoints into relational hubs with dynamic schema audits." />
</svelte:head>

<div class="explorer-container">
  <div class="container py-12">
    
    <!-- Header Section -->
    <div class="header-section text-center mb-12">
      <div class="badge-row mb-4">
        <span class="badge badge-pilot">Pilot Phase: GB-SCT</span>
        <span class="badge badge-transparent"><ShieldCheck size={12} /> 100% Raw Passthrough</span>
      </div>
      <h1 class="page-title">Native API Explorer</h1>
      <h2 class="page-subtitle text-indigo-400">Scottish Parliament (data.parliament.scot)</h2>
      
      <div class="description-box mt-6 mx-auto">
        <p>
          This explorer provides <strong>academic transparency</strong> into the raw OData feeds served by the Scottish Parliament before any transformation. 
          By clicking on the endpoints below, our un-gated CORS proxy acts as a transparent relay to bypass browser restrictions.
        </p>
        <div class="alert-box mt-4">
          <div class="alert-icon"><AlertTriangle size={16} /></div>
          <div class="alert-content">
            <strong>OData Pagination Note:</strong> The dynamic audit verified that the host API ignores <code>$skip</code> on these resources. 
            Transcripts, motions, and votes must be queried by specific filters (like <code>?year=YYYY</code>) rather than standard skip offsets to prevent infinite retrieval loops.
          </div>
        </div>
      </div>
    </div>

    <!-- Entity Hubs Grid -->
    <div class="hubs-layout mt-12">
      {#each hubs as hub}
        {@const key = hubKeys[hub.title]}
        <section class="hub-card">
          <div class="hub-header-row">
            <div class="hub-header">
              <h2>{hub.title}</h2>
              <p class="hub-desc">{hub.description}</p>
            </div>
            <button class="btn-toggle" onclick={() => toggleHub(hub.title)}>
              {#if expandedHubs[key]}
                Hide Endpoints <ChevronUp size={16} />
              {:else}
                Show Endpoints <ChevronDown size={16} />
              {/if}
            </button>
          </div>

          {#if expandedHubs[key]}
            <div class="endpoints-list">
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
                      <span class="text-muted">Query Parameter Required:</span>
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

  </div>
</div>

<NativeEndpointModal bind:isOpen={isModalOpen} endpoint={selectedEndpoint} />

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

  .description-box {
    background: #0f172a;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 0.75rem;
    padding: 1.5rem;
    max-width: 850px;
    text-align: left;
  }

  .description-box p {
    color: #94a3b8;
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0;
  }

  .alert-box {
    background: rgba(245, 158, 11, 0.08);
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: 0.5rem;
    padding: 0.75rem 1rem;
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
  }

  .alert-icon {
    color: #f59e0b;
    margin-top: 0.15rem;
  }

  .alert-content {
    color: #d97706;
    font-size: 0.85rem;
    line-height: 1.5;
  }
  .alert-content code {
    background: rgba(0,0,0,0.3);
    padding: 0.1rem 0.3rem;
    border-radius: 0.25rem;
    color: #f59e0b;
  }

  .hubs-layout {
    display: flex;
    flex-direction: column;
    gap: 2.5rem;
  }

  .hub-card {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 0.85rem;
    padding: 2rem;
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
  }
  .btn-toggle:hover {
    background: rgba(99, 102, 241, 0.2);
    border-color: #818cf8;
    color: #ffffff;
  }

  .hub-header h2 {
    font-family: var(--font-heading);
    font-size: 1.5rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
  }

  .hub-desc {
    color: #64748b;
    font-size: 0.9rem;
    margin: 0.35rem 0 0 0;
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
    padding: 1.25rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    text-align: left;
    cursor: pointer;
    transition: all 0.2s ease;
    width: 100%;
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
    font-size: 1.05rem;
    font-weight: 700;
    color: #ffffff;
  }

  .endpoint-desc {
    color: #94a3b8;
    font-size: 0.85rem;
    margin: 0.35rem 0 0 0;
    max-width: 800px;
    line-height: 1.5;
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
</style>
