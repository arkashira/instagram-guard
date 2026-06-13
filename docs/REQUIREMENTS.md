```markdown
# Requirements

## Functional Requirements

**FR-1: Account Lockout Mechanism**
- The system shall lock an account after 5 consecutive failed login attempts within a 10-minute window.

**FR-2: Lockout Duration**
- The system shall enforce a 30-minute lockout period for locked accounts.

**FR-3: Email Verification for Early Unlock**
- The system shall allow users to verify their account via email to unlock the account before the 30-minute lockout period expires.

**FR-4: Lockout Status Persistence**
- The system shall persist the lockout status in memory and reflect it in the UI.

**FR-5: Login Attempt Tracking**
- The system shall track consecutive failed login attempts and reset the count after a successful login or after the 10-minute window expires.

**FR-6: User Verification**
- The system shall provide a method for users to verify their account via email.

**FR-7: Lockout Status Query**
- The system shall provide a method to query the current lockout status of an account.

## Non-Functional Requirements

**Performance Requirements**
- **NFR-1: Response Time**
  - The system shall respond to login attempts within 200 milliseconds under normal load conditions.

- **NFR-2: Throughput**
  - The system shall handle at least 1000 login attempts per minute.

**Security Requirements**
- **NFR-3: Data Protection**
  - The system shall ensure that all user data, including lockout status and verification tokens, are stored securely in memory.

- **NFR-4: Secure Communication**
  - The system shall use secure communication channels for sending and receiving verification emails.

**Reliability Requirements**
- **NFR-5: System Availability**
  - The system shall be available 99.9% of the time.

- **NFR-6: Fault Tolerance**
  - The system shall gracefully handle and recover from system failures without data loss.

## Constraints

**C-1: Technology Stack**
- The system shall be implemented in Python.

**C-2: Testing Framework**
- The system shall use `pytest` for testing.

**C-3: Memory Persistence**
- The system shall persist lockout status in memory and not rely on external databases.

## Assumptions

**A-1: Email Verification**
- The system assumes that the email verification process is handled by an external service and that the system receives a confirmation upon successful verification.

**A-2: User Interface**
- The system assumes that the UI will be implemented separately and will interact with the `InstagramGuard` class to reflect the lockout status.

**A-3: Time Synchronization**
- The system assumes that the server's clock is synchronized and accurate for tracking lockout durations and login attempt windows.
```
