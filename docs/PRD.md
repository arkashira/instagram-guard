# Instagram Guard – Product Requirements Document (PRD)

**Document Version:** 1.0  
**Last Updated:** 2026‑06‑13  
**Owner:** Senior Product/Engineering Lead, Axentx  
**Stakeholders:** Security Team, Backend Engineering, UI/UX, QA, Customer Success  

---

## 1. Problem Statement  

Instagram accounts are vulnerable to credential‑stuffing and brute‑force attacks. Current Instagram APIs provide only basic rate‑limiting, leaving developers who embed Instagram login flows with no out‑of‑the‑box protection. This results in:

* Increased risk of account takeover for end‑users.  
* Higher support tickets for “my account is locked” or “I’m being spam‑locked”.  
* Lost trust in third‑party applications that rely on Instagram authentication.

**Goal:** Deliver a lightweight, adaptive lockout & recovery library (`instagram-guard`) that developers can drop into any Python‑based Instagram login integration to mitigate brute‑force attacks while preserving a good user experience.

---

## 2. Target Users  

| Segment | Description | Primary Pain |
|---------|-------------|--------------|
| **Third‑party app developers** | Build bots, analytics dashboards, or social‑media management tools that authenticate Instagram users. | Need a plug‑and‑play security layer without managing their own state store. |
| **Security engineers** | Evaluate security controls for client‑facing authentication flows. | Require configurable, auditable lockout policies. |
| **Product managers** | Want to reduce support churn caused by compromised accounts. | Need measurable reduction in brute‑force incidents. |

---

## 3. Success Metrics  

| Metric | Target (12 mo) | Measurement Method |
|--------|----------------|--------------------|
| **Reduction in brute‑force login attempts** | ≥ 70 % drop for customers using Instagram Guard | Log aggregation of failed attempts before/after integration. |
| **False‑positive lockouts** | ≤ 2 % of legitimate login sessions | Survey of support tickets + automated UI flow tests. |
| **Adoption rate** | 30 % of active Instagram‑integrating customers | Package download stats (PyPI) + internal usage telemetry. |
| **Time to recover** | ≤ 5 minutes for verified users | End‑to‑end test harness measuring lockout → verification → unlock. |
| **Developer satisfaction** | ≥ 4.5 / 5 rating on PyPI & internal feedback | Rating collection via GitHub Issues & post‑release survey. |

---

## 4. Scope  

### In‑Scope (MVP)

1. **Adaptive Lockout Engine**  
   * Detect 5 consecutive failed login attempts within a rolling 10‑minute window.  
   * Trigger a lockout for 30 minutes by default.  

2. **Recovery via Email Verification**  
   * Expose `verify_account(email_token)` API to lift lockout instantly.  
   * Generate a time‑limited (15 min) verification token and send via configurable email backend (SMTP or SendGrid).  

3. **In‑Memory Persistence**  
   * Store lockout state in a thread‑safe in‑memory store (Python `dict` + `threading.Lock`).  
   * Provide `get_lockout_status(username)` returning `{locked: bool, expires_at: datetime}`.  

4. **Public Python Package**  
   * Distribute on PyPI (`instagram-guard>=1.0.0`).  
   * Include type hints, comprehensive docstrings, and a `README.md` with quick‑start guide.  

5. **Testing & CI**  
   * 100 % unit‑test coverage (pytest).  
   * GitHub Actions pipeline: lint (ruff), type check (mypy), security scan (bandit).  

### Out‑of‑Scope (Future Phases)

| Feature | Reason |
|---------|--------|
| Persistent storage (Redis, DB) | MVP focuses on low‑friction adoption; persistence will be added for multi‑process deployments in Phase 2. |
| Multi‑factor authentication (MFA) integration | Separate product line; Guard remains a lockout/recovery layer only. |
| Real‑time UI widgets | Guard provides status via API; UI components will be built by consuming apps. |
| Rate‑limiting across IPs or device fingerprints | Future enhancement; initial release only tracks per‑username attempts. |
| Analytics dashboard | Out of scope for library; customers can export logs to their own observability stack. |

---

## 5. Key Features (Prioritized)

