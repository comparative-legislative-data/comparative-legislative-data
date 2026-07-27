# Comparative Legislative Data — Operations & VPS Access Guide

This document contains operational procedures, SSH access profiles, systemd service commands, Nginx configurations, and deployment steps for the **Comparative Legislative Data Platform**.

---

## 1. VPS Host & SSH Access Profile

* **Server IP:** `45.152.161.153`
* **Domain Name:** `https://legislativedata.org` (and `https://www.legislativedata.org`)
* **SSH Host Alias:** `chessserver`
* **SSH Config Entry (`~/.ssh/config`):**
  ```ssh
  Host chessserver
      HostName 45.152.161.153
      User chessadmin
      IdentityFile ~/.ssh/chess_server_private_key
      IdentitiesOnly yes
  ```

### Direct Terminal SSH Command
```bash
# Connect to VPS shell
ssh chessserver

# Run remote diagnostic command directly
ssh chessserver "sudo systemctl status compdata-frontend.service --no-pager"
```

---

## 2. Live Application Stack & Systemd Services

* **Frontend Location on VPS:** `/home/chessadmin/comparativelegislativedata/frontend`
* **Node.js Execution:** `/usr/local/bin/node build` (Port: `3100`, Host: `127.0.0.1`)
* **Systemd Service Unit:** `/etc/systemd/system/compdata-frontend.service`

### Useful Systemd Commands
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

* **Nginx Configuration:** `/etc/nginx/sites-available/legislativedata.org`
* **Enabled Symlink:** `/etc/nginx/sites-enabled/legislativedata.org`
* **Cloudflare SSL/TLS Mode:** **`Full`** (Nginx listens on port `80` and `443` with `/etc/ssl/certs/ssl-cert-snakeoil.pem`).

### Useful Nginx Commands
```bash
# Test Nginx configuration syntax
ssh chessserver "sudo nginx -t"

# Reload Nginx without downtime
ssh chessserver "sudo systemctl reload nginx"
```

---

## 4. Local Deployment Workflow

To build and deploy code updates to `https://legislativedata.org`:

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Build production Node.js bundle
npm run check
npm run build

# 3. Sync compiled build to VPS
rsync -avz --delete build/ chessserver:/home/chessadmin/comparativelegislativedata/frontend/build/

# 4. Restart Systemd service
ssh chessserver "sudo systemctl restart compdata-frontend.service"

# 5. Verify live status
curl -sI https://legislativedata.org
```

---

## 5. PostgreSQL Database Operations

* **PostgreSQL Service Name:** `postgresql@16-bills.service`
* **Database Name:** `comparative_legislative_data`
* **Port:** `5432`

### Database Access Commands
```bash
# Check PostgreSQL status
ssh chessserver "sudo systemctl status postgresql@16-bills.service --no-pager"

# Connect to database via psql
ssh chessserver "sudo -u postgres psql -d comparative_legislative_data"
```
