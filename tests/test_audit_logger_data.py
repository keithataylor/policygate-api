import policygate.audit as audit


def test_audit_logger_data():
  assert audit.logger.name == "policygate.audit"
  assert audit.logger.propagate is False