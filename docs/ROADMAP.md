# ROADMAP.md – Instagram Guard

## Vision
Provide a lightweight, adaptive lockout & recovery layer that can be dropped into any Instagram‑related service (bots, analytics tools, third‑party clients) to protect accounts from credential‑stuffing and brute‑force attacks while preserving a smooth user experience.

---

## Milestones Overview

| Milestone | Target Release | Core Goal | MVP‑Critical Items |
|-----------|----------------|----------|--------------------|
| **MVP**   | **2026‑07‑15** | Deliver a **stable, test‑covered library** that can be imported and used out‑of‑the‑box for basic lockout/recovery. | ✅ Adaptive lockout logic  <br>✅ In‑memory persistence <br>✅ Public API (`login_attempt`, `verify_account`, `get_lockout_status`) <br>✅ Unit test suite (≥ 90 % coverage) <br>✅ CI pipeline (GitHub Actions) |
| **v1.0**  | 2026‑09‑30 | Harden production readiness and add extensibility points. | ✅ Configurable thresholds (attempts, window, lockout time) <br>✅ Pluggable storage back‑ends (Redis, SQLite) <br>✅ Email verification integration (SMTP/SendGrid) <br>✅ Detailed audit logging <br>✅ Documentation site (MkDocs) |
| **v2.0**  | 2026‑12‑15 | Expand ecosystem support and advanced security features. | ✅ Rate‑limit per IP & device fingerprinting <br>✅ Adaptive risk scoring (ML‑light model) <br>✅ Webhook callbacks for SIEM / incident response <br>✅ Docker image & Helm chart for easy deployment <br>✅ Compatibility layer for Instagram Graph API clients |

---

## MVP – Must‑Have for Launch (2026‑07‑15)

| Feature | Description | Acceptance Criteria |
|---------|-------------|----------------------|
| **Adaptive lockout logic** | After **5** failed attempts within **10 min**, account is locked. | - `login_attempt(username, success)` returns `locked=False` until threshold is hit.<br>- After threshold, `get_lockout_status(username)` reports `locked=True` and `unlock_time` 30 min in future. |
| **Lockout duration & recovery** | Locked accounts stay locked for **30 min** unless verified via email. | - `verify_account(username, token)` clears lockout immediately when a valid token is supplied.<br>- Invalid/expired token leaves lockout unchanged. |
| **In‑memory persistence** | State lives in a process‑wide dictionary; suitable for dev & CI. | - Restarting the process clears lockout (documented behavior). |
| **Public API** | `InstagramGuard` class exposing three methods. | - All three methods are type‑annotated, raise clear exceptions on misuse, and are covered by unit tests. |
| **Test suite** | Automated tests with **pytest**. | - ≥ 90 % line coverage.<br>- CI fails on coverage drop. |
| **CI/CD pipeline** | GitHub Actions run lint, tests, and build a wheel. | - Badge displayed in README.<br>- Artifacts published to GitHub Packages on tag. |

---

## v1.0 – Production Hardened (2026‑09‑30)

### Themes
1. **Configurability** – Let integrators tune security posture.
2. **Persistence & Scaling** – Move from volatile memory to durable stores.
3. **User‑Facing Recovery** – Real email verification flow.
4. **Observability** – Logs & metrics for ops teams.

### Feature List
| Theme | Feature | Detail |
|-------|---------|--------|
| Configurability | **Threshold parameters** | `max_attempts`, `window_minutes`, `lockout_minutes` configurable via constructor or env vars. |
| Persistence | **Redis backend** | Optional `RedisStore` implementing the same interface as the in‑memory store. |
| Persistence | **SQLite fallback** | Zero‑config file store for small deployments. |
| Recovery | **Email verification** | Generate a signed token, send via SMTP/SendGrid, validate in `verify_account`. |
| Observability | **Structured logging** | JSON logs with `username`, `event`, `timestamp`. |
| Observability | **Prometheus metrics** | Counters for attempts, lockouts, recoveries; gauge for current locked accounts. |
| Docs | **MkDocs site** | Installation, configuration, API reference, migration guide. |
| Release | **Wheel distribution** | Publish to PyPI under `instagram-guard`. |

---

## v2.0 – Advanced Security & Ecosystem (2026‑12‑15)

### Themes
1. **Risk‑Based Adaptive Controls** – Move beyond static thresholds.
2. **Integration & Automation** – Hook into existing security pipelines.
3. **Deployability** – Container‑first delivery.

### Feature List
| Theme | Feature | Detail |
|-------|---------|--------|
| Risk Scoring | **Lightweight ML model** | Input: IP reputation, device fingerprint, time‑of‑day. Output: risk score that adjusts lockout severity. |
| Rate Limiting | **IP & device throttling** | Separate counters per IP/device to block credential‑stuffing at the edge. |
| Automation | **Webhook callbacks** | POST JSON payload on lockout, unlock, verification to configurable URLs (SIEM, Slack, etc.). |
| Deployability | **Docker image** | Official `Dockerfile` publishing a minimal runtime image. |
| Deployability | **Helm chart** | Kubernetes deployment with ConfigMap for thresholds, Secret for email credentials. |
| Compatibility | **Instagram Graph API wrapper** | Helper utilities to inject guard checks into Graph API client calls. |
| Documentation | **Migration guide** | Steps to move from v1 (in‑memory/Redis) to v2 (risk model). |

---

## Release Process (All Milestones)

1. **Feature branch** → **Pull Request** with:
   - Unit tests
   - Updated docs
   - Lint (`ruff`) and type check (`mypy`) passing
2. **CI** runs:
   - `pytest --cov=instagram_guard`
   - `ruff check`
   - `mypy`
   - Build wheel & publish to GitHub Packages (tag‑only)
3. **Manual QA** on a fresh virtual environment:
   - Install wheel
   - Run integration script simulating lockout/recovery
4. **Tag** release (`vX.Y.Z`) → **GitHub Release** with changelog auto‑generated from PR titles.

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Email provider throttling | Users cannot recover | Support multiple providers; fallback to console token for dev. |
| Redis outage | Lockout state lost | Auto‑fallback to in‑memory with warning; optional persistence checkpoint. |
| False positives from risk model | Legit users locked out | Conservative default thresholds; allow admin override via API. |
| Dependency drift (vLLM, SGLang) | Security vulnerabilities | Pin versions, run `dependabot` weekly, run safety checks in CI. |

---

## Success Metrics

| Metric | Target (12 mo) |
|--------|----------------|
| Weekly active installations | 5 000 |
| Average lockout false‑positive rate | < 1 % |
| Mean time to recovery (email) | < 3 min |
| CI pass rate | 100 % |
| Documentation satisfaction (survey) | ≥ 4.5/5 |

--- 

*Prepared by the Instagram Guard product/engineering lead, 2026‑06‑13.*
