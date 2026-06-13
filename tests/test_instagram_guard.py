from src.instagram_guard import InstagramGuard, Account
import pytest
from datetime import datetime, timedelta

def test_login_attempt_success():
    guard = InstagramGuard()
    assert guard.login_attempt(1) == True

def test_login_attempt_lockout():
    guard = InstagramGuard()
    guard.accounts[1] = Account(id=1, lockout_status=False, failed_attempts=4, last_attempt_time=datetime.now())
    assert guard.login_attempt(1) == True

def test_login_attempt_lockout_duration():
    guard = InstagramGuard()
    guard.accounts[1] = Account(id=1, lockout_status=True, failed_attempts=5, last_attempt_time=datetime.now() - timedelta(minutes=31))
    assert guard.login_attempt(1) == True

def test_verify_account():
    guard = InstagramGuard()
    guard.accounts[1] = Account(id=1, lockout_status=True, failed_attempts=5, last_attempt_time=datetime.now())
    assert guard.verify_account(1) == True
    assert guard.get_lockout_status(1) == False

def test_get_lockout_status():
    guard = InstagramGuard()
    guard.accounts[1] = Account(id=1, lockout_status=True, failed_attempts=5, last_attempt_time=datetime.now())
    assert guard.get_lockout_status(1) == True
