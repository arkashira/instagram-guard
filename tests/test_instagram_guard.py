import pytest
from src.instagram_guard import InstagramGuard, RecoveryAttempt
import json
from datetime import datetime, timedelta

def test_send_recovery_email():
    guard = InstagramGuard()
    user_id = "example_user"
    link = guard.send_recovery_email(user_id)
    assert link.startswith("https://example.com/recover/")

def test_verify_link():
    guard = InstagramGuard()
    user_id = "example_user"
    link = guard.send_recovery_email(user_id)
    success = guard.verify_link(link, user_id)
    assert success

def test_log_recovery_attempt():
    guard = InstagramGuard()
    user_id = "example_user"
    guard.log_recovery_attempt(user_id, True)
    assert user_id in guard.recovery_attempts
    assert len(guard.recovery_attempts[user_id]) == 1
    attempt = guard.recovery_attempts[user_id][0]
    assert isinstance(attempt, RecoveryAttempt)
    assert attempt.user_id == user_id
    assert attempt.success

def test_expired_link():
    guard = InstagramGuard()
    user_id = "example_user"
    link = guard.send_recovery_email(user_id)
    # Simulate an expired link
    token = link.split("/")[-1]
    token_data = json.loads(token)
    token_data["expires"] = (datetime.now() - timedelta(minutes=15)).isoformat()
    link = f"https://example.com/recover/{user_id}/{json.dumps(token_data)}"
    success = guard.verify_link(link, user_id)
    assert not success
