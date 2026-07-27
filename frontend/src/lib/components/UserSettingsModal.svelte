<script lang="ts">
  import { X, Key, CheckCircle2, UserCheck } from 'lucide-svelte';

  let { isOpen = $bindable(false), user } = $props();

  let newPassword = $state('');
  let confirmPassword = $state('');
  let isSubmitting = $state(false);
  let errorMessage = $state('');
  let successMessage = $state('');

  function closeModal() {
    isOpen = false;
    newPassword = '';
    confirmPassword = '';
    errorMessage = '';
    successMessage = '';
  }

  async function handlePasswordChange(e: SubmitEvent) {
    e.preventDefault();
    if (!newPassword || newPassword.length < 6) {
      errorMessage = 'New password must be at least 6 characters long.';
      return;
    }

    if (newPassword !== confirmPassword) {
      errorMessage = 'Passwords do not match.';
      return;
    }

    isSubmitting = true;
    errorMessage = '';
    successMessage = '';

    try {
      const res = await fetch('/api/v1/auth/change-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_password: newPassword })
      });
      const data = await res.json();
      if (!res.ok) {
        errorMessage = data.error || 'Failed to update password.';
      } else {
        successMessage = data.message || 'Password updated successfully!';
        newPassword = '';
        confirmPassword = '';
      }
    } catch (err: any) {
      errorMessage = 'Network error updating password.';
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
          <UserCheck size={20} class="text-cyan" />
          <h3>User Settings & Security</h3>
        </div>
        <button class="btn-close" onclick={closeModal} aria-label="Close modal">
          <X size={18} />
        </button>
      </div>

      <div class="user-profile-summary">
        <div class="profile-item">
          <span class="p-label">Account Name:</span>
          <span class="p-val">{user?.name || 'Researcher'}</span>
        </div>
        <div class="profile-item">
          <span class="p-label">Account Email:</span>
          <span class="p-val">{user?.email}</span>
        </div>
        <div class="profile-item">
          <span class="p-label">Access Level:</span>
          <span class="p-val badge">{user?.is_super_user ? 'SUPER USER ADMIN' : 'APPROVED BETA TESTER'}</span>
        </div>
      </div>

      {#if errorMessage}
        <div class="alert alert-error">{errorMessage}</div>
      {/if}

      {#if successMessage}
        <div class="alert alert-success">
          <CheckCircle2 size={16} />
          <span>{successMessage}</span>
        </div>
      {/if}

      <form onsubmit={handlePasswordChange} class="settings-form">
        <h4 class="section-title"><Key size={14} /> Update Account Password</h4>
        <p class="section-desc">Enter a new password below. (Original password is not required).</p>

        <div class="form-group">
          <label for="new-pass">New Password *</label>
          <input id="new-pass" type="password" bind:value={newPassword} placeholder="At least 6 characters" required />
        </div>

        <div class="form-group">
          <label for="confirm-pass">Confirm New Password *</label>
          <input id="confirm-pass" type="password" bind:value={confirmPassword} placeholder="Re-enter new password" required />
        </div>

        <div class="form-actions">
          <button type="button" class="btn-secondary" onclick={closeModal}>Close</button>
          <button type="submit" class="btn-primary" disabled={isSubmitting}>
            {#if isSubmitting}
              <span>Updating...</span>
            {:else}
              <span>Update Password</span>
            {/if}
          </button>
        </div>
      </form>
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
    max-width: 480px;
    padding: 1.5rem;
    color: #f8fafc;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
  }
  .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
  .header-title { display: flex; align-items: center; gap: 0.5rem; }
  .header-title h3 { margin: 0; font-size: 1.15rem; font-weight: 600; color: #ffffff; }
  .text-cyan { color: #38bdf8; }
  .btn-close { background: transparent; border: none; color: #94a3b8; cursor: pointer; }

  .user-profile-summary {
    background: #1e293b;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    font-size: 0.825rem;
  }
  .profile-item { display: flex; justify-content: space-between; align-items: center; }
  .p-label { color: #94a3b8; }
  .p-val { color: #ffffff; font-weight: 600; }
  .badge { background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 0.15rem 0.4rem; border-radius: 4px; font-size: 0.7rem; }

  .alert { padding: 0.65rem 0.85rem; border-radius: 6px; font-size: 0.85rem; margin-bottom: 1rem; }
  .alert-error { background: rgba(239, 68, 68, 0.15); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.4); }
  .alert-success { background: rgba(34, 197, 94, 0.15); color: #86efac; border: 1px solid rgba(34, 197, 94, 0.4); display: flex; align-items: center; gap: 0.4rem; }

  .settings-form { display: flex; flex-direction: column; gap: 0.85rem; }
  .section-title { font-size: 0.9rem; font-weight: 600; color: #ffffff; margin: 0; display: flex; align-items: center; gap: 0.35rem; }
  .section-desc { font-size: 0.775rem; color: #94a3b8; margin: 0 0 0.5rem 0; }

  .form-group { display: flex; flex-direction: column; gap: 0.3rem; }
  .form-group label { font-size: 0.775rem; font-weight: 600; color: #cbd5e1; }
  .form-group input { background: #1e293b; border: 1px solid #334155; border-radius: 6px; padding: 0.55rem 0.75rem; color: #ffffff; font-size: 0.85rem; }
  .form-group input:focus { outline: none; border-color: #38bdf8; }

  .form-actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 0.5rem; }
  .btn-secondary { background: transparent; border: 1px solid #334155; color: #94a3b8; padding: 0.45rem 1rem; border-radius: 6px; cursor: pointer; font-size: 0.85rem; }
  .btn-secondary:hover { color: #ffffff; background: rgba(255,255,255,0.05); }
  .btn-primary { background: #0284c7; border: none; color: #ffffff; padding: 0.45rem 1.25rem; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 0.85rem; }
  .btn-primary:hover:not(:disabled) { background: #0369a1; }
  .btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
