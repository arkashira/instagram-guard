import pytest
from src.recovery_flow import RecoveryFlow, RecoveryAttempt
from datetime import datetime, timedelta

def test_create_recovery_link():
    flow = RecoveryFlow()
    link = flow.create_recovery_link("user1", "user1@example.com")
    assert isinstance(link, str)

def test_verify_recovery_link():
    flow = RecoveryFlow()
    link = flow.create_recovery_link("user1", "user1@example.com")
    assert flow.verify_recovery_link(link.split("=")[1])

def test_verify_expired_link():
    flow = RecoveryFlow()
    link = flow.create_recovery_link("user1", "user1@example.com")
    flow.attempts[0].link_expires_at = datetime.now() - timedelta(minutes=16)
    assert not flow.verify_recovery_link(link.split("=")[1])

def test_verify_invalid_link():
    flow = RecoveryFlow()
    assert not flow.verify_recovery_link("invalid_link")
