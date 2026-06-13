from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List
import json
import secrets

@dataclass
class RecoveryAttempt:
    user_id: str
    email: str
    link_expires_at: datetime
    link_secret: str

class RecoveryFlow:
    def __init__(self):
        self.attempts = []

    def create_recovery_link(self, user_id: str, email: str) -> str:
        link_expires_at = datetime.now() + timedelta(minutes=15)
        link_secret = secrets.token_urlsafe(16)
        attempt = RecoveryAttempt(user_id, email, link_expires_at, link_secret)
        self.attempts.append(attempt)
        return f"https://example.com/recover?secret={link_secret}"

    def verify_recovery_link(self, link_secret: str) -> bool:
        for attempt in self.attempts:
            if attempt.link_secret == link_secret and attempt.link_expires_at > datetime.now():
                return True
        return False
