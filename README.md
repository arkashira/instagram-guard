# Instagram Guard
A simple Python project that implements an adaptive account lockout and recovery system for Instagram.

## Features
* Account lockout after 5 consecutive failed login attempts within 10 minutes
* Lockout duration of 30 minutes unless user verifies via email
* Lockout status persisted in memory and reflected in the UI

## Usage
1. Create an instance of the `InstagramGuard` class
2. Call the `login_attempt` method to simulate a login attempt
3. Call the `verify_account` method to verify an account
4. Call the `get_lockout_status` method to get the lockout status of an account

## Testing
Run the tests using `pytest` to ensure the implementation is correct.
