<script lang="ts">
  import { X, KeyRound, CheckCircle2, ShieldCheck, User } from 'lucide-svelte';

  let { isOpen = $bindable(false), user = null } = $props();

  let password = $state('');
  let confirmPassword = $state('');
  let isSubmitting = $state(false);
  let errorMessage = $state('');
  let successMessage = $state('');

  function closeModal() {
    isOpen = false;
    password = '';
    confirmPassword = '';
    errorMessage = '';
    successMessage = '';
  }

  async function handleSetPassword(e: SubmitEvent) {
    e.preventDefault();
    if (!password || password.length < 6) {
      errorMessage = 'Password must be at least 6 characters long.';
      return;
    }

    if (password !== confirmPassword) {
      errorMessage = 'Passwords do not match.';
      return;
    }

    isSubmitting = true;
    errorMessage = '';
    successMessage = '';

    try {
      const res = await fetch('/api/v1/auth/set-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: user?.email,
          password
        })
      });

      const data = await res.json();
      if (!res.ok) {
        errorMessage = data.error || 'Failed to set password.';
      } else {
        successMessage = data.message || 'Password set successfully!';
        setTimeout(() => {
          closeModal();
          window.location.reload();
        }, 800);
      }
    } catch (err: any) {
      errorMessage = 'Network error setting password.';
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
          <ShieldCheck size={22} class="text-cyan" />
          <h3>Welcome! Set Up Your Password</h3>
        </div>
        <button class="btn-close" onclick={closeModal} aria-label="Close modal">
          <X size={18} />
        </button>
      </div>

      <p class="modal-subtitle">
        Your beta access request has been approved! Please choose a password for your account to complete setup.
      </p>

      <div class="account-details-box">
        <div class="detail-row">
          <span class="d-label">Account Name:</span>
          <span class="d-val">{user?.name || 'Approved Beta Tester'}</span>
        </div>
        <div class="detail-row">
          <span class="d-label">Account Email:</span>
          <span class="d-val text-cyan">{user?.email || '—'}</span>
        </div>
        {#if user?.role}
          <div class="detail-row">
            <span class="d-label">Institution / Role:</span>
            <span class="d-val">{user.role}</span>
          </div>
        {/if}
      </div>

      {#if errorMessage}
        <div class="alert alert-error">{errorMessage}</div>
      {/if}

      {#if successMessage}
        <div class="alert alert-success">
          <CheckCircle2 size={18} />
          <span>{successMessage}</span>
        </div>
      {/if}

      {#if !successMessage}
        <form onsubmit={handleSetPassword} class="password-form">
          <div class="form-group">
            <label for="setup-pass">Create Account Password *</label>
            <input id="setup-pass" type="password" bind:value={password} placeholder="At least 6 characters" required />
          </div>

          <div class="form-group">
            <label for="confirm-setup-pass">Confirm Password *</label>
            <input id="confirm-setup-pass" type="password" bind:value={confirmPassword} placeholder="Re-enter password" required />
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary" disabled={isSubmitting}>
              {#if isSubmitting}
                <span>Setting Password...</span>
              {:else}
                <KeyRound size={15} />
                <span>Save Password & Log In</span>
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
    border: 1px solid rgba(56, 189, 248, 0.3);
    border-radius: 12px;
    width: 100%;
    max-width: 460px;
    padding: 1.5rem;
    color: #f8fafc;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8);
  }
  .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
  .header-title { display: flex; align-items: center; gap: 0.5rem; }
  .header-title h3 { margin: 0; font-size: 1.15rem; font-weight: 600; color: #ffffff; }
  .text-cyan { color: #38bdf8; }
  .btn-close { background: transparent; border: none; color: #94a3b8; cursor: pointer; }
  .modal-subtitle { font-size: 0.85rem; color: #94a3b8; margin-bottom: 1rem; line-height: 1.4; }

  .account-details-box {
    background: #1e293b;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    font-size: 0.825rem;
  }
  .detail-row { display: flex; justify-content: space-between; align-items: center; }
  .d-label { color: #94a3b8; }
  .d-val { font-weight: 600; color: #ffffff; }

  .alert { padding: 0.75rem 1rem; border-radius: 6px; font-size: 0.85rem; margin-bottom: 1rem; }
  .alert-error { background: rgba(239, 68, 68, 0.15); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.4); }
  .alert-success { background: rgba(34, 197, 94, 0.15); color: #86efac; border: 1px solid rgba(34, 197, 94, 0.4); display: flex; align-items: center; gap: 0.5rem; }

  .password-form { display: flex; flex-direction: column; gap: 1rem; }
  .form-group { display: flex; flex-direction: column; gap: 0.35rem; }
  .form-group label { font-size: 0.8rem; font-weight: 600; color: #cbd5e1; }
  .form-group input { background: #1e293b; border: 1px solid #334155; border-radius: 6px; padding: 0.6rem 0.75rem; color: #ffffff; font-size: 0.875rem; }
  .form-group input:focus { outline: none; border-color: #38bdf8; }

  .form-actions { display: flex; justify-content: flex-end; margin-top: 0.5rem; }
  .btn-primary { background: #0284c7; border: none; color: #ffffff; padding: 0.6rem 1.25rem; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 0.875rem; display: flex; align-items: center; gap: 0.4rem; width: 100%; justify-content: center; }
  .btn-primary:hover:not(:disabled) { background: #0369a1; }
  .btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
