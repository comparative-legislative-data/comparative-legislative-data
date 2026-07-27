<script lang="ts">
  import { X, Send, CheckCircle2, ShieldCheck } from 'lucide-svelte';

  let { isOpen = $bindable(false) } = $props();

  let name = $state('');
  let email = $state('');
  let institutionRole = $state('');
  let researchReason = $state('');
  let isSubmitting = $state(false);
  let errorMessage = $state('');
  let successMessage = $state('');

  function closeModal() {
    isOpen = false;
    errorMessage = '';
    successMessage = '';
  }

  async function handleSubmit(e: SubmitEvent) {
    e.preventDefault();
    if (!name || !email || !institutionRole || !researchReason) {
      errorMessage = 'Please fill out all required fields.';
      return;
    }

    isSubmitting = true;
    errorMessage = '';
    successMessage = '';

    try {
      const res = await fetch('/api/v1/auth/request-access', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name,
          email,
          institution_role: institutionRole,
          research_reason: researchReason
        })
      });

      const data = await res.json();
      if (!res.ok) {
        errorMessage = data.error || 'Failed to submit request.';
      } else {
        successMessage = data.message || 'Request submitted successfully!';
        name = '';
        email = '';
        institutionRole = '';
        researchReason = '';
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
          <ShieldCheck size={20} class="text-cyan" />
          <h3>Request Beta Tester Access</h3>
        </div>
        <button class="btn-close" onclick={closeModal} aria-label="Close modal">
          <X size={18} />
        </button>
      </div>

      <p class="modal-subtitle">
        Access to demonstrative data trends and the <strong>Quad-Studio Data Playground</strong> is currently restricted to approved beta testers. Submit your research details below for review.
      </p>

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
        <form onsubmit={handleSubmit} class="request-form">
          <div class="form-group">
            <label for="req-name">Full Name *</label>
            <input id="req-name" type="text" bind:value={name} placeholder="e.g. Dr. Jane Doe" required />
          </div>

          <div class="form-group">
            <label for="req-email">Institutional Email *</label>
            <input id="req-email" type="email" bind:value={email} placeholder="e.g. j.doe@university.ac.uk" required />
          </div>

          <div class="form-group">
            <label for="req-role">Role / Position *</label>
            <input id="req-role" type="text" bind:value={institutionRole} placeholder="e.g. Associate Professor / PhD Researcher" required />
          </div>

          <div class="form-group">
            <label for="req-reason">Research Intent / Reason for Access *</label>
            <textarea id="req-reason" rows="3" bind:value={researchReason} placeholder="Briefly describe how you intend to use the legislative dataset..." required></textarea>
          </div>

          <div class="form-actions">
            <button type="button" class="btn-secondary" onclick={closeModal}>Cancel</button>
            <button type="submit" class="btn-primary" disabled={isSubmitting}>
              {#if isSubmitting}
                <span>Submitting...</span>
              {:else}
                <Send size={15} />
                <span>Submit Request</span>
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
    max-width: 520px;
    padding: 1.5rem;
    color: #f8fafc;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
  }
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
  }
  .header-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .header-title h3 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #ffffff;
  }
  .text-cyan { color: #38bdf8; }
  .btn-close {
    background: transparent;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    padding: 0.25rem;
  }
  .btn-close:hover { color: #ffffff; }
  .modal-subtitle {
    font-size: 0.875rem;
    color: #94a3b8;
    margin-bottom: 1.25rem;
    line-height: 1.4;
  }
  .alert {
    padding: 0.75rem 1rem;
    border-radius: 6px;
    font-size: 0.875rem;
    margin-bottom: 1rem;
  }
  .alert-error {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #fca5a5;
  }
  .alert-success {
    background: rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(34, 197, 94, 0.4);
    color: #86efac;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .request-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }
  .form-group label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #cbd5e1;
  }
  .form-group input, .form-group textarea {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 0.6rem 0.75rem;
    color: #ffffff;
    font-size: 0.875rem;
  }
  .form-group input:focus, .form-group textarea:focus {
    outline: none;
    border-color: #38bdf8;
  }
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.75rem;
    margin-top: 0.5rem;
  }
  .btn-secondary {
    background: transparent;
    border: 1px solid #334155;
    color: #94a3b8;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.875rem;
  }
  .btn-secondary:hover { color: #ffffff; background: rgba(255,255,255,0.05); }
  .btn-primary {
    background: #0284c7;
    border: none;
    color: #ffffff;
    padding: 0.5rem 1.25rem;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.875rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }
  .btn-primary:hover:not(:disabled) { background: #0369a1; }
  .btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
