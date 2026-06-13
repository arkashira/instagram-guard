# Technical Specification – Instagram Guard

## 1. Overview

**Instagram Guard** is a lightweight Python library that protects Instagram accounts from brute‑force attacks by implementing an adaptive lockout and recovery mechanism.  
The library is designed to be:

- **Stateless** – all state is kept in an in‑memory store that can be swapped for a persistent backend if needed.
- **Extensible** – new lockout policies, notification channels, or recovery flows can be added without touching the core logic.
- **Test‑driven** – the repository contains a full `pytest` suite covering all public APIs.

The component is intended to be dropped into any Python application that needs to guard Instagram credentials, e.g. a web scraper, a bot framework, or a CI pipeline that manages multiple accounts.

---

## 2. Architecture

```
┌───────────────────────┐
│   InstagramGuard API  │
│  (public interface)   │
└─────────────┬─────────┘
              │
              ▼
┌───────────────────────┐
│   LockoutEngine        │
│  (core logic)          │
└───────┬───────┬────────┘
        │       │
        ▼       ▼
┌─────────────┐ ┌───────────────────────┐
│  Store      │ │  Notification Service │
│  (in‑memory)│ │  (email / webhook)    │
└─────────────┘ └───────────────────────┘
```

### 2.1 Components

| Component | Responsibility | Key Classes / Functions |
|-----------|----------------|--------------------------|
| **InstagramGuard** | Public API exposed to callers. Handles session creation, login attempts, verification, and status queries. | `InstagramGuard`, `login_attempt`, `verify_account`, `get_lockout_status` |
| **LockoutEngine** | Implements the lockout policy: counting failures, timing windows, lockout duration, and recovery. | `LockoutEngine`, `record_attempt`, `is_locked`, `unlock` |
| **Store** | Persists lockout state in memory. Can be swapped for a database or Redis. | `InMemoryStore`, `AccountState` |
| **Notification Service** | Sends email notifications when an account is locked. (Optional – stubbed in tests.) | `EmailNotifier` |

---

## 3. Data Model

```python
class AccountState(BaseModel):
    username: str
    failed_attempts: int = 0
    first_failure_ts: Optional[float] = None
    locked_until: Optional[float] = None
    verified: bool = False
```

* `failed_attempts` – number of consecutive failures in the current window.  
* `first_failure_ts` – timestamp of the first failure in the current window.  
* `locked_until` – epoch timestamp until which the account remains locked.  
* `verified` – flag set when the user verifies via email.

All timestamps are stored as `float` epoch seconds (UTC).

---

## 4. Public APIs

| Method | Signature | Description |
|--------|-----------|-------------|
| `login_attempt(username: str, password: str) -> bool` | Returns `True` if login succeeds, `False` otherwise. Triggers lockout logic. |
| `verify_account(username: str, verification_token: str) -> bool` | Verifies the account using a token sent via email. Unlocks the account if successful. |
| `get_lockout_status(username: str) -> Dict[str, Any]` | Returns a dict with keys: `locked`, `locked_until`, `failed_attempts`, `verified`. |

All methods raise `ValueError` for unknown usernames or malformed inputs.

---

## 5. Policy Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MAX_FAILURES` | 5 | Consecutive failures allowed before lockout. |
| `WINDOW_SECONDS` | 600 (10 min) | Time window for counting failures. |
| `LOCKOUT_SECONDS` | 1800 (30 min) | Duration of automatic lockout. |
| `EMAIL_VERIFICATION_ENABLED` | `True` | If `True`, a verification email is sent on lockout. |

Parameters are configurable via the constructor of `InstagramGuard` or via environment variables.

---

## 6. Tech Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Language** | Python 3.11+ | Modern async support, type hints, widespread ecosystem. |
| **Data Validation** | Pydantic | Robust data models, easy JSON serialization. |
| **Testing** | pytest + pytest‑asyncio | Fast, expressive test framework. |
| **Email** | `smtplib` (stubbed in tests) | Minimal dependency; can be swapped for SendGrid, SES, etc. |
| **Packaging** | Poetry | Dependency management, reproducible builds. |
| **CI** | GitHub Actions | Automated linting, type‑checking, and test runs. |

---

## 7. Dependencies

```toml
[tool.poetry.dependencies]
python = "^3.11"
pydantic = "^2.0"

[tool.poetry.dev-dependencies]
pytest = "^7.0"
pytest-asyncio = "^0.21.0"
```

All dependencies are open‑source and permissively licensed (MIT/Apache‑2.0).

---

## 8. Deployment & Runtime

1. **Installation**

   ```bash
   pip install instagram-guard
   ```

2. **Configuration**

   ```python
   from instagram_guard import InstagramGuard

   guard = InstagramGuard(
       max_failures=5,
       window_seconds=600,
       lockout_seconds=1800,
       email_sender="no-reply@example.com",
       smtp_server="smtp.example.com",
       smtp_port=587,
       smtp_user="user",
       smtp_pass="pass",
   )
   ```

3. **Usage Example**

   ```python
   success = guard.login_attempt("user123", "wrongpass")
   if not success:
       status = guard.get_lockout_status("user123")
       print(status)
   ```

4. **Running Tests**

   ```bash
   pytest
   ```

5. **Production Considerations**

   * Replace `InMemoryStore` with a Redis or database backed store for multi‑process safety.  
   * Use a real email service (SendGrid, SES) instead of the stub.  
   * Expose the API via a lightweight FastAPI wrapper if needed.

---

## 9. Extensibility

| Feature | Extension Point | Implementation Hint |
|---------|-----------------|---------------------|
| Custom lockout policy | Override `LockoutEngine` | Subclass and replace `record_attempt` logic. |
| Alternative notification | Swap `EmailNotifier` | Provide a `Notifier` interface; inject via constructor. |
| Persistence | Replace `InMemoryStore` | Implement `Store` interface with Redis or SQLAlchemy. |

---

## 10. Security & Compliance

* Passwords are never stored; only the result of a login attempt is processed.  
* All timestamps are UTC to avoid time‑zone issues.  
* Email verification tokens are generated using `secrets.token_urlsafe(32)` and have a 15‑minute expiry.  
* The library does not log sensitive data; all logs are sanitized.

---

## 11. Roadmap (Future Enhancements)

1. **Rate‑limit per IP** – track IP addresses to mitigate distributed attacks.  
2. **Adaptive lockout** – increase lockout duration after repeated breaches.  
3. **Webhook notifications** – allow external systems to react to lockouts.  
4. **CLI tool** – quick manual lock/unlock for admins.  

--- 

*Prepared by the Instagram Guard Engineering Team – 2026‑06‑13*
