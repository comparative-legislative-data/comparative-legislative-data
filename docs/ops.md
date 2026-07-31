# Operations & VPS Access Guide (General)

This document contains generic operational procedures, SSH access configurations, systemd service commands, Nginx templates, and deployment steps for the comparative legislative data platform.

---

## 1. VPS Host & SSH Access Profile

*   **Server IP:** `45.152.161.153`
*   **Domain Name:** `https://legislativedata.org` (and `https://www.legislativedata.org`)
*   **SSH Host Alias:** `chessserver`
*   **SSH Config Entry (`~/.ssh/config`):**
    ```ssh
    Host chessserver
        HostName 45.152.161.153
        User chessadmin
        IdentityFile ~/.ssh/chess_server_private_key
        IdentitiesOnly yes
    ```

### 1.1 VPS Hardware Specifications (Verified July 2026)
*   **Operating System:** Ubuntu Linux 24.04 LTS (kernel: `6.8.0-90-generic x86_64`)
*   **CPU Architecture:** x86_64
*   **System Memory (RAM):** **18.6 GB** (18,614 MB total, ~13.2 GB available under normal load)
*   **Swap Space:** **4.0 GB** (4,095 MB total)
*   **Disk Storage (SSD):** **387 GB** total storage on `/dev/sda1` root partition (Used: 36%, Available: 64%)

### Direct Terminal SSH Command
```bash
# Connect to VPS shell
ssh chessserver
```

---

## 2. Web Stack & systemd Services

*   **Host Port:** `3100` (Node SvelteKit build listens on localhost)
*   **Systemd Service Unit:** `/etc/systemd/system/compdata-frontend.service`

### Useful Systemd Service Commands
```bash
# Check frontend service status
ssh chessserver "sudo systemctl status compdata-frontend.service --no-pager"

# Restart frontend service
ssh chessserver "sudo systemctl restart compdata-frontend.service"

# View real-time application logs
ssh chessserver "sudo journalctl -u compdata-frontend.service -f -n 50"
```

---

## 3. Web Proxy & SSL Configuration (Nginx + Cloudflare)

*   **Nginx Configuration:** `/etc/nginx/sites-available/legislativedata.org`
*   **Enabled Symlink:** `/etc/nginx/sites-enabled/legislativedata.org`
*   **Cloudflare SSL/TLS Mode:** **`Full`** (Nginx listens on port `80` and `443` with standard certificates).

### Useful Nginx Commands
```bash
# Test Nginx configuration syntax
ssh chessserver "sudo nginx -t"

# Reload Nginx without downtime
ssh chessserver "sudo systemctl reload nginx"
```

---

## 4. Local Deployment Workflow

To sync updates and compile the SvelteKit application on the remote VPS, use the standard `rsync` workflow:

```bash
# 1. Sync source files to remote VPS (excluding local build and node_modules folders)
rsync -avz --exclude 'node_modules/' --exclude '.svelte-kit/' --exclude 'build/' --exclude '.env' --relative [local_files] chessserver:/home/chessadmin/comparativelegislativedata/

# 2. Compile Vite bundles and restart the web service on the server
ssh chessserver "export PATH=/home/chessadmin/.nvm/versions/node/v22.3.0/bin:\$PATH && cd /home/chessadmin/comparativelegislativedata/frontend && npm run build && sudo systemctl restart compdata-frontend.service"

# 3. Verify live status
curl -sI https://legislativedata.org
```

---

## 5. PostgreSQL Database Operations

*   **PostgreSQL Service Name:** `postgresql@16-bills.service` (Port: `5432`)

### Database Access Commands
```bash
# Check PostgreSQL status
ssh chessserver "sudo systemctl status postgresql@16-bills.service --no-pager"
```

For assembly-specific database names, automated ingestion script paths, and sessional directory locations, refer to the individual operational guides:
*   [Scottish Parliament (GB-SCT) Operations Specifics Guide](file:///home/steven/Documents/github/comparativelegislativedata/docs/gb-sct/ops.md)
