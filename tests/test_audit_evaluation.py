
# event contents are correct
# sensitive/raw payload is excluded


def test_audit_event_contents():
    # This test would involve triggering a policy evaluation and then checking the emitted audit event
    # For example, we could mock the policy evaluation to return a specific decision and then verify that the audit event contains the expected data
    pass

def test_audit_event_excludes_sensitive_data():
    # This test would involve ensuring that any sensitive or raw payload data is not included in the audit event
    # We could simulate a request with sensitive data and then check the emitted audit event to confirm that this data is not present
    pass