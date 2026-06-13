import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict

@dataclass
class Account:
    id: int
    lockout_status: bool
    failed_attempts: int
    last_attempt_time: datetime

class InstagramGuard:
    def __init__(self):
        self.accounts: Dict[int, Account] = {}

    def login_attempt(self, account_id: int) -> bool:
        if account_id not in self.accounts:
            self.accounts[account_id] = Account(id=account_id, lockout_status=False, failed_attempts=0, last_attempt_time=datetime.now())
        account = self.accounts[account_id]
        if account.lockout_status and (datetime.now() - account.last_attempt_time) < timedelta(minutes=30):
            return False
        account.failed_attempts += 1
        account.last_attempt_time = datetime.now()
        if account.failed_attempts >= 5 and (datetime.now() - account.last_attempt_time.replace(minute=account.last_attempt_time.minute - 10)) < timedelta(minutes=10):
            account.lockout_status = True
        return True

    def verify_account(self, account_id: int) -> bool:
        if account_id not in self.accounts:
            return False
        account = self.accounts[account_id]
        account.lockout_status = False
        return True

    def get_lockout_status(self, account_id: int) -> bool:
        if account_id not in self.accounts:
            return False
        return self.accounts[account_id].lockout_status
