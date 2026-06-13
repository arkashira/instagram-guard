from instagram_guard import InstagramGuard, User

def test_lock_account():
    guard = InstagramGuard()
    guard.add_user(1, "test@example.com")
    assert guard.lock_account(1)
    assert guard.users[1].locked

def test_generate_recovery_link():
    guard = InstagramGuard()
    guard.add_user(1, "test@example.com")
    link = guard.generate_recovery_link(1)
    assert link
    assert link in guard.recovery_links

def test_verify_recovery_link():
    guard = InstagramGuard()
    guard.add_user(1, "test@example.com")
    link = guard.generate_recovery_link(1)
    assert guard.verify_recovery_link(link)
    assert not guard.users[1].locked

def test_verify_recovery_link_expired():
    guard = InstagramGuard()
    guard.add_user(1, "test@example.com")
    link = guard.generate_recovery_link(1)
    guard.recovery_links[link].locked = True
    guard.recovery_links[link] = User(1, "test@example.com")
    guard.recovery_links[f"1-19700101000000"] = guard.recovery_links[link]
    del guard.recovery_links[link]
    assert not guard.verify_recovery_link(f"1-19700101000000")

def test_log_recovery_attempt():
    guard = InstagramGuard()
    guard.log_recovery_attempt("test_link")
    assert guard.recovery_attempts["test_link"] == 1
    guard.log_recovery_attempt("test_link")
    assert guard.recovery_attempts["test_link"] == 2

def test_send_recovery_email():
    guard = InstagramGuard()
    guard.add_user(1, "test@example.com")
    email = guard.send_recovery_email(1)
    assert email.startswith("Recovery link: ")

def test_add_user():
    guard = InstagramGuard()
    guard.add_user(1, "test@example.com")
    assert 1 in guard.users
    assert guard.users[1].email == "test@example.com"
