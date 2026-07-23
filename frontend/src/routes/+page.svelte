<script lang="ts">
  import { Globe, Database, BookOpen, ShieldCheck, ArrowRight, Layers, FileCode2, CheckCircle2, Mail, Sparkles, AlertTriangle, Code2 } from 'lucide-svelte';

  const assemblies = [
    { code: 'GB-UKP', name: 'UK Parliament', location: 'Westminster', type: 'Sovereign Bicameral', status: 'In Audit', tier: 'Phase 0' },
    { code: 'GB-SCT', name: 'Scottish Parliament', location: 'Holyrood', type: 'Devolved Unicameral', status: 'In Audit', tier: 'Phase 0' },
    { code: 'GB-WLS', name: 'Senedd Cymru', location: 'Cardiff', type: 'Devolved Unicameral', status: 'Planned', tier: 'Phase 0' },
    { code: 'GB-NIR', name: 'Northern Ireland Assembly', location: 'Stormont', type: 'Devolved Assembly', status: 'Planned', tier: 'Phase 0' },
    { code: 'IM-TYN', name: 'Isle of Man Tynwald', location: 'Douglas', type: 'Crown Dependency Bicameral', status: 'Planned', tier: 'Phase 0' },
    { code: 'JE-STJ', name: 'States of Jersey', location: 'St Helier', type: 'Crown Dependency Consensus', status: 'Planned', tier: 'Phase 0' },
    { code: 'GG-STG', name: 'States of Guernsey', location: 'St Peter Port', type: 'Crown Dependency Consensus', status: 'Planned', tier: 'Phase 0' },
    { code: 'GI-GIB', name: 'Gibraltar Parliament', location: 'Gibraltar', type: 'Overseas Territory', status: 'Planned', tier: 'Phase 0' }
  ];

  const dataCatalogSchema = {
    '@context': 'https://schema.org',
    '@type': 'DataCatalog',
    'name': 'Global Parliamentary Data Audit & Mapping Atlas',
    'description': 'Comparative academic research engine mapping data availability, API endpoints, rate limits, and 6-tier provenance schemas across international assemblies.',
    'url': 'https://legislativedata.org',
    'publisher': {
      '@type': 'Organization',
      'name': 'Comparative Legislative Data Project'
    },
    'dataset': assemblies.map(a => ({
      '@type': 'Dataset',
      'name': `${a.name} (${a.code}) Legislative Open Data Blueprint`,
      'url': `https://legislativedata.org/atlas/${a.code}`,
      'spatialCoverage': a.location
    }))
  };
</script>

<svelte:head>
  <title>Comparative Legislative Data Platform — Open Research Engine & Mapping Atlas</title>
  <meta name="description" content="Open academic research engine mapping data availability, API access endpoints, and 6-tier provenance schemas across international legislatures." />
  
  <meta property="og:title" content="Comparative Legislative Data Platform — Open Research Engine" />
  <meta property="og:description" content="Standardising, auditing, and mapping quantitative legislative data across international parliamentary and presidential assemblies." />

  <!-- Page Structured Data (JSON-LD) -->
  {@html `<script type="application/ld+json">${JSON.stringify(dataCatalogSchema)}</script>`}
</svelte:head>

<!-- Hero Section -->
<section class="hero-section">
  <div class="container hero-content">
    <div class="hero-badge">
      <span class="badge badge-bicd">Academic Consultation v2.4.0</span>
      <span class="hero-badge-text">Dual-Layer Data Engine & 6-Tier Provenance</span>
    </div>

    <h1 class="hero-title">
      Comparative Legislative Data <br />
      <span class="text-gradient">Research Infrastructure & Mapping Atlas</span>
    </h1>

    <p class="hero-subtitle">
      Standardising, mirroring, and auditing quantitative legislative data across international parliamentary and presidential assemblies. 
      Built around a <strong>Dual-Layer Data Architecture</strong> and point-in-time decision tracking.
    </p>

    <div class="hero-cta">
      <a href="/atlas" class="btn-primary btn-lg">
        <Globe size={18} /> Explore Data Atlas
      </a>
      <a href="/schema" class="btn-secondary btn-lg">
        <Layers size={18} /> Master Wishlist Catalog
      </a>
      <a href="/peer-review" class="btn-secondary btn-lg">
        <BookOpen size={18} /> Peer Review Brief
      </a>
    </div>

    <!-- Stats Bar -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-num">2</div>
        <div class="stat-label">Data Layers (Native & Canonical)</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">8</div>
        <div class="stat-label">Research Domains</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">6</div>
        <div class="stat-label">Data Provenance Tiers</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">100%</div>
        <div class="stat-label">Open Access Research</div>
      </div>
    </div>
  </div>
