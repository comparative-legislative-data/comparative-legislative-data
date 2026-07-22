# System Architecture & Infrastructure Specification

This document details the software architecture, system deployment topology, data flow pipelines, component responsibilities, operational monitoring, log pruning, backups, and API licensing/access control for the **Comparative Legislative Data API**.

---

## 1. System Architecture Overview

The system is deployed directly on **Primary VPS (`45.152.161.153`)** using **Native Linux Systemd Services** within a dedicated `compdata` unprivileged user environment.

It acts as an **Active Data Mirror & Harmonisation Engine**, ingesting raw legislative feeds into PostgreSQL and DuckDB datastores, and delivering dual-layer payloads (`normalized`, `native`, `provenance`) via native **Caddy**.

```
 ┌─────────────────────────────────────────────────────────────────────────────────────────┐
 │                            PRIMARY VPS: EPYC-Server (45.152.161.153)                    │
 │                                                                                         │
 │  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
 │  │                         Native Caddy Reverse Proxy (HTTPS)                        │  │
 │  └───────────────────────────┬───────────────────────────────────┬───────────────────┘  │
 │                              │                                   │                      │
 │                              ▼                                   ▼                      │
 │  ┌───────────────────────────────────────────────┐   ┌───────────────────────────────┐  │
 │  │      compdata-frontend.service (SvelteKit)    │   │  compdata-api.service (FastAPI│  │
 │  │    - Interactive Visualisations & Charts      │   │   - REST API & Key Rate Limit │  │
 │  │    - Dataset Download Portal                  │   │   - Prometheus Telemetry      │  │
 │  └───────────────────────────────────────────────┘   └───────────────┬───────────────┘  │
 │                                                                      │                  │
 │                                                  ┌───────────────────┴───────────────┐  │
 │                                                  ▼                                   ▼  │
 │                                  ┌───────────────────────────────┐   ┌───────────────┴──┐
 │                                  │     PostgreSQL Service        │   │  Local Directory │
 │                                  │  - Core Bills & Metadata      │   │  /data/raw/      │
 │                                  │  - Provenance & Scraper Logs  │   │  /data/parquet/  │
 │                                  └───────────────────────────────┘   └──────────────────┘
 └─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. API Access Control, Abuse Prevention & Commercial Tiering

API access is governed by FastAPI rate-limiting middleware (`X-API-Key` validation):

1. **Public / Explorer Tier (£0/mo):** 1,000 requests/day (10 req/min). Unauthenticated or public key.
2. **Academic & Student Tier (£0/mo Free):** 50,000 requests/day (100 req/min) + **Direct Bulk Parquet/CSV Downloads**. Auto-verified via `.ac.uk` / `.edu` email.
3. **Commercial Pro Tier (£49–£99/mo):** 500,000 requests/day (500 req/min), high-priority bandwidth, email support.
4. **Enterprise Tier (£299–£499/mo):** Unlimited API throughput, commercial SLAs, custom data extracts, live webhooks.

---

## 3. Observability, Pruning & Backup Integration

Detailed in [`docs/MONITORING.md`](file:///home/steven/Documents/github/comparativelegislativedata/docs/MONITORING.md):

1. **System & Infrastructure Metrics:** Host CPU/RAM, NVMe disk space (< 15 GB alert threshold), systemd process uptime.
2. **API RED Metrics:** Request rates, Error percentages (target 5xx < 0.01%), and Latency percentiles ($p_{50} < 15\text{ms}, p_{95} < 50\text{ms}$).
3. **ETL Scraper Audit Logging:** Structured `audit.jsonl` tracking validation accuracy, external status codes, and schema drift.
4. **Log Rotation & Pruning:** Systemd journal capped at 2 GB / 30 days; `logrotate` for `audit.jsonl` (30-day compressed rolling window).
5. **Nightly Off-Site Backups (`compdata-backup.service`):** Automated `pg_dump` of PostgreSQL + `rclone` incremental sync of raw payload archives (`/data/raw/`) to secondary VPS `HostbrrThreadripper` or S3/B2.

---

## 4. Legal & Commercial Licensing Compliance

1. **Underlying Source Licenses:** All ingested parliaments publish data under non-exclusive open licenses or public domain (Open Parliament Licence v3.0, OGL v3.0, US 17 U.S.C. § 105, dl-de/by-2-0), all of which explicitly authorize commercial redistribution.
2. **Value-Added Service:** Commercial tiers charge for high-availability SaaS API infrastructure, mirrored database uptime SLAs, calculated analytical metrics ($EDS$), and bulk export compiling, fully compliant with open data legal frameworks.

---

## Document Revision History

- **2026-07-22 (v0.6):** Added API Access Control, Commercial Tiering, and Licensing Compliance framework.
- **2026-07-21 (v0.5):** Added log pruning and nightly off-site backup specifications.
- **2026-07-21 (v0.1):** Initial architecture specification.
