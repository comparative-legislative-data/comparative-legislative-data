<script lang="ts">
  import { X, Play, Terminal, ExternalLink } from 'lucide-svelte';

  let { isOpen = $bindable(false), variable } = $props();

  let loading = $state(false);
  let downloadingCsv = $state(false);
  let error = $state<string | null>(null);
  let rawData = $state<any>(null);

  // Derived request URL targeting Database B OData Select option
  let requestUrl = $derived.by(() => {
    if (!variable) return '';
    const host = typeof window !== 'undefined' ? window.location.origin : 'http://legislativedata.org';
    const keyField = variable.endpoint === 'bills' ? 'BillID' : 'SnapshotDate';
    const extraField = variable.endpoint === 'bills' ? ',ShortName' : ',PartyName';
    
    // Select primary key, a label descriptor, and the inspected variable
    const selectParam = `?$select=${keyField}${extraField},${variable.name}&$top=3`;
    return `${host}/api/v2/canonical/gb-sct/${variable.endpoint}${selectParam}`;
  });

  $effect(() => {
    if (isOpen && variable) {
      error = null;
      rawData = null;
      triggerFetch();
    }
  });

  async function triggerFetch() {
    if (!variable) return;
    loading = true;
    error = null;
    rawData = null;

    try {
      const keyField = variable.endpoint === 'bills' ? 'BillID' : 'SnapshotDate';
      const extraField = variable.endpoint === 'bills' ? ',ShortName' : ',PartyName';
      const selectParam = `?$select=${keyField}${extraField},${variable.name}&$top=3`;
      const fetchUrl = `/api/v2/canonical/gb-sct/${variable.endpoint}${selectParam}`;
      
      const res = await fetch(fetchUrl);
      if (!res.ok) {
        throw new Error(`HTTP Error ${res.status}: Failed to fetch canonical variable.`);
      }
      
      const data = await res.json();
      rawData = data;
    } catch (e: any) {
      error = e.message || 'Unknown fetch failure';
    } finally {
      loading = false;
    }
  }

  // Download this variable column as a 2-column CSV slice from Database B
  async function downloadVariableCSV() {
    if (!variable) return;
    downloadingCsv = true;
    try {
      const keyField = variable.endpoint === 'bills' ? 'BillID' : 'SnapshotDate';
      // Fetch ALL rows (omitting the $top limit)
      const fetchUrl = `/api/v2/canonical/gb-sct/${variable.endpoint}?$select=${keyField},${variable.name}`;
      const res = await fetch(fetchUrl);
      if (!res.ok) throw new Error(`HTTP Error ${res.status}: Failed to fetch column data.`);
      
      const data = await res.json();
      
      // Build CSV content
      const headers = [keyField, variable.name];
      const csvRows = [headers.join(",")];
      for (const row of data) {
        const val = row[variable.name];
        let escapedVal = '';
        if (val === null || val === undefined) {
          escapedVal = '';
        } else if (typeof val === 'string') {
          escapedVal = val.includes(',') || val.includes('"') || val.includes('\n')
            ? `"${val.replace(/"/g, '""')}"`
            : val;
        } else {
          escapedVal = String(val);
        }
        csvRows.push(`${row[keyField]},${escapedVal}`);
      }
      
      const csvContent = csvRows.join("\n");
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.setAttribute("href", url);
      link.setAttribute("download", `canonical_var_${variable.name.toLowerCase()}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (e: any) {
      alert(`Export failed: ${e.message}`);
    } finally {
      downloadingCsv = false;
    }
  }

  // Download the loaded JSON preview slice
  function downloadVariableJSON() {
    if (!rawData) return;
    const blob = new Blob([JSON.stringify(rawData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `canonical_var_${variable.name.toLowerCase()}_preview.json`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
</script>

{#if isOpen && variable}
  <!-- Backdrop -->
  <div class="modal-backdrop" onclick={() => isOpen = false} role="presentation"></div>

  <!-- Modal Window -->
  <div class="modal-window">
    <header class="modal-header">
      <div class="modal-title-col">
        <div class="modal-badge">{variable.tier}</div>
        <h2>{variable.name}</h2>
        <span class="span-badge">Active Span: {variable.span}</span>
      </div>
      <button class="btn-close" onclick={() => isOpen = false} aria-label="Close modal">
        <X size={20} />
      </button>
    </header>

    <div class="modal-body">
      <!-- Description Section -->
      <section class="info-section">
        <h3>Academic Definition</h3>
        <p class="description-text">{variable.description}</p>
      </section>

      <!-- Variable Column Downloads -->
      <section class="downloads-section">
        <h3>Variable Column Downloads</h3>
        <div class="actions-row mt-2">
          <button class="btn-action-var" onclick={downloadVariableCSV} disabled={downloadingCsv}>
            {#if downloadingCsv}
              Compiling CSV...
            {:else}
              Download Variable CSV
            {/if}
          </button>
          <button class="btn-action-var btn-action-var-json" onclick={downloadVariableJSON} disabled={!rawData}>
            Download Preview JSON
          </button>
        </div>
        <p class="sql-caption mt-2">
          💡 CSV download generates a standalone file containing the primary key (<code>{variable.endpoint === 'bills' ? 'BillID' : 'SnapshotDate'}</code>) and this column only.
        </p>
      </section>

      <!-- SQL Provenance Section -->
      <section class="sql-section">
        <h3>PostgreSQL Provenance (Database B Compiler)</h3>
        <div class="code-container">
          <pre><code>{variable.sqlFormula}</code></pre>
        </div>
        <p class="sql-caption">
          💡 This calculation runs strictly inside <code>Database B</code> on PostgreSQL, referencing raw mirrors via <code>postgres_fdw</code>.
        </p>
      </section>

      <!-- Live OData Query Preview -->
      <section class="query-preview-section">
        <h3>Single-Variable OData Query Preview</h3>
        <p class="section-desc">
          Researchers can retrieve <em>only</em> this variable to save bandwidth using OData <code>$select</code>:
        </p>
        <div class="query-url-box">
          <Terminal size={14} class="text-emerald-400" />
          <code class="query-url">GET {requestUrl.split('/api/')[1] ? '/api/' + requestUrl.split('/api/')[1] : requestUrl}</code>
        </div>

        <div class="preview-workspace mt-3">
          {#if loading}
            <div class="loading-state">
              <div class="spinner"></div>
              <span>Running projection query...</span>
            </div>
          {:else if error}
            <div class="error-box">
              ⚠️ {error}
            </div>
          {:else if rawData}
            <div class="json-box">
              <pre><code>{JSON.stringify(rawData, null, 2)}</code></pre>
            </div>
          {/if}
        </div>
      </section>
    </div>

    <footer class="modal-footer">
      <span class="footer-help">Clicking downloads retrieves the full canonical tables.</span>
    </footer>
  </div>
{/if}

<style>
  /* Backdrop & Modal Styling */
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(4, 6, 10, 0.8);
    backdrop-filter: blur(8px);
    z-index: 1000;
  }

  .modal-window {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 90%;
    max-width: 650px;
    max-height: 85vh;
    background: #0f172a;
    border: 1px solid rgba(16, 185, 129, 0.2);
    box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5), 0 10px 10px -5px rgba(0,0,0,0.5), 0 0 40px rgba(16, 185, 129, 0.1);
    border-radius: 1.25rem;
    display: flex;
    flex-direction: column;
    z-index: 1001;
    overflow: hidden;
  }

  .modal-header {
    padding: 1.5rem 1.75rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
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
    padding: 0.2rem 0.6rem;
    background: rgba(16, 185, 129, 0.15);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 9999px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .span-badge {
    font-size: 0.75rem;
    color: #94a3b8;
  }

  .modal-header h2 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.02em;
  }

  .btn-close {
    background: transparent;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 0.5rem;
    transition: all 0.2s ease;
  }
  .btn-close:hover {
    color: #ffffff;
    background: rgba(255,255,255,0.05);
  }

  .modal-body {
    padding: 1.75rem;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 1.75rem;
    text-align: left;
  }

  h3 {
    margin: 0 0 0.5rem 0;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #94a3b8;
    letter-spacing: 0.05em;
  }

  .description-text {
    color: #f1f5f9;
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0;
  }

  /* Downloads section */
  .downloads-section {
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    padding-top: 1.5rem;
  }
  .actions-row {
    display: flex;
    gap: 0.75rem;
    align-items: center;
  }
  .btn-action-var {
    background: rgba(16, 185, 129, 0.1);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.25);
    padding: 0.45rem 1rem;
    border-radius: 0.5rem;
    font-size: 0.8rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .btn-action-var:hover:not(:disabled) {
    background: #10b981;
    color: #0f172a;
    border-color: #10b981;
  }
  .btn-action-var:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  .btn-action-var-json {
    background: rgba(56, 189, 248, 0.1);
    color: #38bdf8;
    border-color: rgba(56, 189, 248, 0.25);
  }
  .btn-action-var-json:hover:not(:disabled) {
    background: #38bdf8;
    color: #0f172a;
    border-color: #38bdf8;
  }

  /* Code Container Styles */
  .code-container {
    background: #090d16;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 0.75rem;
    padding: 1rem;
    overflow-x: auto;
  }
  .code-container pre, .json-box pre {
    margin: 0;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 0.85rem;
  }
  .code-container code {
    color: #34d399;
  }

  .sql-caption {
    font-size: 0.75rem;
    color: #64748b;
    margin: 0.5rem 0 0 0;
  }

  /* Query Preview */
  .section-desc {
    font-size: 0.85rem;
    color: #94a3b8;
    margin: 0 0 0.75rem 0;
  }

  .query-url-box {
    background: rgba(16, 185, 129, 0.06);
    border: 1px solid rgba(16, 185, 129, 0.15);
    border-radius: 0.5rem;
    padding: 0.65rem 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.65rem;
  }
  .query-url {
    font-family: monospace;
    color: #34d399;
    font-size: 0.8rem;
    word-break: break-all;
  }

  .preview-workspace {
    background: #090d16;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 0.75rem;
    min-height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .json-box {
    padding: 1rem;
    max-height: 160px;
    overflow-y: auto;
    text-align: left;
  }
  .json-box code {
    color: #f1f5f9;
  }

  .loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    color: #94a3b8;
    font-size: 0.85rem;
  }

  .spinner {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(16, 185, 129, 0.2);
    border-top-color: #10b981;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  .error-box {
    color: #f87171;
    font-size: 0.85rem;
    padding: 1rem;
  }

  .modal-footer {
    padding: 1rem 1.75rem;
    background: rgba(255,255,255,0.02);
    border-top: 1px solid rgba(255,255,255,0.06);
    display: flex;
    justify-content: flex-end;
  }
  
  .footer-help {
    font-size: 0.75rem;
    color: #64748b;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .mt-2 { margin-top: 0.5rem; }
  .mt-3 { margin-top: 0.75rem; }
</style>
