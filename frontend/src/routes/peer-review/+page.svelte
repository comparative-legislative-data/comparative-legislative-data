<script lang="ts">
  import { BookOpen, CheckCircle, FileText, Mail, Layers, ShieldCheck, HelpCircle, MessageSquare } from 'lucide-svelte';

  const title = "Peer Review Commission Brief & Evaluation Guidelines";
  const description = "Self-contained peer review briefing document for external academic reviewers, legislative scholars, and data engineering experts.";
</script>

<svelte:head>
  <title>{title} — Comparative Legislative Data Platform</title>
  <meta name="description" content={description} />
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
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
      <BookOpen size={14} /> Academic Consultation Brief v2.3.0
    </div>
    <h1>Peer Review Commission Brief & Evaluation Guidelines</h1>
    <p class="lead">
      A self-contained briefing document for external academic reviewers, legislative scholars, political scientists, and quantitative data experts. 
      <strong>No GitHub repository setup is required to submit a review.</strong>
    </p>

    <div class="action-bar">
      <a href="mailto:comparativelegislativedata@gmail.com" class="btn btn-primary">
        <Mail size={16} /> Submit Written Review via Email
      </a>
      <a href="https://github.com/comparative-legislative-data/comparative-legislative-data/discussions" target="_blank" rel="noopener noreferrer" class="btn btn-secondary">
        <MessageSquare size={16} /> Join GitHub Discussion
      </a>
      <a href="https://github.com/comparative-legislative-data/comparative-legislative-data" target="_blank" rel="noopener noreferrer" class="btn btn-secondary">
        <svg size="16" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"></path><path d="M9 18c-4.51 2-5-2-7-2"></path></svg> View Repository
      </a>
    </div>
  </div>

  <!-- Section 1: Executive Summary -->
  <section class="card mb-8">
    <h2 class="section-title"><ShieldCheck size={20} color="#6366f1" /> 1. Executive Summary & Purpose</h2>
    <p>
      The <strong>Comparative Legislative Data Platform</strong> (<code>https://legislativedata.org</code>) is an open-access academic research infrastructure designed to standardize, mirror, and audit quantitative legislative data across international parliamentary and presidential assemblies.
    </p>
    <p>
      We commission expert reviewers to evaluate our proposed <strong>Master Canonical Variable Catalog</strong> (Section 3) and <strong>6-Tier Data Availability & Provenance Framework</strong> (Section 2), and to submit a written <strong>Peer Review Report</strong> addressing the core evaluation questions in Section 4.
    </p>
  </section>

  <!-- Section 2: The 6-Tier Data Availability & Provenance Framework -->
  <section class="card mb-8">
    <h2 class="section-title"><Layers size={20} color="#38bdf8" /> 2. The 6-Tier Data Availability & Provenance Framework</h2>
    <p class="mb-4">
      The framework cleanly separates the <strong>Master Canonical Variable Wishlist</strong> (the target research schema) from the 6 ways data values are instantiated per assembly and decision point:
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
        <p>Generated deterministically via rule-based joins, date arithmetic, or roster lookups.</p>
      </div>

      <div class="tier-box tier-human">
        <div class="tier-badge">Tier 3</div>
        <h4>DERIVED_HUMAN_CODED</h4>
        <p>Manually hand-coded by human researchers, subject experts, or doctoral coders (Gold Standard).</p>
      </div>

      <div class="tier-box tier-ai">
        <div class="tier-badge">Tier 4</div>
        <h4>DERIVED_SYNTHETIC_AI</h4>
        <p>Synthesized via NLP/LLM text extractions carrying the AI Validation Lifecycle (Draft -> Sample -> Gold).</p>
      </div>

      <div class="tier-box tier-linked">
        <div class="tier-badge">Tier 5</div>
        <h4>LINKED_EXTERNAL_AUTHORITY</h4>
        <p>Deterministically linked from benchmark peer-reviewed datasets (ParlGov, Wikidata, CAP, MARPOR).</p>
      </div>

      <div class="tier-box tier-gap">
        <div class="tier-badge">Tier 6</div>
        <h4>UNAVAILABLE_HARD_GAP</h4>
        <p>Institutional data omissions carrying sub-reason codes (Not Recorded, Undigitized, Restricted Access).</p>
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
          <li>Does the <strong>Master Canonical Variable Catalog</strong> cover the necessary quantitative variables for researching legislative effectiveness, executive dominance, sessional timelines, voting coalitions, and procedural obstruction?</li>
          <li>Are there critical variables in comparative legislative studies that are missing and should be added?</li>
          <li>Are the variable definitions and enums sufficiently neutral to span both parliamentary (Westminster, devolved, consensus) and presidential/semi-presidential systems?</li>
        </ol>
      </div>

      <div class="q-group">
        <h3>Area 2: 6-Tier Provenance Spectrum, Temporal Tracking & External Linking</h3>
        <ol start="4">
          <li>Is the 6-tier provenance spectrum (<code>NATIVE_DIRECT</code> vs <code>DERIVED_DETERMINISTIC</code> vs <code>DERIVED_HUMAN_CODED</code> vs <code>DERIVED_SYNTHETIC_AI</code> vs <code>LINKED_EXTERNAL_AUTHORITY</code> vs <code>UNAVAILABLE_HARD_GAP</code>) methodologically sound for academic publication?</li>
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

  <!-- Section 4: Submission Guidelines -->
  <section class="card submission-card mb-8">
    <h2 class="section-title"><FileText size={20} color="#22c55e" /> 4. Report Submission Guidelines</h2>
    <p>
      Expert reviewers are requested to compile their findings into a <strong>Written Peer Review Report</strong> (PDF or Word document format) and submit it directly to the project team:
    </p>
    <div class="contact-box">
      <div class="contact-item">
        <strong>Primary Submission Email:</strong> 
        <a href="mailto:comparativelegislativedata@gmail.com">comparativelegislativedata@gmail.com</a>
      </div>
      <div class="contact-item">
        <strong>GitHub Organization Discussions:</strong> 
        <a href="https://github.com/comparative-legislative-data/comparative-legislative-data/discussions" target="_blank" rel="noopener noreferrer">https://github.com/comparative-legislative-data/comparative-legislative-data/discussions</a>
      </div>
      <div class="contact-item">
        <strong>Project Portal:</strong> 
        <a href="https://legislativedata.org">https://legislativedata.org</a>
      </div>
    </div>
  </section>

  <!-- Section 5: Live GitHub Discussion & Comments -->
  <section class="card">
    <h2 class="section-title"><MessageSquare size={20} color="#38bdf8" /> 5. Public Academic Discussion & Comments</h2>
    <p class="mb-4 text-muted">
      Sign in with your GitHub account below to leave feedback, questions, or methodological suggestions. All comments automatically sync with our GitHub Organization Discussions board.
    </p>
    <div class="giscus"></div>
  </section>
</div>

<style>
  .py-8 { padding-top: 2rem; padding-bottom: 4rem; }
  .mb-8 { margin-bottom: 2rem; }
  .mb-4 { margin-bottom: 1rem; }
  .text-muted { color: var(--text-muted); font-size: 0.9rem; }

  .page-header {
    margin-bottom: 2.5rem;
  }

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
    line-height: 1.25;
    margin-bottom: 0.75rem;
  }

  .lead {
    font-size: 1.1rem;
    color: var(--text-muted);
    max-width: 54rem;
    line-height: 1.6;
    margin-bottom: 1.5rem;
  }

  .action-bar {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.65rem 1.25rem;
    border-radius: 0.5rem;
    font-weight: 600;
    font-size: 0.9rem;
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

  .card {
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
    margin-bottom: 1rem;
  }

  .typology-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1rem;
  }

  .tier-box {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid var(--border-subtle);
    border-radius: 0.5rem;
    padding: 1.25rem;
    position: relative;
  }

  .tier-badge {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    padding: 0.15rem 0.5rem;
    border-radius: 0.25rem;
    margin-bottom: 0.5rem;
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-muted);
  }

  .tier-box h4 {
    font-size: 0.95rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.35rem;
  }

  .tier-box p {
    font-size: 0.85rem;
    color: var(--text-muted);
    line-height: 1.4;
  }

  .tier-native { border-left: 3px solid #22c55e; }
  .tier-deterministic { border-left: 3px solid #38bdf8; }
  .tier-human { border-left: 3px solid #a855f7; }
  .tier-ai { border-left: 3px solid #eab308; }
  .tier-linked { border-left: 3px solid #6366f1; }
  .tier-gap { border-left: 3px solid #ef4444; }

  .questions-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .q-group h3 {
    font-size: 1rem;
    font-weight: 700;
    color: var(--accent-cyan);
    margin-bottom: 0.5rem;
  }

  .q-group ol {
    padding-left: 1.25rem;
  }

  .q-group li {
    font-size: 0.9rem;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
    line-height: 1.5;
  }

  .submission-card {
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.05) 0%, rgba(15, 23, 42, 0.8) 100%);
    border-color: rgba(34, 197, 94, 0.2);
  }

  .contact-box {
    margin-top: 1rem;
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid var(--border-subtle);
    border-radius: 0.5rem;
    padding: 1rem 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .contact-item {
    font-size: 0.9rem;
    color: var(--text-main);
  }

  .contact-item a {
    color: var(--accent-cyan);
    text-decoration: none;
  }
  .contact-item a:hover { text-decoration: underline; }

  .giscus {
    margin-top: 1rem;
    min-height: 150px;
  }
</style>
