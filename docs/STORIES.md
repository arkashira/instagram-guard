```markdown
# STORIES.md

## Epic: Core Lockout System

### Story: Implement Basic Lockout Mechanism
**As a** security engineer
**I want** to implement a basic lockout mechanism that locks an account after 5 failed login attempts within 10 minutes
**So that** I can prevent brute force attacks on Instagram accounts

**Acceptance Criteria:**
- [ ] Account is locked after 5 consecutive failed login attempts within 10 minutes
- [ ] Lockout duration is set to 30 minutes
- [ ] Lockout status is persisted in memory

### Story: Verify Account via Email
**As a** security engineer
**I want** to implement an email verification system to allow users to verify their account and unlock it immediately
**So that** legitimate users can regain access to their accounts quickly

**Acceptance Criteria:**
- [ ] Users can request an email verification link
- [ ] Email verification link is sent to the user's registered email address
- [ ] Account is unlocked immediately upon successful verification

### Story: Reflect Lockout Status in UI
**As a** UX designer
**I want** to display the lockout status to the user in the UI
**So that** users are informed about their account status

**Acceptance Criteria:**
- [ ] Lockout status is displayed in the UI
- [ ] UI shows the remaining time until the lockout expires
- [ ] UI provides an option to request an email verification link

## Epic: Advanced Features

### Story: Persist Lockout Status
**As a** backend developer
**I want** to persist the lockout status in a database
**So that** the lockout status is maintained even after the application restarts

**Acceptance Criteria:**
- [ ] Lockout status is stored in a database
- [ ] Lockout status is retrieved from the database on application startup
- [ ] Lockout status is updated in the database after each login attempt or verification

### Story: Implement Rate Limiting
**As a** security engineer
**I want** to implement rate limiting to prevent multiple lockout attempts from the same IP address
**So that** I can prevent automated attacks on the lockout system

**Acceptance Criteria:**
- [ ] Multiple lockout attempts from the same IP address are rate-limited
- [ ] Rate limiting is applied after a configurable number of lockout attempts
- [ ] Rate limiting duration is configurable

### Story: Add Logging and Monitoring
**As a** DevOps engineer
**I want** to add logging and monitoring for the lockout system
**So that** I can track and analyze lockout events

**Acceptance Criteria:**
- [ ] All lockout events are logged
- [ ] Logs include the account ID, timestamp, and reason for lockout
- [ ] Monitoring system alerts on suspicious lockout patterns

## Epic: User Experience

### Story: Provide Clear Feedback to Users
**As a** UX designer
**I want** to provide clear feedback to users about their lockout status and next steps
**So that** users understand what happened and how to regain access

**Acceptance Criteria:**
- [ ] Users receive a clear message when their account is locked
- [ ] Message includes the remaining lockout time and instructions for verification
- [ ] Users receive a confirmation message upon successful verification

### Story: Implement Self-Service Unlock
**As a** product manager
**I want** to implement a self-service unlock feature that allows users to unlock their account without email verification
**So that** users can regain access quickly if they remember their password

**Acceptance Criteria:**
- [ ] Users can request a self-service unlock
- [ ] Users are prompted to enter their password for verification
- [ ] Account is unlocked immediately upon successful password verification

## Epic: Testing and Validation

### Story: Write Unit Tests for Lockout Mechanism
**As a** QA engineer
**I want** to write unit tests for the lockout mechanism
**So that** I can ensure the lockout system works as expected

**Acceptance Criteria:**
- [ ] Unit tests cover all scenarios of the lockout mechanism
- [ ] Unit tests are run automatically as part of the CI pipeline
- [ ] Unit tests pass successfully

### Story: Write Integration Tests for Email Verification
**As a** QA engineer
**I want** to write integration tests for the email verification system
**So that** I can ensure the email verification system works as expected

**Acceptance Criteria:**
- [ ] Integration tests cover all scenarios of the email verification system
- [ ] Integration tests are run automatically as part of the CI pipeline
- [ ] Integration tests pass successfully

### Story: Write End-to-End Tests for User Flow
**As a** QA engineer
**I want** to write end-to-end tests for the user flow
**So that** I can ensure the entire user flow works as expected

**Acceptance Criteria:**
- [ ] End-to-end tests cover all user flows, including lockout and verification
- [ ] End-to-end tests are run automatically as part of the CI pipeline
- [ ] End-to-end tests pass successfully
```
