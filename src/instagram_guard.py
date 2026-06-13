import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict

@dataclass
class User:
    id: int
    email: str
    locked: bool = False

class InstagramGuard:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.recovery_links: Dict[str, User] = {}
        self.recovery_attempts: Dict[str, int] = {}

    def lock_account(self, user_id: int):
        if user_id in self.users:
            self.users[user_id].locked = True
            return True
        return False

    def generate_recovery_link(self, user_id: int) -> str:
        if user_id in self.users:
            link = f"{user_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            self.recovery_links[link] = self.users[user_id]
            return link
        return ""

    def verify_recovery_link(self, link: str) -> bool:
        if link in self.recovery_links:
            user = self.recovery_links[link]
            if (datetime.now() - datetime.strptime(link.split('-')[1], '%Y%m%d%H%M%S')).total_seconds() <= 900:
                del self.recovery_links[link]
                user.locked = False
                return True
            else:
                del self.recovery_links[link]
        return False

    def log_recovery_attempt(self, link: str):
        if link in self.recovery_attempts:
            self.recovery_attempts[link] += 1
        else:
            self.recovery_attempts[link] = 1

    def send_recovery_email(self, user_id: int):
        link = self.generate_recovery_link(user_id)
        if link:
            return f"Recovery link: {link}"
        return "Failed to generate recovery link"

    def add_user(self, user_id: int, email: str):
        self.users[user_id] = User(user_id, email)