</section>

<!-- Dual-Layer Architecture Section -->
<section class="section section-dual-layer">
  <div class="container">
    <div class="section-header">
      <h2 class="section-title">The Dual-Layer Architecture: "Riding Two Horses"</h2>
      <p class="section-sub">
        Serving single-country legislative specialists with 100% native institutional resolution while empowering cross-national quantitative political scientists with harmonised comparative metrics.
      </p>
    </div>

    <div class="layers-grid">
      <div class="layer-card layer-native">
        <div class="layer-badge">Layer A</div>
        <h3>High-Resolution Native Institutional Layer</h3>
        <p class="layer-desc">Preserves 100% of raw assembly-specific fields, Hansard timestamps, document word counts, motion texts, and roll-call votes without stripping native detail.</p>
        <ul class="layer-list">
          <li><CheckCircle2 size={15} color="#22c55e" /> Raw Hansard API payloads & official publication links</li>
          <li><CheckCircle2 size={15} color="#22c55e" /> Assembly-specific stage codes (e.g. Holyrood Stage 1/2/3)</li>
          <li><CheckCircle2 size={15} color="#22c55e" /> Native motion titles (Financial Resolutions, Stage 1 Reports)</li>
          <li><CheckCircle2 size={15} color="#22c55e" /> Member-level roll-call vote records & party status at date T</li>
        </ul>
      </div>

      <div class="layer-card layer-canonical">
        <div class="layer-badge">Layer B</div>
        <h3>Harmonised Canonical Comparative Layer</h3>
        <p class="layer-desc">Abstracts quantitative metrics across 8 research domains, evaluating every variable against our 6-tier provenance spectrum for comparative modeling.</p>
        <ul class="layer-list">
          <li><CheckCircle2 size={15} color="#38bdf8" /> Standardised stage progression milestones & sitting day intervals</li>
          <li><CheckCircle2 size={15} color="#38bdf8" /> Bill text word counts (`introduced`, `post_committee`, `enacted`)</li>
          <li><CheckCircle2 size={15} color="#38bdf8" /> Point-in-time decision-point floor majority margins</li>
          <li><CheckCircle2 size={15} color="#38bdf8" /> Party unity, dissent rates & cross-party coalition typologies</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- Methodological Core Section -->
<section class="section">
  <div class="container">
    <div class="section-header">
      <h2 class="section-title">The 6-Tier Data Availability & Provenance Spectrum</h2>
      <p class="section-sub">
        Every variable in our Master Wishlist is evaluated per assembly, per session, and at every specific decision point against a rigorous 6-tier spectrum.
      </p>
    </div>

    <div class="typology-display">
      <div class="typology-card">
        <div class="tier-indicator tier-1">Tier 1</div>
        <h3>NATIVE_DIRECT</h3>
        <p>Served out-of-the-box in official host assembly API endpoints or raw bulk data feeds (JSON/XML).</p>
      </div>

      <div class="typology-card">
        <div class="tier-indicator tier-2">Tier 2</div>
        <h3>DERIVED_DETERMINISTIC</h3>
        <p>Generated deterministically via rule-based joins, date arithmetic, or roster lookups.</p>
      </div>

      <div class="typology-card">
        <div class="tier-indicator tier-3">Tier 3</div>
        <h3>DERIVED_HUMAN_CODED</h3>
        <p>Manually hand-coded by human researchers, subject experts, or PhD coders (serving as ground truth).</p>
      </div>

      <div class="typology-card">
        <div class="tier-indicator tier-4">Tier 4</div>
        <h3>DERIVED_SYNTHETIC_AI</h3>
        <p>Synthesized via NLP/LLM text extractions carrying an explicit Validation Lifecycle (Draft -> Sample -> Gold).</p>
      </div>

      <div class="typology-card">
        <div class="tier-indicator tier-5">Tier 5</div>
        <h3>LINKED_EXTERNAL_AUTHORITY</h3>
        <p>Deterministically linked from benchmark peer-reviewed datasets (ParlGov, Wikidata, CAP, MARPOR).</p>
      </div>

      <div class="typology-card">
        <div class="tier-indicator tier-6">Tier 6</div>
        <h3>UNAVAILABLE_HARD_GAP</h3>
        <p>Documented institutional omissions carrying sub-reason codes (Not Recorded, Undigitized, Restricted Access).</p>
      </div>
    </div>
  </div>
