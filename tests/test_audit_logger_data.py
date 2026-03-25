import policygate.audit as audit


def test_audit_logger_data():
  assert audit.audit_logger.name == "policygate.audit"
  assert audit.audit_logger.propagate is False
