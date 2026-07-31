<script lang="ts">
  import { X, Copy, Check, Terminal, ExternalLink, Play } from 'lucide-svelte';
  
  const UNCOMPRESSED_ENDPOINTS = [
    "billtypes", "billstagetypes", "parties", "committeeroles", 
    "committeetypes", "bills", "members", "committees"
  ];

  let { isOpen = $bindable(false), endpoint } = $props();

  let apiSource = $state('mirror');

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
    if (endpoint.isCanonical) {
      return `${host}/api/v2/canonical/gb-sct/${endpoint.path}${queryParams}`;
    }
    const base = apiSource === 'mirror' ? `${host}/api/v2/mirror/gb-sct` : 'https://data.parliament.scot/api';
    return `${base}/${endpoint.path}${queryParams}`;
  });

  // Derived state to check if endpoint CSV should be uncompressed
  let isUncompressed = $derived(endpoint ? UNCOMPRESSED_ENDPOINTS.includes(endpoint.path) : false);
  let csvExt = $derived(isUncompressed ? 'csv' : 'csv.gz');

  $effect(() => {
    if (isOpen && endpoint) {
      activeTab = 'schema';
      error = null;
      rawData = null;
      apiSource = endpoint.isCanonical ? 'canonical' : 'mirror'; // Default to canonical or optimized mirror
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
      // Build the fetch URL using local mirror, proxy, or canonical base
      const pathWithParams = endpoint.path + (queryParams ? queryParams : '');
      let baseEndpoint = '/api/v2/mirror/gb-sct';
      if (endpoint.isCanonical) {
        baseEndpoint = '/api/v2/canonical/gb-sct';
      } else if (apiSource === 'proxy') {
        baseEndpoint = '/api/v2/proxy/gb-sct';
      }
      const fetchUrl = `${baseEndpoint}/${pathWithParams}`;
      
      const res = await fetch(fetchUrl);
      if (!res.ok) {
        throw new Error(`HTTP Error ${res.status}: Failed to fetch.`);
      }
      
      const data = await res.json();
      rawData = data;
    } catch (e: any) {
      error = e.message || 'Unknown fetch failure';
    } finally {
      loading = false;
    }
  }

  // Recursive schema introspector to flatten nested JSON structures
  function introspectSchema(obj: any, prefix = ''): Array<{ path: string; type: string; val: string }> {
    if (!obj) return [];
    
    let fields: Array<{ path: string; type: string; val: string }> = [];
    
    // Resolve array of objects to inspect the first element
    if (Array.isArray(obj)) {
      if (obj.length === 0) return [];
      return introspectSchema(obj[0], prefix);
    }

    if (typeof obj === 'object') {
      for (const [key, value] of Object.entries(obj)) {
        const currentPath = prefix ? `${prefix}.${key}` : key;
        
        if (value === null) {
          fields.push({ path: currentPath, type: 'null', val: 'null' });
        } else if (Array.isArray(value)) {
          if (value.length > 0 && typeof value[0] === 'object' && value[0] !== null) {
            // Document array of objects by traversing first item
            fields.push({ path: `${currentPath}[]`, type: 'Array of Objects', val: '' });
            fields = [...fields, ...introspectSchema(value[0], `${currentPath}[]`)];
          } else {
            const itemType = value.length > 0 ? typeof value[0] : 'unknown';
            fields.push({ path: currentPath, type: `Array of ${itemType}`, val: JSON.stringify(value.slice(0, 3)) });
          }
        } else if (typeof value === 'object') {
          fields.push({ path: currentPath, type: 'Object', val: '' });
          fields = [...fields, ...introspectSchema(value, currentPath)];
        } else {
          fields.push({ 
            path: currentPath, 
            type: typeof value, 
            val: typeof value === 'string' && value.length > 60 ? value.substring(0, 60) + '...' : String(value) 
          });
        }
      }
    }
    
    return fields;
  }

  // Derive schema records from raw data
  let schemaRecords = $derived.by(() => {
    if (!rawData) return [];
    return introspectSchema(rawData);
  });

  // Derive preview data (limit to first 5 items)
  let previewData = $derived.by(() => {
    if (!rawData) return null;
    if (Array.isArray(rawData)) {
      return rawData.slice(0, 5);
    }
    return rawData;
  });

  function copyToClipboard(text: string, key: string) {
    navigator.clipboard.writeText(text).then(() => {
      copiedText = key;
      setTimeout(() => {
        if (copiedText === key) copiedText = null;
      }, 2000);
    });
  }

  // Helper to escape Svelte curly braces
  const ob = '{';
  const cb = '}';
</script>

{#if isOpen && endpoint}
  <!-- Backdrop -->
  <div class="modal-backdrop" onclick={() => isOpen = false} role="presentation"></div>

  <!-- Modal Window -->
  <div class="modal-window">
    <header class="modal-header">
      <div class="modal-title-col">
        {#if endpoint.isCanonical}
          <div class="modal-badge badge-canonical">DATABASE_CANONICAL (OPTIMIZED)</div>
        {:else if apiSource === 'mirror'}
          <div class="modal-badge badge-mirror">DATABASE_MIRROR (OPTIMIZED)</div>
        {:else}
          <div class="modal-badge badge-proxy">PROXY_PASSTHROUGH (LIVE)</div>
        {/if}
        <h2>{endpoint.name}</h2>
        {#if endpoint.isCanonical}
          <code class="modal-path">GET /api/v2/canonical/gb-sct/{endpoint.path}</code>
        {:else if apiSource === 'mirror'}
          <code class="modal-path">GET /api/v2/mirror/gb-sct/{endpoint.path}</code>
        {:else}
          <code class="modal-path">GET https://data.parliament.scot/api/{endpoint.path}</code>
        {/if}
      </div>
      <button class="btn-close" onclick={() => isOpen = false} aria-label="Close modal">
        <X size={20} />
      </button>
    </header>

    <!-- Query Editor Panel -->
    <section class="query-panel">
      <div class="query-input-row">
        <span class="query-label">API Data Source:</span>
        <div class="source-select-container">
          <select class="source-select" bind:value={apiSource} onchange={triggerFetch}>
            {#if endpoint.isCanonical}
              <option value="canonical">Local PostgreSQL Database B Canonical Research (Optimized)</option>
            {:else}
              <option value="mirror">Local PostgreSQL Database Mirror (Optimized)</option>
              <option value="proxy">Scottish Parliament Proxy API (Live)</option>
            {/if}
          </select>
        </div>
      </div>
      {#if apiSource === 'mirror' || apiSource === 'canonical'}
        <div class="query-input-row downloads-row">
          <div class="bulk-downloads-row">
            <span class="bulk-download-title">Bulk Downloads:</span>
            {#if endpoint.isCanonical}
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
            {:else}
              <a 
                href="/downloads/gb-sct/{endpoint.path}.{csvExt}?v=2" 
                download 
                class="btn-bulk-download"
                title={isUncompressed ? "Download complete mirrored table as plain CSV" : "Download complete mirrored table as compressed CSV.GZ"}
              >
                CSV{isUncompressed ? '' : '.GZ'}
              </a>
              <a 
                href="/downloads/gb-sct/{endpoint.path}.parquet?v=2" 
                download 
                class="btn-bulk-download btn-parquet"
                title="Download complete mirrored table as snappy-compressed Parquet"
              >
                Parquet
              </a>
              <a 
                href="/downloads/gb-sct/gb_sct_mirror.sqlite.gz?v=2" 
                download 
                class="btn-bulk-download btn-sqlite"
                title="Download entire 15-table relational database as compressed SQLite.GZ"
              >
                Full SQLite DB
              </a>
            {/if}
          </div>
          <div class="decompression-help">
            💡 Gzip (.gz) archives can be extracted using 
            <a href="https://7-zip.org/" target="_blank" rel="noopener noreferrer">7-Zip</a> (Win/Linux) or 
            <a href="https://www.keka.io/" target="_blank" rel="noopener noreferrer">Keka</a> (macOS). 
            If your browser automatically decompresses the download, you can open it directly or rename it to .csv / .sqlite.
          </div>
        </div>
      {/if}
      <div class="query-input-row mt-2">
        <span class="query-label">Edit Query Parameters:</span>
        <input 
          type="text" 
          class="query-input" 
          bind:value={queryParams} 
          placeholder="e.g. ?$top=5 or ?year=2024"
        />
        <button class="btn-run" onclick={triggerFetch} disabled={loading}>
          <Play size={12} fill="currentColor" /> Run Query
        </button>
      </div>
      <span class="text-xs text-slate-400">
        {#if apiSource === 'mirror'}
          Local Database Mirror Endpoint: 
          <a 
            href={requestUrl} 
            target="_blank" 
            rel="noopener noreferrer" 
            class="external-link"
          >
            {requestUrl} <ExternalLink size={10} />
          </a>
        {:else}
          Direct Host API Endpoint: 
          <a 
            href={requestUrl} 
            target="_blank" 
            rel="noopener noreferrer" 
            class="external-link"
          >
            {requestUrl} <ExternalLink size={10} />
          </a>
        {/if}
      </span>
    </section>

    <!-- Tab Bar -->
    <nav class="tab-bar">
      <button 
        class="tab-btn" 
        class:active={activeTab === 'schema'} 
        onclick={() => activeTab = 'schema'}
      >
        Dynamic Schema ({schemaRecords.length} fields)
      </button>
      <button 
        class="tab-btn" 
        class:active={activeTab === 'preview'} 
        onclick={() => activeTab = 'preview'}
      >
        JSON Payload Preview
      </button>
      <button 
        class="tab-btn" 
        class:active={activeTab === 'snippets'} 
        onclick={() => activeTab = 'snippets'}
      >
        Replication Snippets
      </button>
    </nav>

    <!-- Modal Body -->
    <div class="modal-body">
      {#if loading}
        <div class="status-box text-indigo-400">
          <div class="spinner"></div> Introspecting live assembly payload...
        </div>
      {:else if error}
        <div class="status-box text-rose-400">
          <strong>Introspection Failed:</strong> {error}
        </div>
      {:else if rawData}
        
        <!-- Tab: Schema -->
        {#if activeTab === 'schema'}
          <div class="table-container">
            <table class="schema-table">
              <thead>
                <tr>
                  <th>Field Path</th>
                  <th>JavaScript Type</th>
                  <th>Live Sample Value</th>
                </tr>
              </thead>
              <tbody>
                {#each schemaRecords as field}
                  <tr>
                    <td class="font-mono text-indigo-300">{field.path}</td>
                    <td class="font-mono text-cyan-400">{field.type}</td>
                    <td class="text-slate-300">{field.val}</td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        {/if}

        <!-- Tab: Preview -->
        {#if activeTab === 'preview'}
          <div class="preview-container">
            <div class="preview-header">
            <span class="text-xs text-slate-400">
              {#if apiSource === 'mirror'}
                Displaying sample records directly from optimized local database mirror
              {:else}
                Displaying sample records directly from passthrough proxy
              {/if}
            </span>
              <button 
                class="btn-copy" 
                onclick={() => copyToClipboard(JSON.stringify(rawData, null, 2), 'json')}
              >
                {#if copiedText === 'json'}<Check size={14} /> Copied{:else}<Copy size={14} /> Copy JSON{/if}
              </button>
            </div>
            <pre class="json-code"><code>{JSON.stringify(previewData, null, 2)}</code></pre>
          </div>
        {/if}

        <!-- Tab: Snippets -->
        {#if activeTab === 'snippets'}
          <div class="snippets-container">
            <!-- cURL -->
            <div class="snippet-box">
              <div class="snippet-header">
                <span>cURL (HTTP Get Request)</span>
                <button 
                  class="btn-copy" 
                  onclick={() => copyToClipboard(`curl -X GET "${requestUrl}" -H "Accept: application/json"`, 'curl')}
                >
                  {#if copiedText === 'curl'}<Check size={14} /> Copied{:else}<Copy size={14} /> Copy{/if}
                </button>
              </div>
              <pre class="snippet-code"><code>curl -X GET "{requestUrl}" \
  -H "Accept: application/json"</code></pre>
            </div>

            <!-- Python -->
            <div class="snippet-box mt-4">
              <div class="snippet-header">
                <span>Python (requests)</span>
                <button 
                  class="btn-copy" 
                  onclick={() => copyToClipboard(`import requests\n\nurl = "${requestUrl}"\nheaders = ${ob}"Accept": "application/json"${cb}\nresponse = requests.get(url, headers=headers)\ndata = response.json()\nprint(f"Retrieved ${ob}len(data)${cb} records.")`, 'python')}
                >
                  {#if copiedText === 'python'}<Check size={14} /> Copied{:else}<Copy size={14} /> Copy{/if}
                </button>
              </div>
              <pre class="snippet-code"><code>import requests

url = "{requestUrl}"
headers = {ob}"Accept": "application/json"{cb}

response = requests.get(url, headers=headers)
data = response.json()
print(f"Retrieved {ob}len(data){cb} records.")</code></pre>
            </div>

            <!-- R -->
            <div class="snippet-box mt-4">
              <div class="snippet-header">
                <span>R (httr / jsonlite)</span>
                <button 
                  class="btn-copy" 
                  onclick={() => copyToClipboard(`library(httr)\nlibrary(jsonlite)\n\nurl <- "${requestUrl}"\nresponse <- GET(url, add_headers(Accept = "application/json"))\ndata <- fromJSON(content(response, "text"))\n\nprint(paste("Retrieved", nrow(data), "records."))`, 'r')}
                >
                  {#if copiedText === 'r'}<Check size={14} /> Copied{:else}<Copy size={14} /> Copy{/if}
                </button>
              </div>
              <pre class="snippet-code"><code>library(httr)
library(jsonlite)

url &lt;- "{requestUrl}"
response &lt;- GET(url, add_headers(Accept = "application/json"))
data &lt;- fromJSON(content(response, "text"))

print(paste("Retrieved", nrow(data), "records."))</code></pre>
            </div>
          </div>
        {/if}

      {/if}
    </div>
  </div>
{/if}

<style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(2, 6, 23, 0.8);
    backdrop-filter: blur(8px);
    z-index: 1000;
  }

  .modal-window {
    position: fixed;
    top: 5%;
    left: 50%;
    transform: translateX(-50%);
    width: 90%;
    max-width: 950px;
    height: 85vh;
    background: #0b0f19;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 0.85rem;
    display: flex;
    flex-direction: column;
    z-index: 1001;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    overflow: hidden;
  }

  .modal-header {
    padding: 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }

  .modal-title-col h2 {
    font-family: var(--font-heading);
    font-size: 1.35rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0.35rem 0;
  }

  .modal-badge {
    font-size: 0.65rem;
    font-weight: 800;
    padding: 0.15rem 0.5rem;
    border-radius: 0.25rem;
    display: inline-block;
    border: 1px solid transparent;
  }
  .badge-mirror {
    background: rgba(52, 211, 153, 0.15);
    color: #34d399;
    border-color: rgba(52, 211, 153, 0.25);
  }
  .badge-proxy {
    background: rgba(99, 102, 241, 0.15);
    color: #818cf8;
    border-color: rgba(99, 102, 241, 0.25);
  }

  .source-select-container {
    position: relative;
    display: inline-flex;
    align-items: center;
  }
  .source-select {
    background: rgba(52, 211, 153, 0.12);
    color: #34d399;
    border: 1px solid rgba(52, 211, 153, 0.25);
    padding: 0.25rem 2.25rem 0.25rem 0.85rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    cursor: pointer;
    appearance: none;
    outline: none;
    transition: all 0.2s ease;
  }
  .source-select:hover {
    background: rgba(52, 211, 153, 0.2);
    border-color: #34d399;
    color: #ffffff;
  }
  .source-select-container::after {
    content: "▼";
    font-size: 0.55rem;
    color: #34d399;
    position: absolute;
    right: 0.85rem;
    pointer-events: none;
  }

  .mt-2 {
    margin-top: 0.5rem;
  }

  .btn-bulk-download {
    background: rgba(52, 211, 153, 0.15);
    color: #34d399;
    border: 1px solid rgba(52, 211, 153, 0.3);
    padding: 0.25rem 0.75rem;
    border-radius: 0.375rem;
    font-size: 0.75rem;
    font-weight: 700;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    cursor: pointer;
    transition: all 0.2s;
  }
  .btn-bulk-download:hover {
    background: rgba(52, 211, 153, 0.25);
    border-color: #34d399;
    color: #ffffff;
    box-shadow: 0 0 10px rgba(52, 211, 153, 0.15);
  }

  .bulk-downloads-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .bulk-download-title {
    font-size: 0.7rem;
    color: #94a3b8;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 0.05em;
    margin-right: 0.25rem;
  }
  .btn-parquet {
    background: rgba(56, 189, 248, 0.12) !important;
    color: #38bdf8 !important;
    border-color: rgba(56, 189, 248, 0.25) !important;
  }
  .btn-parquet:hover {
    background: rgba(56, 189, 248, 0.2) !important;
    border-color: #38bdf8 !important;
    color: #ffffff !important;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.15);
  }
  .btn-sqlite {
    background: rgba(251, 191, 36, 0.12) !important;
    color: #fbbf24 !important;
    border-color: rgba(251, 191, 36, 0.25) !important;
  }
  .btn-sqlite:hover {
    background: rgba(251, 191, 36, 0.2) !important;
    border-color: #fbbf24 !important;
    color: #ffffff !important;
    box-shadow: 0 0 10px rgba(251, 191, 36, 0.15);
  }

  .decompression-help {
    font-size: 0.7rem;
    color: #64748b;
    max-width: 480px;
    text-align: right;
    line-height: 1.25;
  }
  .decompression-help a {
    color: #38bdf8;
    text-decoration: none;
    font-weight: 600;
  }
  .decompression-help a:hover {
    text-decoration: underline;
  }

  .modal-path {
    font-family: var(--font-mono);
    color: #94a3b8;
    font-size: 0.8rem;
  }

  .btn-close {
    background: transparent;
    border: none;
    color: #64748b;
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 0.25rem;
    transition: all 0.2s ease;
  }
  .btn-close:hover {
    color: #ffffff;
    background: rgba(255,255,255,0.05);
  }

  .query-panel {
    background: rgba(0,0,0,0.2);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding: 1rem 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .query-input-row {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  .downloads-row {
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
    margin-top: 0.25rem;
    margin-bottom: 0.25rem;
  }

  .query-label {
    font-size: 0.85rem;
    color: #cbd5e1;
    font-weight: 600;
    white-space: nowrap;
  }

  .query-input {
    background: #020617;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #ffffff;
    border-radius: 0.375rem;
    padding: 0.35rem 0.75rem;
    font-family: var(--font-mono);
    font-size: 0.85rem;
    flex: 1;
  }
  .query-input:focus {
    border-color: #4f46e5;
    outline: none;
  }

  .btn-run {
    background: #4f46e5;
    color: #ffffff;
    border: none;
    padding: 0.35rem 1rem;
    border-radius: 0.375rem;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.35rem;
    transition: background 0.2s;
  }
  .btn-run:hover { background: #4338ca; }

  .external-link {
    color: #818cf8;
    text-decoration: none;
  }
  .external-link:hover { text-decoration: underline; }

  .tab-bar {
    display: flex;
    background: #080b12;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding: 0 1.5rem;
  }

  .tab-btn {
    background: transparent;
    border: none;
    color: #64748b;
    padding: 1rem 1.25rem;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    border-bottom: 2px solid transparent;
    transition: all 0.2s ease;
  }
  .tab-btn:hover { color: #ffffff; }
  .tab-btn.active {
    color: #818cf8;
    border-bottom-color: #818cf8;
  }

  .modal-body {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
    background: #070a12;
  }

  .status-box {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    height: 200px;
    font-size: 0.95rem;
  }

  .spinner {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(129, 140, 248, 0.2);
    border-top-color: #818cf8;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .table-container {
    overflow-x: auto;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 0.5rem;
  }

  .schema-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
    text-align: left;
  }

  .schema-table th, .schema-table td {
    padding: 0.85rem 1.25rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  }

  .schema-table th {
    background: rgba(15, 23, 42, 0.6);
    color: #94a3b8;
    font-weight: 600;
  }

  .schema-table tbody tr:hover {
    background: rgba(255, 255, 255, 0.01);
  }

  .font-mono { font-family: var(--font-mono); }
  .text-indigo-300 { color: #a5b4fc; }
  .text-cyan-400 { color: #22d4bf; }
  .text-slate-300 { color: #cbd5e1; }
  .text-rose-400 { color: #fb7185; }
  .text-xs { font-size: 0.75rem; }

  .preview-container {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    height: 100%;
  }

  .preview-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .btn-copy {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    color: #cbd5e1;
    padding: 0.35rem 0.75rem;
    border-radius: 0.375rem;
    font-size: 0.75rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.35rem;
    transition: all 0.2s;
  }
  .btn-copy:hover {
    background: rgba(99, 102, 241, 0.15);
    border-color: rgba(99, 102, 241, 0.35);
    color: #a5b4fc;
  }

  .json-code {
    background: #020617;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 0.5rem;
    padding: 1.25rem;
    font-family: var(--font-mono);
    font-size: 0.825rem;
    color: #cbd5e1;
    overflow-x: auto;
    max-height: 480px;
    margin: 0;
  }

  .snippets-container {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .snippet-box {
    background: rgba(15, 23, 42, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 0.5rem;
    overflow: hidden;
  }

  .snippet-header {
    background: rgba(2, 6, 23, 0.6);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    padding: 0.75rem 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.8rem;
    font-weight: 700;
    color: #94a3b8;
  }

  .snippet-code {
    padding: 1.25rem;
    background: #020617;
    margin: 0;
    overflow-x: auto;
    font-family: var(--font-mono);
    font-size: 0.825rem;
    color: #cbd5e1;
  }
</style>
