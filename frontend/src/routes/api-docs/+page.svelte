<script lang="ts">
  import { FileCode2, Download, CheckCircle2, Copy, Check, ExternalLink, Terminal } from 'lucide-svelte';

  let copiedEndpoint = $state<string | null>(null);

  function copyCode(text: string, label: string) {
    navigator.clipboard.writeText(text);
    copiedEndpoint = label;
    setTimeout(() => { copiedEndpoint = null; }, 2000);
  }
</script>

<svelte:head>
  <title>API & Bulk Data Access — Comparative Legislative Data Platform</title>
  <meta name="description" content="Live versioned REST APIs, 1:1 host parity reconciliation, and bulk CSV/Parquet dataset downloads for the Scottish Parliament and comparative assemblies." />
</svelte:head>

<div class="container page-padding">
  <!-- Page Header -->
  <div class="page-header">
    <div class="header-badge">
      <span class="badge badge-success">Live API v2.8.0</span>
      <span>100% Host Parity Verified</span>
    </div>
    <h1 class="page-title">Versioned REST APIs & Bulk Downloads</h1>
    <p class="page-sub">
      High-speed JSON REST APIs and bulk CSV/Parquet research datasets for computational social science, powered by zero-rate-limit database mirrors.
    </p>
  </div>

  <!-- Live Status Card -->
  <div class="card status-banner-card">
    <div class="status-icon">
      <CheckCircle2 size={32} color="#10b981" />
    </div>
    <div class="status-text">
      <h3>Active Jurisdiction: Scottish Parliament (Holyrood / GB-SCT)</h3>
      <p>
        102,317 raw API records ingested across 13 native endpoints. 473 canonical bill records (Sessions 1–6, 1999–Present) evaluated under 100.0% Pass 1 Ground-Truth Baseline.
      </p>
    </div>
  </div>

  <!-- Endpoint Explorer Grid -->
  <h2 class="section-heading">Versioned Production Endpoints</h2>

  <div class="endpoints-list">
    <!-- Endpoint 1: Health & Parity Monitor -->
    <div class="card endpoint-card">
      <div class="ep-header">
        <span class="method-tag method-get">GET</span>
        <code class="ep-url">https://legislativedata.org/api/v1/GB-SCT/health</code>
        <button class="btn-copy" onclick={() => copyCode('curl -s https://legislativedata.org/api/v1/GB-SCT/health', 'health')}>
          {#if copiedEndpoint === 'health'}<Check size={13} color="#4ade80" /> Copied{:else}<Copy size={13} /> Copy cURL{/if}
        </button>
      </div>
      <p class="ep-desc">Returns real-time database mirror health status, 1:1 host parity verification report, sync timestamp, and record counts.</p>
      <div class="ep-sample">
        <pre><code>{`{
  "status": "HEALTHY",
  "jurisdiction": "GB-SCT",
  "parity_verification": "100.0% EXACT HOST PARITY VERIFIED",
  "last_reconciliation_timestamp": "2026-07-24 16:37:07 UTC",
  "raw_records_count": 102317,
  "canonical_records_count": 473
}`}</code></pre>
      </div>
    </div>

    <!-- Endpoint 2: Canonical Bills -->
    <div class="card endpoint-card">
      <div class="ep-header">
        <span class="method-tag method-get">GET</span>
        <code class="ep-url">https://legislativedata.org/api/v1/GB-SCT/canonical/bills?limit=50</code>
        <button class="btn-copy" onclick={() => copyCode('curl -s "https://legislativedata.org/api/v1/GB-SCT/canonical/bills?limit=50"', 'bills')}>
          {#if copiedEndpoint === 'bills'}<Check size={13} color="#4ade80" /> Copied{:else}<Copy size={13} /> Copy cURL{/if}
        </button>
      </div>
      <p class="ep-desc">Returns 72 Pass 1 baseline variables (51 `NATIVE_DIRECT` + 21 `DERIVED_DETERMINISTIC`) for all 473 Scottish Parliament bills.</p>
      <div class="ep-params">
        <span>Query Parameters:</span> <code>limit=50</code> &bull; <code>initiator_type=EXECUTIVE</code>
      </div>
    </div>

    <!-- Endpoint 3: Bulk Downloads -->
    <div class="card endpoint-card">
      <div class="ep-header">
        <span class="method-tag method-download">DOWNLOAD</span>
        <code class="ep-url">https://legislativedata.org/static/data/GB-SCT_canonical_bills.csv</code>
        <a href="https://legislativedata.org/static/data/GB-SCT_canonical_bills.csv" download class="btn-copy">
          <Download size={13} /> Download CSV
        </a>
      </div>
      <p class="ep-desc">Bulk research package containing all 72 canonical variables formatted for R, Python, Excel, SPSS, and Stata.</p>
      <div class="download-formats-row">
        <a href="https://legislativedata.org/static/data/GB-SCT_canonical_bills.csv" download class="fmt-pill">CSV Dataset</a>
        <a href="https://legislativedata.org/static/data/GB-SCT_canonical_bills.json" download class="fmt-pill">JSON Dataset</a>
        <a href="https://legislativedata.org/static/data/GB-SCT_canonical_bills.parquet" download class="fmt-pill">Parquet Dataset</a>
        <a href="https://legislativedata.org/static/data/GB-SCT_canonical_bills_loader.R" download class="fmt-pill">R Import Script (.R)</a>
      </div>
    </div>
  </div>
</div>

<style>
  .page-padding { padding: 3rem 1.5rem; }
  .page-header { text-align: center; max-width: 800px; margin: 0 auto 2.5rem; }
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
  .page-sub { font-size: 1.05rem; color: var(--text-muted); }

  .status-banner-card {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(17, 24, 39, 0.95) 100%);
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 1.75rem;
    margin-bottom: 3.5rem;
  }

  .status-text h3 { font-size: 1.25rem; color: #ffffff; margin-bottom: 0.35rem; }
  .status-text p { color: var(--text-muted); font-size: 0.9rem; }

  .section-heading { font-size: 1.5rem; margin-bottom: 1.5rem; }

  .endpoints-list { display: flex; flex-direction: column; gap: 1.5rem; }

  .endpoint-card { padding: 1.5rem; display: flex; flex-direction: column; gap: 0.85rem; }
  .ep-header { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }
  .method-tag {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
  }
  .method-get { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
  .method-download { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }

  .ep-url { font-family: var(--font-mono); font-size: 0.95rem; color: var(--accent-cyan); flex-grow: 1; word-break: break-all; }

  .btn-copy {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(31, 41, 55, 0.8);
    border: 1px solid var(--border-subtle);
    color: #e5e7eb;
    padding: 0.35rem 0.75rem;
    border-radius: 6px;
    font-size: 0.8rem;
    cursor: pointer;
  }
  .btn-copy:hover { border-color: var(--accent-cyan); color: #ffffff; }

  .ep-desc { color: var(--text-muted); font-size: 0.9rem; }

  .ep-sample pre {
    background: #090d16;
    padding: 0.85rem;
    border-radius: 6px;
    font-size: 0.8rem;
    font-family: var(--font-mono);
    color: #38bdf8;
    overflow-x: auto;
  }

  .ep-params { font-size: 0.825rem; color: var(--text-muted); }
  .ep-params code { background: rgba(31, 41, 55, 0.6); padding: 0.15rem 0.4rem; border-radius: 4px; color: #ffffff; }

  .download-formats-row { display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 0.5rem; }
  .fmt-pill {
    background: rgba(31, 41, 55, 0.6);
    border: 1px solid var(--border-subtle);
    color: #e5e7eb;
    padding: 0.4rem 0.85rem;
    border-radius: 6px;
    font-size: 0.8rem;
    text-decoration: none;
  }
  .fmt-pill:hover { border-color: var(--accent-cyan); color: var(--accent-cyan); }
</style>
