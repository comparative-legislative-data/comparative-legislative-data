<script lang="ts">
  import { X, LogIn, Sparkles, KeyRound, CheckCircle2 } from 'lucide-svelte';

  let { isOpen = $bindable(false), onLoginSuccess = () => {} } = $props();

  let mode = $state<'LOGIN' | 'MAGIC_LINK'>('LOGIN');
  let email = $state('');
  let password = $state('');
  let isSubmitting = $state(false);
  let errorMessage = $state('');
  let successNotice = $state('');

  function closeModal() {
    isOpen = false;
    errorMessage = '';
    successNotice = '';
  }

  async function handleLogin(e: SubmitEvent) {
    e.preventDefault();
    if (!email || !password) {
      errorMessage = 'Please enter your email and password.';
      return;
    }

    isSubmitting = true;
    errorMessage = '';
    successNotice = '';

    try {
      const res = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (!res.ok) {
        errorMessage = data.error || 'Login failed.';
      } else {
        successNotice = 'Logged in successfully!';
        setTimeout(() => {
          closeModal();
          onLoginSuccess();
          window.location.reload();
        }, 600);
      }
    } catch (err: any) {
      errorMessage = 'Network error. Please try again.';
    } finally {
      isSubmitting = false;
    }
  }

  async function handleMagicLink(e: SubmitEvent) {
    e.preventDefault();
    if (!email) {
      errorMessage = 'Please enter your email address.';
      return;
    }

    isSubmitting = true;
    errorMessage = '';
    successNotice = '';

    try {
      const res = await fetch('/api/v1/auth/magic-link', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });
      const data = await res.json();
      if (!res.ok) {
        errorMessage = data.error || 'Failed to send Magic Link.';
      } else {
        successNotice = data.message || 'Magic Link sent! Please check your email inbox.';
      }
    } catch (err: any) {
      errorMessage = 'Network error. Please try again.';
    } finally {
      isSubmitting = false;
    }
  }
</script>

{#if isOpen}
  <div class="modal-backdrop" onclick={(e) => { if (e.target === e.currentTarget) closeModal(); }} role="presentation">
    <div class="modal-card" role="dialog" aria-modal="true">
      <div class="modal-header">
        <div class="header-title">
          <LogIn size={20} class="text-cyan" />
          <h3>{mode === 'LOGIN' ? 'Log In to Platform' : 'Passwordless Magic Link'}</h3>
        </div>
        <button class="btn-close" onclick={closeModal} aria-label="Close modal">
          <X size={18} />
        </button>
      </div>

      <div class="mode-tabs">
        <button class="tab-btn" class:active={mode === 'LOGIN'} onclick={() => { mode = 'LOGIN'; errorMessage = ''; successNotice = ''; }}>
          <KeyRound size={14} /> Password Login
        </button>
        <button class="tab-btn" class:active={mode === 'MAGIC_LINK'} onclick={() => { mode = 'MAGIC_LINK'; errorMessage = ''; successNotice = ''; }}>
          <Sparkles size={14} /> Magic Link Login
        </button>
      </div>

      {#if errorMessage}
        <div class="alert alert-error">{errorMessage}</div>
      {/if}

      {#if successNotice}
        <div class="alert alert-success">
          <CheckCircle2 size={16} />
          <span>{successNotice}</span>
        </div>
      {/if}

      {#if mode === 'LOGIN'}
        <form onsubmit={handleLogin} class="auth-form">
          <div class="form-group">
            <label for="login-email">Email Address</label>
            <input id="login-email" type="email" bind:value={email} placeholder="e.g. researcher@university.ac.uk" required />
          </div>

          <div class="form-group">
            <label for="login-password">Password</label>
            <input id="login-password" type="password" bind:value={password} placeholder="••••••••" required />
          </div>

          <div class="form-actions">
            <button type="button" class="btn-secondary" onclick={closeModal}>Cancel</button>
            <button type="submit" class="btn-primary" disabled={isSubmitting}>
              {#if isSubmitting}
                <span>Logging in...</span>
              {:else}
                <LogIn size={15} />
                <span>Log In</span>
              {/if}
            </button>
          </div>
        </form>
      {:else}
        <form onsubmit={handleMagicLink} class="auth-form">
          <p class="magic-info">
            Enter your email to receive a secure, one-time <strong>Magic Link</strong>. Clicking the link logs you in instantly without needing a password.
          </p>

          <div class="form-group">
            <label for="magic-email">Email Address</label>
            <input id="magic-email" type="email" bind:value={email} placeholder="e.g. researcher@university.ac.uk" required />
          </div>

          <div class="form-actions">
            <button type="button" class="btn-secondary" onclick={closeModal}>Cancel</button>
            <button type="submit" class="btn-primary" disabled={isSubmitting}>
              {#if isSubmitting}
                <span>Sending Link...</span>
              {:else}
                <Sparkles size={15} />
                <span>Email Magic Link</span>
              {/if}
            </button>
          </div>
        </form>
      {/if}
    </div>
  </div>
{/if}

<style>
  .modal-backdrop {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    padding: 1rem;
  }
  .modal-card {
    background: #0f172a;
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 12px;
    width: 100%;
    max-width: 440px;
    padding: 1.5rem;
    color: #f8fafc;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
  }
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }
  .header-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .header-title h3 {
    margin: 0;
    font-size: 1.15rem;
    font-weight: 600;
    color: #ffffff;
  }
  .text-cyan { color: #38bdf8; }
  .btn-close {
    background: transparent;
    border: none;
    color: #94a3b8;
    cursor: pointer;
  }
  .mode-tabs {
    display: flex;
    background: #1e293b;
    border-radius: 6px;
    padding: 0.25rem;
    margin-bottom: 1.25rem;
    gap: 0.25rem;
  }
  .tab-btn {
    flex: 1;
    background: transparent;
    border: none;
    color: #94a3b8;
    padding: 0.45rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.35rem;
  }
  .tab-btn.active {
    background: #0284c7;
    color: #ffffff;
  }
  .magic-info {
    font-size: 0.825rem;
    color: #94a3b8;
    line-height: 1.4;
    margin-bottom: 1rem;
  }
  .alert {
    padding: 0.75rem 1rem;
    border-radius: 6px;
    font-size: 0.85rem;
    margin-bottom: 1rem;
  }
  .alert-error { background: rgba(239, 68, 68, 0.15); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.4); }
  .alert-success { background: rgba(34, 197, 94, 0.15); color: #86efac; border: 1px solid rgba(34, 197, 94, 0.4); display: flex; align-items: center; gap: 0.5rem; }
  
  .auth-form { display: flex; flex-direction: column; gap: 1rem; }
  .form-group { display: flex; flex-direction: column; gap: 0.35rem; }
  .form-group label { font-size: 0.8rem; font-weight: 600; color: #cbd5e1; }
  .form-group input {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 0.6rem 0.75rem;
    color: #ffffff;
    font-size: 0.875rem;
  }
  .form-group input:focus { outline: none; border-color: #38bdf8; }
  .form-actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 0.5rem; }
  .btn-secondary { background: transparent; border: 1px solid #334155; color: #94a3b8; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; font-size: 0.85rem; }
  .btn-secondary:hover { color: #ffffff; background: rgba(255,255,255,0.05); }
  .btn-primary { background: #0284c7; border: none; color: #ffffff; padding: 0.5rem 1.25rem; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 0.85rem; display: flex; align-items: center; gap: 0.4rem; }
  .btn-primary:hover:not(:disabled) { background: #0369a1; }
  .btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