</section>

<!-- Peer Review & Call for Collaboration Section -->
<section class="section section-dark">
  <div class="container">
    <div class="callout-box">
      <div class="callout-content">
        <div class="callout-badge">
          <BookOpen size={14} /> Peer Review Consultation Open
        </div>
        <h2>Call for External Academic Review Reports</h2>
        <p>
          We invite legislative scholars, political scientists, and data engineering experts to review our 
          <strong>Dual-Layer Architecture</strong>, <strong>Master Canonical Variable Catalog</strong>, and <strong>6-Tier Provenance Model</strong>. 
          Read our self-contained briefing document and submit a written evaluation report.
        </p>
        <div class="callout-actions">
          <a href="/peer-review" class="btn-primary">
            <BookOpen size={16} /> Read Peer Review Brief
          </a>
          <a href="mailto:comparativelegislativedata@gmail.com" class="btn-secondary">
            <Mail size={16} /> Contact Team: comparativelegislativedata@gmail.com
          </a>
          <a href="https://github.com/comparative-legislative-data/comparative-legislative-data" target="_blank" rel="noopener noreferrer" class="btn-secondary">
            <svg size="16" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"></path><path d="M9 18c-4.51 2-5-2-7-2"></path></svg> Open GitHub Repo
          </a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Assemblies Grid Section -->
