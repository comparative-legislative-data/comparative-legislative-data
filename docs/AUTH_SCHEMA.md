# Authentication & Access Control Schema

**Purpose:** This document specifies the beta access request pipeline, email verification, and session management architecture that survived the Phase 1 Purge. This architecture has been verified and remains the foundation for access control on the Comparative Legislative Data platform.

---

## 1. Beta Access Control Pipeline

The platform uses a gated beta access model to restrict analytical features.

1. **Access Request Submission:**
   - Users submit their Name, Email, Role, and Research Reason via the public `RequestAccessModal`.
   - Data is stored in the PostgreSQL `beta_access_requests` table.

2. **Super User Administration:**
   - Super User credentials (configured in `.env.local`) allow access to the `AdminPanelModal`.
   - Super Users can review, approve, or reject pending requests.

3. **Email Dispatch (Resend API):**
   - Upon approval, an automated email is dispatched via `access@legislativedata.org`.
   - The email contains a 72-hour one-time signup token link.

## 2. Authentication Flow

1. **Password Setup / Magic Link Verification:**
   - Users click the email link containing a `token`, `email`, and `action` (`verify_signup` or `magic_login`).
   - The frontend `+layout.svelte` intercepts these parameters and submits them to the `/api/v1/auth/verify-token` endpoint.
   - For new signups, this opens the `SetPasswordModal`.
   - For existing users requesting a magic link, this logs them directly into a session.

2. **Standard Login:**
   - Users can log in using their email and password via the `LoginModal`, authenticated against the `users` table.

## 3. Session Security & Token Lifecycle

* **Session Cookie:** 
  - Sessions are managed via an encrypted, `HttpOnly` cookie named `session`.
  - The cookie is parsed server-side in `hooks.server.ts`, which populates the SvelteKit `event.locals.user` object for route protection.
* **Signup Tokens:** SHA-256 hashed and stored in the `auth_tokens` table with a **72-hour** expiration.
* **Magic Link Tokens:** SHA-256 hashed and stored in the `auth_tokens` table with a **1-hour** expiration.

## 4. Preserved Database Tables

The following tables constitute the Auth Schema in the PostgreSQL database:
- `users`: Stores user credentials, roles, and password hashes.
- `auth_tokens`: Stores ephemeral tokens for signup and magic link flows.
- `beta_access_requests`: Stores pending and resolved beta applications.
