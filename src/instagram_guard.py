import json
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict

@dataclass
class RecoveryAttempt:
    """Represents a recovery attempt."""
    user_id: str
    attempt_time: datetime
    success: bool

class InstagramGuard:
    """Implements the adaptive account lockout and recovery system."""
    def __init__(self):
        self.recovery_attempts = {}

    def send_recovery_email(self, user_id: str) -> str:
        """Sends a recovery email with a single-click link that expires in 15 minutes."""
        link = f"https://example.com/recover/{user_id}/{self.generate_token()}"
        # Simulate sending an email
        logging.info(f"Sent recovery email to {user_id} with link {link}")
        return link

    def generate_token(self) -> str:
        """Generates a token that expires in 15 minutes."""
        return json.dumps({"expires": (datetime.now() + timedelta(minutes=15)).isoformat()})

    def verify_link(self, link: str, user_id: str) -> bool:
        """Verifies the recovery link and unlocks the account if valid."""
        try:
            token = link.split("/")[-1]
            token_data = json.loads(token)
            if token_data["expires"] < datetime.now().isoformat():
                return False
            # Simulate verifying the user's identity
            logging.info(f"Verified link for {user_id}")
            return True
        except Exception as e:
            logging.error(f"Error verifying link: {e}")
            return False

    def log_recovery_attempt(self, user_id: str, success: bool):
        """Logs the recovery attempt."""
        attempt = RecoveryAttempt(user_id, datetime.now(), success)
        if user_id not in self.recovery_attempts:
            self.recovery_attempts[user_id] = []
        self.recovery_attempts[user_id].append(attempt)
        logging.info(f"Logged recovery attempt for {user_id}")

def main():
    guard = InstagramGuard()
    user_id = "example_user"
    link = guard.send_recovery_email(user_id)
    print(f"Recovery link: {link}")
    # Simulate verifying the link
    success = guard.verify_link(link, user_id)
    guard.log_recovery_attempt(user_id, success)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
