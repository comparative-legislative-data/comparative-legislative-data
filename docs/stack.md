# Final Technical Stack & Infrastructure Specification

This document serves as the **Single Source of Truth (SSOT)** for the technology stack, host infrastructure, hardware allocation, and software architecture for the **Comparative Legislative Data API**.

---

## 1. Architectural Strategy: VPS-Based Systemd Deployment

> [!IMPORTANT]
> **Final Architecture Decision**
> 
> The application is deployed directly to **Primary Host `EPYC-Server` (`45.152.161.153`)** using **Native Systemd User Isolation** (bypassing Docker overhead and volume permission friction).

### Key Architectural Rationale
1. **Unrestricted Ingestion & Scraping:** Continuous background execution without arbitrary serverless function timeouts (10s–60s).
2. **Raw Data Provenance Archiving:** Direct local NVMe storage of raw source JSON/XML payloads (`/data/raw/`) for academic reproducibility.
3. **High-Performance Embedded Analytics (DuckDB):** In-process OLAP queries for metric calculations ($EDS$) and automated Parquet export compilation.
4. **Zero Incremental Hosting Cost:** Utilizing existing capacity on primary server `45.152.161.153` (6 AMD EPYC cores, 11 GiB available RAM, 257 GiB available SSD space).

---

## 2. Technical Stack Specification

| Subsystem | Selected Technology | Role & Function |
| :--- | :--- | :--- |
| **Backend & Ingestion Engine** | **Python 3.11+ (FastAPI + Pydantic v2)** | Ingestion scrapers, Pydantic v2 schema validation (powered by native Rust `pydantic-core`), REST API endpoints. |
| **Primary Datastore** | **PostgreSQL 16** | Relational integrity for core entities (`Bill`, `Amendment`), JSONB raw payload storage, indexed API queries. |
| **Analytical & Export Engine** | **DuckDB (Embedded)** | In-process execution of complex comparative statistical queries and nightly generation of compressed `.parquet` / `.csv` bulk datasets. |
| **Frontend & Graphics** | **SvelteKit (Svelte 5)** | Lightweight, reactive web portal, interactive data visualisations (D3.js / LayerCake), API documentation, dataset downloads. |
| **Reverse Proxy & SSL** | **Caddy** | Automated Let's Encrypt SSL, HTTP/2 reverse proxy routing `api.comparativelegislativedata.org` $\rightarrow$ `127.0.0.1:8000`. |
| **Process Isolation** | **Native Systemd Services** | Unprivileged `compdata` Linux system user running isolated `.venv` processes. |

---

## 3. Audited Host Infrastructure Inventory

### Primary Production Host: `EPYC-Server` (`45.152.161.153` / `chessadmin`)
- **OS / Kernel:** Ubuntu 24.04.3 LTS / Kernel 6.8.0-90-generic x86_64.
- **CPU:** 6 vCPUs on **AMD EPYC 7763 64-Core Processor**.
- **RAM:** 18 GiB Total | **11 GiB Available**.
- **Disk:** 387 GiB SSD | **257 GiB Available**.
- **Role:** **Primary Production Host** for API backend, database, frontend, and bulk data distribution.

### Secondary / Staging Host: `HostbrrThreadripper` (`77.90.2.83` / `chess-analysis-worker`)
- **OS / Kernel:** Debian GNU/Linux 12 (bookworm) / Kernel 6.1.0-9-amd64.
- **CPU:** 3 vCPUs on **AMD Ryzen Threadripper PRO 9995WX 96-Cores**.
- **RAM:** 12 GiB Total | **4.5 GiB Available**.
- **Disk:** 150 GiB NVMe | **107 GiB Available**.
- **Role:** **Staging / Testing Host** and off-site target for nightly automated backups of raw payload archives (`/data/raw/`).

---

## 4. Hardware Resource Allocation & Footprint

| Phase | Target Scope | Active RAM Footprint | Disk Storage Requirement | Recommended Hardware Profile |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1 MVP (Shallow Pilot)** | 4–10 Parliaments, ~50k Bills | ~705 MB Peak | ~1 GB Raw Archive + ~100 MB Postgres | 1 vCPU \| 2 GB RAM \| 20 GB NVMe Disk |
| **Mature App (Phases 1–3)** | 20+ Parliaments, ~500k Bills, 3M+ Amendments | ~4.3 GB Peak | ~150 GB Raw Archive + ~15 GB Postgres | 4 vCPUs \| 8 GB RAM \| 200 GB NVMe Disk |

---

## 5. Performance Dynamics: Network I/O vs. CPU-Bound Compute

For legislative ingestion pipelines, execution speed is dominated by **HTTP Network Latency (30ms–200ms)** and **Source API Rate Limits** (10–50 requests/sec).

- **Python vs Go/Rust:** Language CPU overhead accounts for $< 5\%$ of total pipeline execution time.
- **Rust-Backed Validation:** Pydantic v2 delegates JSON parsing and schema validation directly to native Rust (`pydantic-core`).
- **C++ Analytics:** DuckDB executes analytical queries and Parquet compilation in C++ multi-threaded native code.

---

## Document Revision History

- **2026-07-21 (v2.0):** Finalised `docs/stack.md` as the Single Source of Truth for tech stack and host infrastructure.
- **2026-07-21 (v1.5):** Added audited VPS hosts (`EPYC-Server` primary, `HostbrrThreadripper` secondary).
