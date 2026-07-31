<script lang="ts">
  import { X, Copy, Check, Terminal, ExternalLink, Play } from 'lucide-svelte';
  
  const UNCOMPRESSED_ENDPOINTS = ["bills"];

  let { isOpen = $bindable(false), endpoint } = $props();

  let activeTab = $state('schema'); // 'schema', 'preview', 'snippets'
  let loading = $state(false);
  let error = $state<string | null>(null);
  let rawData = $state<any>(null);
  
  // Custom query parameters edited by the user
  let queryParams = $state('');

  // Hashed state to show "Copied" message
  let copiedText = $state<string | null>(null);

  // Derived request URL for snippets and links
  let requestUrl = $derived.by(() => {
    if (!endpoint) return '';
    const host = typeof window !== 'undefined' ? window.location.origin : 'http://legislativedata.org';
    return `${host}/api/v2/canonical/gb-sct/${endpoint.path}${queryParams}`;
  });

  // Derived state to check if endpoint CSV should be uncompressed (the 500-row rule)
  let isUncompressed = $derived(endpoint ? UNCOMPRESSED_ENDPOINTS.includes(endpoint.path) : false);
  let csvExt = $derived(isUncompressed ? 'csv' : 'csv.gz');

  $effect(() => {
    if (isOpen && endpoint) {
      activeTab = 'schema';
      error = null;
      rawData = null;
      queryParams = endpoint.params || '';
      triggerFetch();
    }
  });

  async function triggerFetch() {
    if (!endpoint) return;
    loading = true;
    error = null;
    rawData = null;

    try {
      const pathWithParams = endpoint.path + (queryParams ? queryParams : '');
      const fetchUrl = `/api/v2/canonical/gb-sct/${pathWithParams}`;
      
      const res = await fetch(fetchUrl);
      if (!res.ok) {
        throw new Error(`HTTP Error ${res.status}: Failed to fetch canonical dataset.`);
      }
      
      const data = await res.json();
      rawData = data;
    } catch (e: any) {
      error = e.message || 'Unknown fetch failure';
    } finally {
      loading = false;
    }
  }

  // Schema introspector to document fields
  function introspectSchema(obj: any): Array<{ path: string; type: string }> {
    if (!obj) return [];
    if (Array.isArray(obj)) {
      if (obj.length === 0) return [];
      return introspectSchema(obj[0]);
    }
    if (typeof obj === 'object') {
      return Object.entries(obj).map(([key, value]) => {
        let type = 'String';
        if (typeof value === 'number') {
          type = Number.isInteger(value) ? 'Integer' : 'Float';
        } else if (typeof value === 'boolean') {
          type = 'Boolean';
        } else if (value === null) {
          type = 'Nullable';
        }
        return { path: key, type };
      });
    }
    return [];
  }

  let schemaFields = $derived(rawData ? introspectSchema(rawData) : []);

  function copySnippet(text: string, id: string) {
    navigator.clipboard.writeText(text);
    copiedText = id;
    setTimeout(() => {
      if (copiedText === id) copiedText = null;
    }, 2000);
  }

  // Snippets definition matching the OData specs for R, Python, and cURL
  let pythonSnippet = $derived(() => {
    return `import requests\n\nurl = "${requestUrl}"\nresponse = requests.get(url)\ndata = response.json()\nprint(data[:2])`;
  });

  let rSnippet = $derived(() => {
    return `library(httr)\nlibrary(jsonlite)\n\nurl <- "${requestUrl}"\nres <- GET(url)\ndata <- fromJSON(rawToChar(res$content))\nhead(data)`;
  });

  let curlSnippet = $derived(() => {
    return `curl -i "${requestUrl}"`;
  });

  const cb = '}';
</script>

