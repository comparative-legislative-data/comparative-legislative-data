<script lang="ts">
  import { X, ShieldAlert, Check, Ban, RefreshCw, Copy, CheckCheck } from 'lucide-svelte';

  let { isOpen = $bindable(false) } = $props();

  let requests = $state<any[]>([]);
  let isLoading = $state(false);
  let errorMessage = $state('');
  let successNotice = $state('');
  let copiedLinkId = $state<number | null>(null);

  $effect(() => {
    if (isOpen) {
      loadRequests();
    }
  });

  async function loadRequests() {
    isLoading = true;
    errorMessage = '';
    try {
      const res = await fetch('/api/v1/auth/admin/requests');
      const data = await res.json();
      if (!res.ok) {
        errorMessage = data.error || 'Failed to load requests.';
      } else {
        requests = data.requests || [];
      }
    } catch (err: any) {
      errorMessage = 'Network error fetching admin requests.';
    } finally {
      isLoading = false;
    }
  }

  function closeModal() {
    isOpen = false;
  }

  async function approveRequest(reqId: number) {
    errorMessage = '';
    successNotice = '';
    try {
      const res = await fetch('/api/v1/auth/admin/approve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ request_id: reqId })
      });
      const data = await res.json();
      if (!res.ok) {
        errorMessage = data.error || 'Failed to approve request.';
      } else {
        successNotice = data.message || 'Request approved successfully!';
        loadRequests();
      }
    } catch (err: any) {
      errorMessage = 'Network error approving request.';
    }
  }

  async function rejectRequest(reqId: number) {
    errorMessage = '';
    successNotice = '';
    try {
      const res = await fetch('/api/v1/auth/admin/reject', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ request_id: reqId })
      });
      const data = await res.json();
      if (!res.ok) {
        errorMessage = data.error || 'Failed to reject request.';
      } else {
        successNotice = 'Request rejected.';
        loadRequests();
      }
    } catch (err: any) {
      errorMessage = 'Network error rejecting request.';
    }
  }
</script>

{#if isOpen}
  <div class="modal-backdrop" onclick={(e) => { if (e.target === e.currentTarget) closeModal(); }} role="presentation">
    <div class="modal-card" role="dialog" aria-modal="true">
      <div class="modal-header">
        <div class="header-title">
          <ShieldAlert size={22} class="text-yellow" />
          <h3>Beta Access Administration Panel</h3>
        </div>
        <button class="btn-close" onclick={closeModal} aria-label="Close modal">
          <X size={18} />
        </button>
      </div>

      <div class="admin-toolbar">
        <span>Manage Beta Access Applications ({requests.length} Total)</span>
        <button class="btn-refresh" onclick={loadRequests} disabled={isLoading}>
          <RefreshCw size={13} class={isLoading ? 'spin' : ''} /> Refresh
        </button>
      </div>

      {#if errorMessage}
        <div class="alert alert-error">{errorMessage}</div>
      {/if}

      {#if successNotice}
        <div class="alert alert-success">{successNotice}</div>
      {/if}

      <div class="table-container">
        {#if isLoading && requests.length === 0}
          <div class="loading-state">Loading access requests...</div>
        {:else if requests.length === 0}
          <div class="empty-state">No access requests submitted yet.</div>
        {:else}
          <table class="admin-table">
            <thead>
              <tr>
                <th>Applicant</th>
                <th>Role & Institution</th>
                <th>Research Reason</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {#each requests as r}
                <tr>
                  <td>
                    <div class="applicant-name">{r.name}</div>
                    <div class="applicant-email">{r.email}</div>
                  </td>
                  <td>{r.institution_role}</td>
                  <td class="reason-cell">{r.research_reason}</td>
                  <td>
                    <span class="badge badge-{r.status.toLowerCase()}">{r.status}</span>
                  </td>
                  <td>
                    {#if r.status === 'PENDING'}
                      <div class="action-buttons">
                        <button class="btn-act btn-approve" onclick={() => approveRequest(r.request_id)} title="Approve & Send Signup Email">
                          <Check size={14} /> Approve
                        </button>
                        <button class="btn-act btn-reject" onclick={() => rejectRequest(r.request_id)} title="Reject Request">
                          <Ban size={14} /> Reject
                        </button>
                      </div>
                    {:else}
                      <span class="text-muted">—</span>
                    {/if}
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        {/if}
      </div>
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
    border: 1px solid rgba(234, 179, 8, 0.3);
    border-radius: 12px;
    width: 100%;
    max-width: 960px;
    max-height: 85vh;
    display: flex;
    flex-direction: column;
    padding: 1.5rem;
    color: #f8fafc;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8);
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
  .text-yellow { color: #eab308; }
  .btn-close {
    background: transparent;
    border: none;
    color: #94a3b8;
    cursor: pointer;
  }
  .admin-toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.875rem;
    color: #94a3b8;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #1e293b;
  }
  .btn-refresh {
    background: #1e293b;
    border: 1px solid #334155;
    color: #cbd5e1;
    padding: 0.35rem 0.75rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.35rem;
  }
  .btn-refresh:hover { color: #ffffff; background: #334155; }
  .spin { animation: spin 1s linear infinite; }
  @keyframes spin { 100% { transform: rotate(360deg); } }

  .alert {
    padding: 0.6rem 0.85rem;
    border-radius: 6px;
    font-size: 0.85rem;
    margin-bottom: 0.75rem;
  }
  .alert-error { background: rgba(239, 68, 68, 0.15); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.4); }
  .alert-success { background: rgba(34, 197, 94, 0.15); color: #86efac; border: 1px solid rgba(34, 197, 94, 0.4); }

  .table-container {
    overflow-y: auto;
    flex-grow: 1;
    border: 1px solid #1e293b;
    border-radius: 8px;
  }
  .loading-state, .empty-state {
    padding: 2rem;
    text-align: center;
    color: #94a3b8;
  }
  .admin-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
    text-align: left;
  }
  .admin-table th {
    background: #1e293b;
    color: #cbd5e1;
    padding: 0.75rem 1rem;
    font-weight: 600;
  }
  .admin-table td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #1e293b;
    vertical-align: top;
  }
  .applicant-name { font-weight: 600; color: #ffffff; }
  .applicant-email { font-size: 0.75rem; color: #38bdf8; }
  .reason-cell { max-width: 280px; color: #cbd5e1; font-size: 0.8rem; line-height: 1.3; }

  .badge {
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
  }
  .badge-pending { background: rgba(234, 179, 8, 0.15); color: #fde047; border: 1px solid rgba(234, 179, 8, 0.4); }
  .badge-approved { background: rgba(34, 197, 94, 0.15); color: #86efac; border: 1px solid rgba(34, 197, 94, 0.4); }
  .badge-rejected { background: rgba(239, 68, 68, 0.15); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.4); }

  .action-buttons { display: flex; gap: 0.4rem; }
  .btn-act {
    border: none;
    border-radius: 4px;
    padding: 0.3rem 0.6rem;
    font-size: 0.75rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
  .btn-approve { background: #16a34a; color: #ffffff; }
  .btn-approve:hover { background: #15803d; }
  .btn-reject { background: #dc2626; color: #ffffff; }
  .btn-reject:hover { background: #b91c1c; }
  .text-muted { color: #64748b; }
</style>
