<script lang="ts">
  import '../app.css';
  import { Database, Globe, FileCode2, Layers } from 'lucide-svelte';
  import { page } from '$app/state';

  let { children } = $props();

  let canonicalUrl = $derived(`https://legislativedata.org${page.url.pathname}`);

  const organizationSchema = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    'name': 'Comparative Legislative Data Project',
    'url': 'https://legislativedata.org',
    'logo': 'https://legislativedata.org/favicon.svg',
    'description': 'An open academic research project mapping data availability, API access, and canonical schemas across international legislatures.'
  };

  const websiteSchema = {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    'name': 'Comparative Legislative Data Platform',
    'url': 'https://legislativedata.org',
    'description': 'Global Open Parliamentary Data Audit & Mapping Atlas for Comparative Legislative Research.'
  };
</script>

<svelte:head>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="manifest" href="/site.webmanifest" />
  <link rel="canonical" href={canonicalUrl} />

  <meta property="og:site_name" content="Comparative Legislative Data Platform" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content={canonicalUrl} />
  
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@LegislativeData" />
  <meta name="twitter:title" content="Comparative Legislative Data Platform" />
  <meta name="twitter:description" content="Global Open Parliamentary Data Audit & Mapping Atlas establishing clean, harmonised foundations for legislative research." />

  <!-- Global Structured Data (JSON-LD) -->
  {@html `<script type="application/ld+json">${JSON.stringify(organizationSchema)}</script>`}
  {@html `<script type="application/ld+json">${JSON.stringify(websiteSchema)}</script>`}
</svelte:head>

<div class="app-shell">
  <!-- Header Navigation -->
  <header class="site-header">
    <div class="container header-content">
      <a href="/" class="brand">
        <div class="brand-icon">
          <Database size={20} color="#6366f1" />
        </div>
        <div class="brand-text">
          <span class="brand-title">Comparative Legislative Data</span>
          <span class="brand-sub">Research Platform & Mapping Atlas</span>
        </div>
      </a>

      <nav class="main-nav">
        <a href="/atlas" class="nav-link">
          <Globe size={16} /> Data Atlas
        </a>
        <a href="/schema" class="nav-link">
          <Layers size={16} /> Schema
        </a>
        <a href="/api-docs" class="nav-link">
          <FileCode2 size={16} /> API & Bulk Data
        </a>
      </nav>
    </div>
  </header>

  <!-- Main Content Body -->
  <main>
    {@render children()}
  </main>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="container footer-content">
      <div class="footer-col">
        <div class="brand-title">Comparative Legislative Data Platform</div>
        <p class="footer-desc">An open research project mapping data availability, API access, and canonical schemas across international legislatures.</p>
        <p class="copyright">&copy; 2026 Comparative Legislative Data Project. Hosted at <a href="https://legislativedata.org" class="footer-link">legislativedata.org</a> under OGL v3.0 / Open Parliament Licence v3.0.</p>
      </div>

      <div class="footer-col">
        <h4>Project Structure</h4>
        <ul>
          <li><a href="/atlas">Parliament Data Atlas</a></li>
          <li><a href="/schema">Canonical Schema Specification</a></li>
          <li><a href="/api-docs">API Specification & Access</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Phase 0 BICD Focus</h4>
        <ul>
          <li><a href="/atlas/GB-UKP">UK Parliament (Westminster)</a></li>
          <li><a href="/atlas/GB-SCT">Scottish Parliament (Holyrood)</a></li>
          <li><a href="/atlas/GB-WLS">Senedd Cymru (Wales)</a></li>
          <li><a href="/atlas/GB-NIR">Northern Ireland Assembly</a></li>
          <li><a href="/atlas/IM-TYN">Isle of Man Tynwald</a></li>
        </ul>
      </div>
    </div>
  </footer>
</div>

<style>
  .app-shell {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  .site-header {
    background: var(--bg-glass);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid var(--border-subtle);
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 4.25rem;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    text-decoration: none;
  }

  .brand-icon {
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid var(--border-subtle);
    padding: 0.45rem;
    border-radius: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .brand-text {
    display: flex;
    flex-direction: column;
  }

  .brand-title {
    font-family: var(--font-heading);
    font-weight: 700;
    font-size: 1.05rem;
    color: #ffffff;
    line-height: 1.2;
  }

  .brand-sub {
    font-size: 0.725rem;
    color: var(--text-muted);
  }

  .main-nav {
    display: flex;
    align-items: center;
    gap: 1.75rem;
  }

  .nav-link {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    color: var(--text-muted);
    font-size: 0.9rem;
    font-weight: 500;
    text-decoration: none;
    transition: color 0.2s ease;
  }

  .nav-link:hover {
    color: var(--text-main);
  }

  main {
    flex: 1;
  }

  .site-footer {
    background: #070a12;
    border-top: 1px solid var(--border-subtle);
    padding: 3rem 0 2rem;
    margin-top: 4rem;
  }

  .footer-content {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    gap: 3rem;
  }

  .footer-desc {
    color: var(--text-muted);
    font-size: 0.85rem;
    margin: 0.75rem 0 1.25rem;
  }

  .copyright {
    color: var(--text-dim);
    font-size: 0.75rem;
  }

  .footer-link {
    color: var(--accent-cyan);
    text-decoration: none;
  }
  .footer-link:hover { text-decoration: underline; }

  .footer-col h4 {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-bottom: 1rem;
  }

  .footer-col ul {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .footer-col a {
    color: var(--text-muted);
    font-size: 0.85rem;
    text-decoration: none;
    transition: color 0.2s ease;
  }

  .footer-col a:hover {
    color: var(--accent-cyan);
  }

  @media (max-width: 768px) {
    .main-nav { display: none; }
    .footer-content { grid-template-columns: 1fr; gap: 2rem; }
  }
</style>
