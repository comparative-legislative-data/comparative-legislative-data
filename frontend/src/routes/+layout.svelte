<script lang="ts">
  import '../app.css';
  import { Database, Globe, FileCode2, Layers, BookOpen, Mail, ShieldAlert, LogIn, User, KeyRound, UserCheck, ShieldCheck } from 'lucide-svelte';
  import { page } from '$app/state';

  import RequestAccessModal from '$lib/components/RequestAccessModal.svelte';
  import AdminPanelModal from '$lib/components/AdminPanelModal.svelte';
  import LoginModal from '$lib/components/LoginModal.svelte';
  import UserSettingsModal from '$lib/components/UserSettingsModal.svelte';
  import SetPasswordModal from '$lib/components/SetPasswordModal.svelte';

  let { children, data } = $props();

  let user = $derived(data?.user || page.data?.user || null);

  let isRequestAccessOpen = $state(false);
  let isAdminPanelOpen = $state(false);
  let isLoginOpen = $state(false);
  let isUserSettingsOpen = $state(false);
  let isSetPasswordOpen = $state(false);
  let verifiedUser = $state<any>(null);

  let canonicalUrl = $derived(`https://legislativedata.org${page.url.pathname}`);

  $effect(() => {
    // Check url search params for verify_signup or magic_login
    if (page.url.searchParams.has('action') && page.url.searchParams.has('token')) {
      const action = page.url.searchParams.get('action');
      const token = page.url.searchParams.get('token');
      const email = page.url.searchParams.get('email');

      if (token && email && (action === 'verify_signup' || action === 'magic_login')) {
        verifyTokenAndLogin(token, email, action);
      }
    }
  });

  async function verifyTokenAndLogin(token: string, email: string, action: string) {
    try {
      const res = await fetch('/api/v1/auth/verify-token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, email })
      });
      const resData = await res.json();
      if (res.ok) {
        // Clean URL parameters
        window.history.replaceState({}, '', page.url.pathname);
        if (action === 'verify_signup') {
          verifiedUser = resData.user;
          isSetPasswordOpen = true; // Open dedicated Set Password modal
        } else {
          window.location.reload();
        }
      }
    } catch (e) {
      console.error('Failed to verify token:', e);
    }
  }

  async function handleLogout() {
    await fetch('/api/v1/auth/logout', { method: 'POST' });
    window.location.reload();
  }

  const organizationSchema = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    'name': 'Comparative Legislative Data Project',
    'url': 'https://legislativedata.org',
    'logo': 'https://legislativedata.org/favicon.svg',
    'email': 'comparativelegislativedata@gmail.com',
    'description': 'An open academic research infrastructure standardising, auditing, and mapping quantitative legislative data across international parliamentary and presidential assemblies.'
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
  <meta name="twitter:description" content="Global Open Parliamentary Data Audit & Mapping Atlas establishing clean, harmonised foundations for comparative legislative research." />

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
          <span class="brand-sub">Research Infrastructure & Mapping Atlas</span>
        </div>
      </a>

      <nav class="main-nav">
        <span class="nav-link text-muted" style="cursor: not-allowed; opacity: 0.6;">
          <Database size={16} /> Native Explorer (Offline)
        </span>
        
        <!-- Auth & Admin Controls -->
        {#if user?.is_super_user}
          <button class="btn-auth btn-admin" onclick={() => isAdminPanelOpen = true}>
            <ShieldAlert size={15} /> Admin Panel
          </button>
        {/if}

        {#if user}
          <button class="btn-auth btn-user-pill" onclick={() => isUserSettingsOpen = true}>
            <UserCheck size={15} class="text-cyan" /> {user.name}
          </button>
          <button class="btn-auth btn-logout" onclick={handleLogout}>
            Log Out
          </button>
        {:else}
          <button class="btn-auth btn-request" onclick={() => isRequestAccessOpen = true}>
            <ShieldCheck size={15} /> Request Access
          </button>
          <button class="btn-auth btn-login" onclick={() => isLoginOpen = true}>
            <LogIn size={15} /> Log In
          </button>
        {/if}

        <a href="https://github.com/comparative-legislative-data/comparative-legislative-data" target="_blank" rel="noopener noreferrer" class="nav-link nav-github">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"></path><path d="M9 18c-4.51 2-5-2-7-2"></path></svg> GitHub
        </a>
      </nav>
    </div>
  </header>

  <!-- Modals -->
  <RequestAccessModal bind:isOpen={isRequestAccessOpen} />
  <AdminPanelModal bind:isOpen={isAdminPanelOpen} />
  <LoginModal bind:isOpen={isLoginOpen} />
  <UserSettingsModal bind:isOpen={isUserSettingsOpen} {user} />
  <SetPasswordModal bind:isOpen={isSetPasswordOpen} user={verifiedUser} />

  <!-- Main Content Body -->
  <main>
    {@render children()}
  </main>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="container footer-content">
      <div class="footer-col">
        <div class="brand-title">Comparative Legislative Data Platform</div>
        <p class="footer-desc">An open academic research infrastructure standardising, auditing, and mapping quantitative legislative data across international parliamentary and presidential assemblies.</p>
        <p class="copyright">&copy; 2026 Comparative Legislative Data Project. Hosted at <a href="https://legislativedata.org" class="footer-link">legislativedata.org</a> under OGL v3.0 / Open Parliament Licence v3.0.</p>
      </div>

      <div class="footer-col">
        <h4>Platform Navigation</h4>
        <ul>
          <li><span class="text-muted">Navigation disabled during Rebuild</span></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Academic Contact & GitHub</h4>
        <ul>
          <li>
            <a href="https://github.com/comparative-legislative-data/comparative-legislative-data" target="_blank" rel="noopener noreferrer" class="footer-icon-link">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"></path><path d="M9 18c-4.51 2-5-2-7-2"></path></svg> GitHub Organization Repository
            </a>
          </li>
          <li>
            <a href="mailto:comparativelegislativedata@gmail.com" class="footer-icon-link">
              <Mail size={14} /> comparativelegislativedata@gmail.com
            </a>
          </li>
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
    gap: 1.5rem;
  }

  .nav-link {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    color: var(--text-muted);
    font-size: 0.875rem;
    font-weight: 500;
    text-decoration: none;
    transition: color 0.2s ease;
  }

  .nav-link:hover {
    color: var(--text-main);
  }

  .nav-github {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border-subtle);
    padding: 0.35rem 0.75rem;
    border-radius: 0.375rem;
  }
  .nav-github:hover {
    background: rgba(255, 255, 255, 0.1);
    color: #ffffff;
  }

  .btn-auth {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.35rem 0.75rem;
    border-radius: 0.375rem;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .btn-admin {
    background: rgba(234, 179, 8, 0.15);
    border: 1px solid rgba(234, 179, 8, 0.4);
    color: #fde047;
  }
  .btn-admin:hover { background: rgba(234, 179, 8, 0.25); color: #ffffff; }

  .btn-request {
    background: rgba(56, 189, 248, 0.15);
    border: 1px solid rgba(56, 189, 248, 0.4);
    color: #38bdf8;
  }
  .btn-request:hover { background: rgba(56, 189, 248, 0.25); color: #ffffff; }

  .btn-login {
    background: transparent;
    border: 1px solid var(--border-subtle);
    color: var(--text-muted);
  }
  .btn-login:hover { color: #ffffff; background: rgba(255, 255, 255, 0.08); }

  .btn-user-pill {
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid #334155;
    color: #ffffff;
  }
  .btn-user-pill:hover { border-color: #38bdf8; }

  .btn-logout {
    background: transparent;
    border: none;
    color: #94a3b8;
  }
  .btn-logout:hover { color: #fca5a5; }

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
    line-height: 1.5;
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

  .footer-icon-link {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
  }

  @media (max-width: 768px) {
    .main-nav { display: none; }
    .footer-content { grid-template-columns: 1fr; gap: 2rem; }
  }
</style>