<section class="section">
  <div class="container">
    <div class="section-header">
      <h2 class="section-title">Tracked Legislative Assemblies & Atlas Progress</h2>
      <p class="section-sub">Phase 0 initial focus on the British-Irish Council & Commonwealth assemblies.</p>
    </div>

    <div class="assemblies-grid">
      {#each assemblies as a}
        <a href={`/atlas/${a.code}`} class="assembly-card">
          <div class="assembly-header">
            <span class="assembly-code">{a.code}</span>
            <span class="assembly-status">{a.status}</span>
          </div>
          <h3 class="assembly-name">{a.name}</h3>
          <div class="assembly-meta">
            <span class="meta-item">{a.location}</span>
            <span class="meta-bullet">•</span>
            <span class="meta-item">{a.type}</span>
          </div>
          <div class="assembly-arrow">
            Inspect Data Audit Blueprint <ArrowRight size={14} />
          </div>
        </a>
      {/each}
    </div>
  </div>
</section>

<style>
  .hero-section {
    background: radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.15) 0%, rgba(7, 10, 18, 0) 70%);
    padding: 4.5rem 0 3rem;
    border-bottom: 1px solid var(--border-subtle);
  }

  .hero-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .hero-badge {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid var(--border-subtle);
    padding: 0.25rem 0.75rem 0.25rem 0.25rem;
    border-radius: 9999px;
    margin-bottom: 1.5rem;
  }

  .badge-bicd {
    background: var(--accent-indigo);
    color: #ffffff;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    padding: 0.2rem 0.5rem;
    border-radius: 9999px;
  }

  .hero-badge-text {
    font-size: 0.8rem;
    color: var(--text-muted);
  }

  .hero-title {
    font-family: var(--font-heading);
    font-size: 2.75rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
    margin-bottom: 1.25rem;
    letter-spacing: -0.02em;
  }

  .hero-subtitle {
    font-size: 1.15rem;
    color: var(--text-muted);
    max-width: 52rem;
    line-height: 1.6;
    margin-bottom: 2rem;
  }

  .hero-cta {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
    margin-bottom: 3.5rem;
  }

  .btn-lg {
    padding: 0.75rem 1.5rem;
    font-size: 0.95rem;
    font-weight: 600;
    border-radius: 0.5rem;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    text-decoration: none;
    transition: all 0.2s ease;
  }

  .btn-primary {
    background: var(--gradient-primary);
    color: #ffffff;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
  }
  .btn-primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.45);
  }

  .btn-secondary {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border-subtle);
    color: var(--text-main);
  }
  .btn-secondary:hover {
    background: rgba(255, 255, 255, 0.1);
    color: #ffffff;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
    width: 100%;
    max-width: 54rem;
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: 0.75rem;
    padding: 1.5rem;
  }

  .stat-card {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .stat-num {
    font-family: var(--font-heading);
    font-size: 1.75rem;
    font-weight: 800;
    color: var(--accent-cyan);
  }

  .stat-label {
    font-size: 0.775rem;
    color: var(--text-muted);
    margin-top: 0.25rem;
    text-align: center;
  }

  .section {
    padding: 4rem 0;
    border-bottom: 1px solid var(--border-subtle);
  }

  .section-dual-layer {
    background: rgba(15, 23, 42, 0.4);
  }

  .section-header {
    text-align: center;
    max-width: 48rem;
    margin: 0 auto 3rem;
  }

  .section-title {
    font-family: var(--font-heading);
    font-size: 1.85rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.5rem;
  }

  .section-sub {
    font-size: 1rem;
    color: var(--text-muted);
  }

  .layers-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
  }

  .layer-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: 0.75rem;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    position: relative;
  }

  .layer-native { border-top: 3px solid #22c55e; }
  .layer-canonical { border-top: 3px solid #38bdf8; }

  .layer-badge {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.2rem 0.6rem;
    border-radius: 0.25rem;
    margin-bottom: 0.75rem;

    background: rgba(255, 255, 255, 0.1);
    color: var(--text-muted);
  }

  .layer-card h3 {
    font-family: var(--font-heading);
    font-size: 1.25rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.5rem;
  }

  .layer-desc {
    font-size: 0.9rem;
    color: var(--text-muted);
    line-height: 1.5;
    margin-bottom: 1.25rem;
  }

  .layer-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
  }

  .layer-list li {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    color: var(--text-main);
  }

  .typology-display {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 1.25rem;
  }

  .typology-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: 0.65rem;
    padding: 1.5rem;
  }

  .tier-indicator {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    padding: 0.15rem 0.5rem;
    border-radius: 0.25rem;
    margin-bottom: 0.5rem;
  }

  .tier-1 { background: rgba(34, 197, 94, 0.15); color: #4ade80; }
  .tier-2 { background: rgba(56, 189, 248, 0.15); color: #38bdf8; }
  .tier-3 { background: rgba(168, 85, 247, 0.15); color: #c084fc; }
  .tier-4 { background: rgba(234, 179, 8, 0.15); color: #facc15; }
  .tier-5 { background: rgba(99, 102, 241, 0.15); color: #818cf8; }
  .tier-6 { background: rgba(239, 68, 68, 0.15); color: #f87171; }

  .typology-card h3 {
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.4rem;
  }

  .typology-card p {
    font-size: 0.85rem;
    color: var(--text-muted);
    line-height: 1.5;
  }

  .callout-box {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 1rem;
    padding: 2.5rem;
    text-align: center;
  }

  .callout-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(99, 102, 241, 0.2);
    color: var(--accent-cyan);
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    margin-bottom: 1rem;
  }

  .callout-content h2 {
    font-family: var(--font-heading);
    font-size: 1.75rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.75rem;
  }

  .callout-content p {
    font-size: 1rem;
    color: var(--text-muted);
    max-width: 44rem;
    margin: 0 auto 1.5rem;
    line-height: 1.6;
  }

  .callout-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .assemblies-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1.25rem;
  }

  .assembly-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: 0.65rem;
    padding: 1.25rem;
    text-decoration: none;
    transition: all 0.2s ease;
    display: flex;
    flex-direction: column;
  }
  .assembly-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99, 102, 241, 0.4);
    background: rgba(15, 23, 42, 0.9);
  }

  .assembly-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .assembly-code {
    font-family: var(--font-mono);
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--accent-cyan);
  }

  .assembly-status {
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--accent-gold);
    background: rgba(234, 179, 8, 0.1);
    padding: 0.15rem 0.45rem;
    border-radius: 0.25rem;
  }

  .assembly-name {
    font-family: var(--font-heading);
    font-size: 1.05rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.35rem;
  }

  .assembly-meta {
    font-size: 0.775rem;
    color: var(--text-muted);
    display: flex;
    gap: 0.35rem;
    align-items: center;
    margin-bottom: 1rem;
  }

  .assembly-arrow {
    font-size: 0.775rem;
    font-weight: 600;
    color: var(--accent-indigo);
    display: flex;
    align-items: center;
    gap: 0.35rem;
    margin-top: auto;
  }

  @media (max-width: 768px) {
    .hero-title { font-size: 2rem; }
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
    .layers-grid { grid-template-columns: 1fr; }
  }
</style>