{#if isOpen && endpoint}
  <!-- Backdrop -->
  <div class="modal-backdrop" onclick={() => isOpen = false} role="presentation"></div>

  <!-- Modal Window -->
  <div class="modal-window">
    <header class="modal-header">
      <div class="modal-title-col">
        <div class="modal-badge">DATABASE_CANONICAL (OPTIMIZED)</div>
        <h2>{endpoint.name}</h2>
        <code class="modal-path">GET /api/v2/canonical/gb-sct/{endpoint.path}</code>
      </div>
      <button class="btn-close" onclick={() => isOpen = false} aria-label="Close modal">
        <X size={20} />
      </button>
    </header>

    <!-- Query Editor Panel -->
    <section class="query-panel">
      <div class="query-input-row">
        <span class="query-label">API Data Source:</span>
        <div class="source-info">
          PostgreSQL Database B (Isolated Research Layer)
        </div>
      </div>
      
      <div class="query-input-row downloads-row">
        <div class="bulk-downloads-row">
          <span class="bulk-download-title">Bulk Downloads:</span>
          <a 
            href="/downloads/gb-sct/canonical_{endpoint.path}.{csvExt}?v=2" 
            download 
            class="btn-bulk-download"
            title={isUncompressed ? "Download complete canonical table as plain CSV" : "Download complete canonical table as compressed CSV.GZ"}
          >
            CSV{isUncompressed ? '' : '.GZ'}
          </a>
          <a 
            href="/downloads/gb-sct/canonical_{endpoint.path}.parquet?v=2" 
            download 
            class="btn-bulk-download btn-parquet"
            title="Download complete canonical table as snappy-compressed Parquet"
          >
            Parquet
          </a>
          <a 
            href="/downloads/gb-sct/gb_sct_canonical.sqlite.gz?v=2" 
            download 
            class="btn-bulk-download btn-sqlite"
            title="Download entire research database as compressed SQLite.GZ"
          >
            Canonical SQLite DB
          </a>
        </div>
        <div class="decompression-help">
          💡 CSV and Parquet downloads represent this table specifically. The Canonical SQLite DB contains all research datasets.
        </div>
      </div>

      <div class="query-input-row mt-2">
        <span class="query-label">Edit Query Parameters:</span>
        <input 
          type="text" 
          class="query-input" 
          bind:value={queryParams} 
          placeholder="e.g. ?$top=5 or ?$filter=BillOutcome eq 'PASSED'"
        />
        <button class="btn-run" onclick={triggerFetch} disabled={loading}>
          <Play size={12} fill="currentColor" /> Run Query
        </button>
      </div>
      <span class="text-xs text-slate-400">
        Live API Endpoint: 
        <a 
          href={requestUrl} 
          target="_blank" 
          rel="noopener noreferrer" 
          class="external-link"
        >
          {requestUrl} <ExternalLink size={10} />
        </a>
      </span>
    </section>

    <!-- Tabs Navigation -->
    <nav class="tabs-nav">
      <button 
        class="tab-btn" 
        class:active={activeTab === 'schema'} 
        onclick={() => activeTab = 'schema'}
      >
        Table Schema
      </button>
      <button 
        class="tab-btn" 
        class:active={activeTab === 'preview'} 
        onclick={() => activeTab = 'preview'}
      >
        Data Preview ({rawData ? Array.isArray(rawData) ? rawData.length : 1 : 0} rows)
      </button>
      <button 
        class="tab-btn" 
        class:active={activeTab === 'snippets'} 
        onclick={() => activeTab = 'snippets'}
      >
        Code Snippets
      </button>
    </nav>

    <!-- Tab Contents -->
    <div class="modal-body">
      {#if activeTab === 'schema'}
        <div class="tab-content">
          {#if loading}
            <div class="loading-state">
              <div class="spinner"></div>
              <span>Introspecting schema...</span>
            </div>
          {:else if error}
            <div class="error-box">
              ⚠️ Failed to resolve schema. Error: {error}
            </div>
          {:else if schemaFields.length > 0}
            <table class="schema-table">
              <thead>
                <tr>
                  <th>Field Name (CamelCase)</th>
                  <th>Database Type</th>
                </tr>
              </thead>
              <tbody>
                {#each schemaFields as field}
                  <tr>
                    <td><code>{field.path}</code></td>
                    <td><span class="type-badge">{field.type}</span></td>
                  </tr>
                {/each}
              </tbody>
            </table>
          {:else}
            <div class="empty-state">No schema descriptors found. Run query to load schema.</div>
          {/if}
        </div>
      {:else if activeTab === 'preview'}
        <div class="tab-content">
          {#if loading}
            <div class="loading-state">
              <div class="spinner"></div>
              <span>Streaming query rows...</span>
            </div>
          {:else if error}
            <div class="error-box">
              ⚠️ Database Query Failed: {error}
            </div>
          {:else if rawData}
            <div class="preview-json">
              <pre><code>{JSON.stringify(rawData, null, 2)}</code></pre>
            </div>
          {:else}
            <div class="empty-state">No data loaded.</div>
          {/if}
        </div>
      {:else if activeTab === 'snippets'}
        <div class="tab-content snippets-content">
          <!-- Python -->
          <div class="snippet-block">
            <div class="snippet-header">
              <span>Python (requests)</span>
              <button class="btn-copy" onclick={() => copySnippet(pythonSnippet(), 'py')}>
                {copiedText === 'py' ? 'Copied!' : 'Copy Code'}
              </button>
            </div>
            <pre><code>{pythonSnippet()}</code></pre>
          </div>

          <!-- R -->
          <div class="snippet-block">
            <div class="snippet-header">
              <span>R (httr / jsonlite)</span>
              <button class="btn-copy" onclick={() => copySnippet(rSnippet(), 'r')}>
                {copiedText === 'r' ? 'Copied!' : 'Copy Code'}
              </button>
            </div>
            <pre><code>{rSnippet()}</code></pre>
          </div>

          <!-- cURL -->
          <div class="snippet-block">
            <div class="snippet-header">
              <span>Shell (cURL)</span>
              <button class="btn-copy" onclick={() => copySnippet(curlSnippet(), 'curl')}>
                {copiedText === 'curl' ? 'Copied!' : 'Copy Code'}
              </button>
            </div>
            <pre><code>{curlSnippet()}</code></pre>
          </div>
        </div>
      {/if}
    </div>
  </div>
{/if}

<style>
  /* Backdrop */
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(4, 6, 10, 0.85);
    backdrop-filter: blur(8px);
    z-index: 1000;
  }

  /* Modal Window */
  .modal-window {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 95%;
    max-width: 800px;
    height: 85vh;
    background: #090d16;
    border: 1px solid rgba(16, 185, 129, 0.2);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 50px rgba(16, 185, 129, 0.1);
    border-radius: 1.25rem;
    display: flex;
    flex-direction: column;
    z-index: 1001;
    overflow: hidden;
  }

  .modal-header {
    padding: 1.5rem 2rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }

  .modal-title-col {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    text-align: left;
  }

  .modal-badge {
    align-self: flex-start;
    padding: 0.2rem 0.65rem;
    background: rgba(16, 185, 129, 0.12);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 9999px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .modal-header h2 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.025em;
  }

  .modal-path {
    font-family: monospace;
    font-size: 0.8rem;
    color: #94a3b8;
    background: rgba(255,255,255,0.03);
    padding: 0.15rem 0.5rem;
    border-radius: 0.25rem;
    width: fit-content;
  }

  .btn-close {
    background: transparent;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    padding: 0.35rem;
    border-radius: 0.5rem;
    transition: all 0.2s ease;
  }
  .btn-close:hover {
    color: #ffffff;
    background: rgba(255,255,255,0.05);
  }

  /* Query Editor Panel */
  .query-panel {
    background: rgba(15, 23, 42, 0.4);
    padding: 1.25rem 2rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
    text-align: left;
  }

  .query-input-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .query-label {
    font-size: 0.85rem;
    font-weight: 700;
    color: #94a3b8;
    min-width: 150px;
  }

  .source-info {
    font-size: 0.85rem;
    color: #10b981;
    font-weight: 600;
  }

  .query-input {
    flex: 1;
    min-width: 250px;
    background: #020617;
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #f1f5f9;
    padding: 0.5rem 0.85rem;
    border-radius: 0.5rem;
    font-family: monospace;
    font-size: 0.85rem;
  }
  .query-input:focus {
    outline: none;
    border-color: rgba(16, 185, 129, 0.4);
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.1);
  }

  .btn-run {
    background: #10b981;
    color: #040815;
    border: none;
    padding: 0.5rem 1.25rem;
    border-radius: 0.5rem;
    font-size: 0.85rem;
    font-weight: 700;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    transition: all 0.2s ease;
  }
  .btn-run:hover:not(:disabled) {
    background: #059669;
    transform: translateY(-1px);
  }

  .external-link {
    color: #10b981;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
  }
  .external-link:hover {
    text-decoration: underline;
  }

  /* Bulk Downloads Styling */
  .downloads-row {
    border-top: 1px solid rgba(255, 255, 255, 0.03);
    padding-top: 0.85rem;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  .bulk-downloads-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
  }
  .bulk-download-title {
    font-size: 0.85rem;
    font-weight: 700;
    color: #94a3b8;
    margin-right: 0.5rem;
  }
  .btn-bulk-download {
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    text-decoration: none;
    transition: all 0.2s ease;
    border: 1px solid #10b981;
    background: rgba(16, 185, 129, 0.08);
    color: #10b981;
  }
  .btn-bulk-download:hover {
    background: #10b981;
    color: #020617;
  }
  .btn-parquet {
    border-color: #38bdf8;
    background: rgba(56, 189, 248, 0.08);
    color: #38bdf8;
  }
  .btn-parquet:hover {
    background: #38bdf8;
    color: #020617;
  }
  .btn-sqlite {
    border-color: #a78bfa;
    background: rgba(167, 139, 250, 0.08);
    color: #a78bfa;
  }
  .btn-sqlite:hover {
    background: #a78bfa;
    color: #020617;
  }
  .decompression-help {
    font-size: 0.7rem;
    color: #64748b;
  }

  /* Tabs Nav */
  .tabs-nav {
    background: rgba(255, 255, 255, 0.01);
    display: flex;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    padding: 0 2rem;
  }
  .tab-btn {
    padding: 1rem 1.5rem;
    background: transparent;
    border: none;
    color: #64748b;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    border-bottom: 2px solid transparent;
    transition: all 0.2s ease;
  }
  .tab-btn:hover {
    color: #ffffff;
  }
  .tab-btn.active {
    color: #10b981;
    border-bottom-color: #10b981;
  }

  /* Body Content */
  .modal-body {
    flex: 1;
    overflow-y: auto;
    padding: 2rem;
  }
  .tab-content {
    height: 100%;
  }

  /* Schema Table */
  .schema-table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
  }
  .schema-table th, .schema-table td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  }
  .schema-table th {
    font-size: 0.8rem;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .schema-table td {
    font-size: 0.875rem;
    color: #f1f5f9;
  }
  .schema-table code {
    color: #38bdf8;
  }
  .type-badge {
    padding: 0.15rem 0.5rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 0.25rem;
    font-size: 0.75rem;
    color: #94a3b8;
  }

  /* Preview Json */
  .preview-json {
    background: #020617;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 0.75rem;
    padding: 1.25rem;
    max-height: 100%;
    overflow-y: auto;
    text-align: left;
  }
  .preview-json pre {
    margin: 0;
    font-family: monospace;
    font-size: 0.85rem;
    color: #f1f5f9;
  }

  /* Code Snippets */
  .snippets-content {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    text-align: left;
  }
  .snippet-block {
    background: #020617;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 0.75rem;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  .snippet-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #94a3b8;
    font-size: 0.8rem;
    font-weight: 700;
  }
  .btn-copy {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    color: #e2e8f0;
    padding: 0.25rem 0.75rem;
    border-radius: 0.35rem;
    font-size: 0.7rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .btn-copy:hover {
    background: rgba(16, 185, 129, 0.1);
    border-color: #10b981;
    color: #10b981;
  }
  .snippet-block pre {
    margin: 0;
    font-family: monospace;
    font-size: 0.8rem;
    color: #34d399;
    overflow-x: auto;
  }

  /* Common States */
  .loading-state {
    height: 200px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 0.75rem;
    color: #64748b;
    font-size: 0.875rem;
  }
  .spinner {
    width: 24px;
    height: 24px;
    border: 2px solid rgba(16, 185, 129, 0.1);
    border-top-color: #10b981;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .error-box {
    padding: 1.5rem;
    background: rgba(239, 68, 68, 0.05);
    border: 1px solid rgba(239, 68, 68, 0.15);
    color: #f87171;
    border-radius: 0.5rem;
    font-size: 0.875rem;
  }

  .empty-state {
    padding: 3rem;
    color: #64748b;
    font-size: 0.875rem;
  }

  .text-xs { font-size: 0.75rem; }
  .text-slate-400 { color: #94a3b8; }
  .mt-2 { margin-top: 0.5rem; }
  .mt-3 { margin-top: 0.75rem; }
</style>
