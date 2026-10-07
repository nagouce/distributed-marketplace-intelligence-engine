# ⚡ Distributed Multi-Marketplace Intelligence & Deal Arbitrage Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Linux Compatible](https://img.shields.io/badge/platform-Linux%20%7C%20POSIX-green.svg)](https://www.kernel.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade, high-throughput data extraction and real-time deal arbitrage engine written in Python and architected for continuous **24/7 Linux daemon environments**.

---

## 🏗️ Architectural Overview

The engine monitors, extracts, deduplicates, and scores product feeds and trending arbitrage signals from major e-commerce platforms (Shopee, Mercado Libre, Amazon) without relying on resource-heavy headless browsers.

┌────────────────────────────────────────────────────────┐
│               Autonomous Ingestion Daemon              │
│        (POSIX-Compliant / Graceful Signal Handler)     │
└───────────────────────────┬────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Shopee API    │   │ Mercado Libre │   │ Amazon Feed   │
│ Engine        │   │ Engine        │   │ Engine        │
│ (TLS Spoof)   │   │ (REST Parser) │   │ (Signature)   │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
        ┌───────────────────────────────────────┐
        │  Relational Storage & Indexing Engine │
        │   - Sub-millisecond composite indices │
        │   - ACID composite unique deduplication│
        └───────────────────┬───────────────────┘
                            ▼
        ┌───────────────────────────────────────┐
        │    Distribution & Webhook Workers     │
        │    (Multi-channel Alert Dispatcher)   │
        └───────────────────────────────────────┘

⚡ Core Engineering Features
Advanced Anti-Bot Evasion (TLS/JA3/JA4 Fingerprinting): Utilizes curl_cffi to spoof Chrome TLS fingerprints at the C-socket level, bypassing Cloudflare, Akamai, and Datadome defenses with minimal CPU/RAM overhead (<150MB RSS).
Private API Reverse Engineering: Ingests raw JSON payloads directly from internal marketplace endpoints rather than parsing dynamic HTML DOMs.
ACID Deduplication & Sub-Millisecond Indexing: SQLite relational schema designed with composite unique constraints (produto_id, marketplace, data_fila) and temporal indexes (idx_fila_status) for instant queue lookups.
POSIX Daemon Resiliency: Integrated SIGINT / SIGTERM signal traps ensuring complete data flush and safe connection termination during systemd restarts or container updates.
📊 Database Schema & Query Optimization
The pipeline utilizes custom composite indexes tailored for concurrent read/write locks and queue processing:

SQL

CREATE INDEX idx_fila_status ON fila_postagem(status, data_fila);
CREATE INDEX idx_fila_posicao ON fila_postagem(posicao, data_fila);
CREATE INDEX idx_hist_modelo ON historico_disparos(modelo_hash, enviado_em);
CREATE INDEX idx_hist_produto ON historico_disparos(produto_id, marketplace, enviado_em);
🚀 Quick Start
1. Requirements
Linux / macOS (POSIX-compliant)
Python 3.10+
SQLite 3
2. Installation
Bash

git clone https://github.com/nagouce/distributed-marketplace-intelligence-engine.git
cd distributed-marketplace-intelligence-engine
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
3. Run the Autonomous Daemon
Bash

python3 src/orchestrator/radar.py
👨‍💻 Author
Nag — Backend & Data Scraping Engineer
Specialized in high-throughput web scraping, API reverse-engineering, and autonomous Linux daemons.
