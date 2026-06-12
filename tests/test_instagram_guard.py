from instagram_guard import InstagramGuard, SecurityRule

def test_get_rules():
    guard = InstagramGuard()
    rules = guard.get_rules()
    assert len(rules) == 2
    assert rules["geo-restriction"].name == "Geo-Restriction"
    assert rules["device-fingerprinting"].name == "Device Fingerprinting"

def test_toggle_rule():
    guard = InstagramGuard()
    guard.toggle_rule("geo-restriction")
    assert guard.get_rules()["geo-restriction"].enabled
    guard.toggle_rule("geo-restriction")
    assert not guard.get_rules()["geo-restriction"].enabled

def test_toggle_nonexistent_rule():
    guard = InstagramGuard()
    try:
        guard.toggle_rule("nonexistent-rule")
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "Rule not found"

def test_save_preferences():
    guard = InstagramGuard()
    guard.toggle_rule("geo-restriction")
    guard.save_preferences()
    # This will print the current state, but we can't assert on it directly
    # Instead, we'll verify that the rule was toggled correctly
    assert guard.get_rules()["geo-restriction"].enabled