| Priority | Feature | Description | Acceptance Criteria |
|----------|---------|-------------|----------------------|
| **P1** | **Lockout Trigger** | Detect 5 failed attempts in 10 min per username. | - `login_attempt(username, success=False)` increments counter.<br>- After 5th failure, `get_lockout_status` returns `locked=True` with `expires_at` ≈ now+30 min. |
| **P1** | **Automatic Unlock after Timeout** | Unlock automatically when lockout period expires. | - After 30 min, `get_lockout_status` returns `locked=False` without external action. |
| **P1** | **Email Verification Flow** | Generate token, send email, unlock on valid token. | - `verify_account(username, token)` returns success only if token matches and not expired.<br>- Account unlocks immediately on success. |
| **P2** | **Configurable Policies** | Allow callers to set `max_attempts`, `window_minutes`, `lockout_minutes`. | - Constructor accepts optional `policy` dict; behavior matches supplied values. |
| **P2** | **Pluggable Email Backend** | Abstract email sender for SMTP, SendGrid, etc. | - Provide `EmailSender` interface; default implementation uses SMTP. |
| **P3** | **Thread‑Safe & Async Support** | Safe operation in async frameworks (e.g., FastAPI). | - Library works with `asyncio` via `await guard.login_attempt_async(...)`. |
| **P3** | **Metrics Export** | Emit Prometheus counters for attempts, lockouts, recoveries. | - `/metrics` endpoint optional via `export_metrics(port)`. |

---

## 6. User Journeys  

1. **Developer Integration**  
   *Add library → instantiate `InstagramGuard(policy=…)` → wrap existing login logic with `guard.login_attempt(username, success)`.*  

2. **Brute‑Force Attack**  
   *Attacker fails 5 times → guard locks account → UI shows “Account locked. Check email to unlock.”*  

3. **User Recovery**  
   *User clicks email link → token sent to backend → `guard.verify_account(username, token)` → lock cleared → user can log in again.*  

4. **Automatic Expiration**  
   *If user ignores email, lock expires after 30 min → next login attempt succeeds.*  

---

## 7. Technical Requirements  

| Requirement | Detail |
|-------------|--------|
| **Language** | Python 3.10+ |
| **Packaging** | `setup.cfg` + `pyproject.toml` (PEP 517) |
| **Dependencies** | `pydantic>=2.0`, `email-validator`, optional `aiosmtplib` for async email |
| **Security** | All tokens generated with `secrets.token_urlsafe(32)`; stored only in memory; no logging of tokens. |
| **Performance** | O(1) per login attempt; memory footprint < 2 KB per active username. |
| **Observability** | Optional Prometheus client (`prometheus_client`). |
| **Documentation** | Auto‑generated API docs via `mkdocs` + `mkdocstrings`. |
| **Compliance** | No personal data persisted beyond email token; complies with GDPR (no long‑term storage). |

---

## 8. Milestones & Timeline  

| Milestone | Deliverable | Owner | Target Date |
|-----------|-------------|-------|-------------|
| **M1 – Requirements Freeze** | Final PRD sign‑off | PM | 2026‑06‑20 |
| **M2 – Core Engine** | Lockout detection & in‑memory store | Backend Lead | 2026‑07‑05 |
| **M3 – Email Verification** | Token generation, SMTP sender, API | Backend Lead | 2026‑07‑12 |
| **M4 – Packaging & CI** | PyPI publish pipeline, tests, lint | DevOps | 2026‑07‑19 |
| **M5 – Documentation & Samples** | README, quick‑start, API docs | Docs Engineer | 2026‑07‑22 |
| **M6 – Beta Release** | v0.1.0 to internal partners | Release Manager | 2026‑07‑31 |
| **M7 – Public Launch** | v1.0.0 on PyPI, marketing blog | Marketing | 2026‑08‑15 |
| **M8 – Post‑Launch Review** | Metrics collection, roadmap planning | PM | 2026‑09‑30 |

---

## 9. Risks & Mitigations  

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **In‑memory state loss** (process restart) | Users may be unexpectedly unlocked | Medium | Document that persistence is future work; provide graceful fallback to “no lock”. |
| **Email delivery failures** | Users cannot recover | Low | Allow custom email backend; expose callback for delivery status. |
| **Token brute‑force** | Account takeover | Low | Use 256‑bit tokens, rate‑limit verification attempts (max 3 per 5 min). |
| **Performance bottleneck under high concurrency** | Latency spikes | Low | Use lock‑free data structures (`collections.defaultdict` + `threading.RLock`); benchmark in load tests. |
| **Regulatory compliance** (email handling) | Legal exposure | Low | Store only token & expiry; no personal data; provide opt‑out hook. |

---

## 10. Open Questions  

1. Should we expose a webhook for external systems to be notified on lockout/recovery events?  
2. Is there demand for a Redis‑backed persistence layer in the initial release?  
3. What branding (logo, naming) is required for the public PyPI package?  

*Answers to be resolved in the next sprint planning session.*

--- 

*Prepared by:*  
**[Your Name]** – Senior Product/Engineering Lead, Axentx  
*Approved by:*  
**[Stakeholder Sign‑off]**  

---
