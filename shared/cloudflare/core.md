# Cloudflare Platform Skill

Consolidated skill for building on the Cloudflare platform. Use decision trees below to find the right product, then load detailed references.

## Quick Decision Trees

### "I need to run code"

```
Need to run code?
├─ Serverless functions at the edge → Workers
├─ Full-stack web app with Git deploys → Pages
├─ Stateful coordination/real-time → Durable Objects
├─ Long-running multi-step jobs → Workflows
├─ Run containers → Containers
├─ Multi-tenant (customers deploy code) → Workers for Platforms
├─ Scheduled tasks (cron) → Cron Triggers
├─ Lightweight edge logic (modify HTTP) → Snippets
├─ Process Worker execution events (logs/observability) → Tail Workers
└─ Optimize latency to backend infrastructure → Smart Placement
```

### "I need to store data"

```
Need storage?
├─ Key-value (config, sessions, cache) → KV
├─ Relational SQL → D1 (SQLite) or Hyperdrive (existing Postgres/MySQL)
├─ Object/file storage (S3-compatible) → R2
├─ Message queue (async processing) → Queues
├─ Vector embeddings (AI/semantic search) → Vectorize
├─ Strongly-consistent per-entity state → Durable Objects (DO storage)
├─ Secrets management → Secrets Store
├─ Streaming ETL to R2 → Pipelines
└─ Persistent cache (long-term retention) → Cache Reserve
```

### "I need AI/ML"

```
Need AI?
├─ Run inference (LLMs, embeddings, images) → Workers AI
├─ Vector database for RAG/search → Vectorize
├─ Build stateful AI agents → Agents SDK
├─ Gateway for any AI provider (caching, routing) → AI Gateway
└─ AI-powered search widget → AI Search
```

### "I need networking/connectivity"

```
Need networking?
├─ Expose local service to internet → Tunnel
├─ TCP/UDP proxy (non-HTTP) → Spectrum
├─ WebRTC TURN server → TURN
├─ Private network connectivity → Network Interconnect
├─ Optimize routing → Argo Smart Routing
├─ Optimize latency to backend (not user) → Smart Placement
└─ Real-time video/audio → RealtimeKit or Realtime SFU
```

### "I need security"

```
Need security?
├─ Web Application Firewall → WAF
├─ DDoS protection → DDoS
├─ Bot detection/management → Bot Management
├─ API protection → API Shield
├─ CAPTCHA alternative → Turnstile
└─ Credential leak detection → WAF (managed ruleset)
```

### "I need media/content"

```
Need media?
├─ Image optimization/transformation → Images
├─ Video streaming/encoding → Stream
├─ Browser automation/screenshots → Browser Rendering
└─ Third-party script management → Zaraz
```

### "I need infrastructure-as-code"

```
Need IaC? → Pulumi, Terraform, or REST API
```

## Product Index

### Compute & Runtime

| Product               | Key Capability                     |
| --------------------- | --------------------------------- |
| Workers               | Serverless functions at the edge  |
| Pages                 | Full-stack web app hosting        |
| Pages Functions       | Serverless functions in Pages     |
| Durable Objects       | Stateful coordination & storage   |
| Workflows             | Long-running multi-step jobs      |
| Containers            | Container-based compute           |
| Workers for Platforms | Multi-tenant worker deployment    |
| Cron Triggers         | Scheduled task execution          |
| Tail Workers          | Worker execution event processing |
| Snippets              | Lightweight HTTP modification     |
| Smart Placement       | Latency-optimized routing         |

### Storage & Data

| Product         | Key Capability                |
| --------------- | ----------------------------- |
| KV              | Key-value storage             |
| D1              | SQLite-compatible relational  |
| R2              | S3-compatible object storage  |
| Queues          | Message queue for async work  |
| Hyperdrive      | Accelerated external DB access|
| DO Storage      | Strongly-consistent per-entity|
| Secrets Store   | Secret and key management     |
| Pipelines       | Streaming ETL to R2           |

### AI & Machine Learning

| Product    | Key Capability                   |
| ---------- | -------------------------------- |
| Workers AI | Serverless inference             |
| Vectorize  | Vector database for RAG/search   |
| Agents SDK | Stateful AI agent framework      |
| AI Gateway | Unified AI provider gateway      |
| AI Search  | AI-powered search widget         |

### Networking & Connectivity

| Product              | Key Capability                |
| -------------------- | ----------------------------- |
| Tunnel               | Expose local services securely|
| Spectrum             | TCP/UDP proxy                 |
| TURN                 | WebRTC TURN server            |
| Network Interconnect | Private network connectivity  |
| Argo Smart Routing   | Optimized network routing     |
| Workers VPC          | VPC for Workers               |

### Security

| Product         | Key Capability              |
| --------------- | --------------------------- |
| WAF             | Web Application Firewall    |
| DDoS Protection | DDoS mitigation             |
| Bot Management  | Bot detection and control   |
| API Shield      | API security                |
| Turnstile       | CAPTCHA alternative         |

### Media & Content

| Product           | Key Capability                |
| ----------------- | ----------------------------- |
| Images            | Image optimization            |
| Stream            | Video streaming               |
| Browser Rendering | Browser automation            |
| Zaraz             | Third-party script management |

### Developer Tools

| Product            | Key Capability                |
| ------------------ | ----------------------------- |
| Wrangler           | CLI for Cloudflare development|
| Miniflare          | Local Workers simulator       |
| C3                 | Create Cloudflare app         |
| Observability      | Logs and monitoring           |
| Analytics Engine   | Custom analytics              |
| Web Analytics      | Website analytics             |
