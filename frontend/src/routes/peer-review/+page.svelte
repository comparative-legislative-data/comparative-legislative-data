<script lang="ts">
  import { ShieldCheck, BookOpen, Layers, HelpCircle, FileText, CheckCircle, Mail, MessageSquare } from 'lucide-svelte';

  const briefSchema = {
    '@context': 'https://schema.org',
    '@type': 'TechArticle',
    'name': 'Peer Review Commission Brief & Evaluation Guidelines',
    'headline': 'Formal Academic Peer Review Commission for Comparative Legislative Data Platform',
    'description': 'Briefing document and evaluation guidelines for external peer review of our Dual-Layer Architecture, Master Canonical Variable Catalog, and 7-Tier Provenance Framework.',
    'url': 'https://legislativedata.org/peer-review',
    'author': {
      '@type': 'Organization',
      'name': 'Comparative Legislative Data Project'
    }
  };
</script>

<svelte:head>
  <title>Peer Review Commission Brief & Evaluation Guidelines — Comparative Legislative Data Platform</title>
  <meta name="description" content="Briefing document and evaluation guidelines for external peer review of our Dual-Layer Architecture, Master Canonical Variable Catalog, and 7-Tier Provenance Framework." />
  
  <meta property="og:title" content="Peer Review Commission Brief — Comparative Legislative Data Platform" />
  <meta property="og:description" content="Formal call for written academic evaluation reports on our research infrastructure and provenance methodology." />

  <!-- Article Structured Data (JSON-LD) -->
  {@html `<script type="application/ld+json">${JSON.stringify(briefSchema)}</script>`}
</svelte:head>

<div class="container page-padding">
  <!-- Page Header -->
  <div class="page-header">
    <div class="header-badge">
      <ShieldCheck size={14} /> Academic Consultation v2.8.0
    </div>
    <h1 class="page-title">Peer Review Commission Brief</h1>
    <p class="page-sub">
      Formal briefing document and evaluation guidelines for external peer reviewers evaluating our Dual-Layer Architecture, Master Canonical Variable Catalog, and 7-Tier Provenance Framework.
    </p>
  </div>

  <!-- Section 1: Executive Summary -->
  <section class="card mb-8">
    <h2 class="section-title"><ShieldCheck size={20} color="#6366f1" /> 1. Executive Summary & Purpose</h2>
    <p>
      The <strong>Comparative Legislative Data Platform</strong> (<code>https://legislativedata.org</code>) is an open-access academic research infrastructure designed to standardize, mirror, and audit quantitative legislative data across international parliamentary and presidential assemblies.
    </p>
    <p>
      We commission expert reviewers to evaluate our proposed <strong>Master Canonical Variable Catalog</strong> (Section 3) and <strong>7-Tier Data Availability & Provenance Framework</strong> (Section 2), and to submit a written <strong>Peer Review Report</strong> addressing the core evaluation questions in Section 4.
    </p>
  </section>

  <!-- Section 2: The 7-Tier Data Availability & Provenance Framework -->
  <section class="card mb-8">
    <h2 class="section-title"><Layers size={20} color="#38bdf8" /> 2. The 7-Tier Data Availability & Provenance Framework</h2>
    <p class="mb-4">
      The framework cleanly separates the <strong>Master Canonical Variable Wishlist</strong> (the target research schema across 11 domains) from the 7 ways data values are instantiated per assembly and decision point:
    </p>

    <div class="typology-grid">
      <div class="tier-box tier-native">
        <div class="tier-badge">Tier 1</div>
        <h4>NATIVE_DIRECT</h4>
        <p>Available directly in host assembly official APIs or raw feeds (JSON/XML).</p>
      </div>

      <div class="tier-box tier-deterministic">
        <div class="tier-badge">Tier 2</div>
        <h4>DERIVED_DETERMINISTIC</h4>
        <p>Generated deterministically via rule-based joins, date arithmetic, or temporal roster lookups on structured JSON API feeds.</p>
      </div>

      <div class="tier-box tier-extracted">
        <div class="tier-badge">Tier 3</div>
        <h4>DERIVED_EXTRACTED</h4>
        <p>Programmatically extracted via PDF/HTML document text parsing, Hansard transcript scraping, or Marshalled List regex parsing.</p>
      </div>

      <div class="tier-box tier-human">
        <div class="tier-badge">Tier 4</div>
        <h4>DERIVED_HUMAN_CODED</h4>
        <p>Manually hand-coded by human researchers, subject experts, or doctoral coders (Gold Standard).</p>
      </div>

      <div class="tier-box tier-ai">
        <div class="tier-badge">Tier 5</div>
        <h4>DERIVED_SYNTHETIC_AI</h4>
        <p>Synthesized via NLP/LLM text extractions carrying the AI Validation Lifecycle (Draft -> Sample -> Gold).</p>
      </div>

      <div class="tier-box tier-linked">
        <div class="tier-badge">Tier 6</div>
        <h4>LINKED_EXTERNAL_AUTHORITY</h4>
        <p>Deterministically linked from benchmark peer-reviewed datasets (ParlGov, Wikidata, CAP, MARPOR).</p>
      </div>

      <div class="tier-box tier-gap">
        <div class="tier-badge">Tier 7</div>
        <h4>UNAVAILABLE_HARD_GAP</h4>
        <p>Institutional data omissions carrying sub-reason codes (Not Recorded, Undigitized, Restricted Access, Not Applicable).</p>
      </div>
    </div>
  </section>

  <!-- Section 3: Commission Questions -->
  <section class="card mb-8">
    <h2 class="section-title"><HelpCircle size={20} color="#a855f7" /> 3. Commission Questions for Written Report</h2>
    <div class="questions-list">
      <div class="q-group">
        <h3>Area 1: Variable Completeness & Conceptual Scope</h3>
        <ol>
          <li>Does the <strong>Master Canonical Variable Catalog</strong> cover the necessary quantitative variables across all 11 research domains (including micro amendments, committee rosters, and debate proceedings)?</li>
          <li>Are there critical variables in comparative legislative studies that are missing and should be added?</li>
          <li>Are the variable definitions and enums sufficiently neutral to span both parliamentary (Westminster, devolved, consensus) and presidential/semi-presidential systems?</li>
        </ol>
      </div>

      <div class="q-group">
        <h3>Area 2: 7-Tier Provenance Spectrum, Temporal Tracking & External Linking</h3>
        <ol start="4">
          <li>Is the 7-tier provenance spectrum (<code>NATIVE_DIRECT</code> vs <code>DERIVED_DETERMINISTIC</code> vs <code>DERIVED_EXTRACTED</code> vs <code>DERIVED_HUMAN_CODED</code> vs <code>DERIVED_SYNTHETIC_AI</code> vs <code>LINKED_EXTERNAL_AUTHORITY</code> vs <code>UNAVAILABLE_HARD_GAP</code>) methodologically sound for academic publication?</li>
          <li>Does evaluating politician affiliation and floor arithmetic at <strong>every decision point</strong> (bill introduction, amendment tabling, division vote) resolve temporal changes in parliamentary majority status?</li>
          <li>How effectively does linking external authority datasets (ParlGov, CAP, Wikidata) enhance comparative analysis?</li>
        </ol>
      </div>

      <div class="q-group">
        <h3>Area 3: Data Gap Transparency & Academic Utility</h3>
        <ol start="7">
          <li>Does explicitly documenting host API omissions as <code>UNAVAILABLE_HARD_GAP</code> with sub-reason codes provide sufficient transparency for comparative political scientists?</li>
          <li>What metadata or documentation format would make this platform most useful for your own quantitative research or teaching?</li>
        </ol>
      </div>
    </div>
  </section>

  <!-- Submission Box -->
  <section class="card submission-card">
    <div class="submission-header">
      <h2>How to Submit Your Peer Review Evaluation Report</h2>
      <p>Written evaluation reports should address the commission questions in Section 3 and can be submitted via email or GitHub Discussion.</p>
    </div>
    <div class="submission-actions">
      <a href="mailto:comparativelegislativedata@gmail.com?subject=Peer Review Evaluation Submission" class="btn-primary">
        <Mail size={16} /> Email Peer Review Submission
      </a>
      <a href="https://github.com/comparative-legislative-data/comparative-legislative-data/discussions" target="_blank" rel="noopener noreferrer" class="btn-secondary">
        <MessageSquare size={16} /> Submit on GitHub Discussions
      </a>
    </div>
  </section>
</div>

<style>
  .page-padding { padding-top: 2rem; padding-bottom: 5rem; }
  .mb-8 { margin-bottom: 2rem; }

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

  .page-title {
    font-family: var(--font-heading);
    font-size: 2.25rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.5rem;
  }

  .page-sub {
    font-size: 1.05rem;
    color: var(--text-muted);
    max-width: 48rem;
    line-height: 1.5;
  }

  .section-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: var(--font-heading);
    font-size: 1.35rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 1rem;
  }

  p {
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 1rem;
    font-size: 0.95rem;
  }

  .typology-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 1.25rem;
    margin-top: 1.25rem;
  }

  .tier-box {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid var(--border-subtle);
    border-radius: 0.65rem;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .tier-badge {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    padding: 0.15rem 0.45rem;
    border-radius: 0.25rem;
    align-self: flex-start;
  }

  .tier-native .tier-badge { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
  .tier-deterministic .tier-badge { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
  .tier-extracted .tier-badge { background: rgba(45, 212, 191, 0.15); color: #2dd4bf; border: 1px solid rgba(45, 212, 191, 0.3); }
  .tier-human .tier-badge { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
  .tier-ai .tier-badge { background: rgba(251, 191, 36, 0.15); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3); }
  .tier-linked .tier-badge { background: rgba(96, 165, 250, 0.15); color: #60a5fa; border: 1px solid rgba(96, 165, 250, 0.3); }
  .tier-gap .tier-badge { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }

  .tier-box h4 {
    font-family: var(--font-mono);
    font-size: 0.95rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
  }

  .tier-box p {
    font-size: 0.825rem;
    color: var(--text-muted);
    line-height: 1.45;
    margin: 0;
  }

  .questions-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .q-group h3 {
    font-family: var(--font-heading);
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--accent-cyan);
    margin-bottom: 0.75rem;
  }

  .q-group ol {
    padding-left: 1.25rem;
    color: var(--text-muted);
    line-height: 1.6;
    font-size: 0.95rem;
  }

  .q-group li {
    margin-bottom: 0.5rem;
  }

  .submission-card {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(56, 189, 248, 0.05));
    border: 1px solid rgba(99, 102, 241, 0.3);
  }

  .submission-header h2 {
    font-family: var(--font-heading);
    font-size: 1.35rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.5rem;
  }

  .submission-actions {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-top: 1.25rem;
  }
</style>
