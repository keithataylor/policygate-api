"""
Logging configuration for the PolicyGate service.
"""

import time
import logging

# Separate loggers allow audit records and operational logs to be filtered independently.

formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)
formatter.converter = time.gmtime

handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Audit logger for structured audit events, which can be sent to a SIEM or 
# log management system for security monitoring and compliance.
audit_logger = logging.getLogger("policygate.audit")
audit_logger.setLevel(logging.INFO)
audit_logger.propagate = False
if not audit_logger.handlers:
    audit_logger.addHandler(handler)

# Application logger for general operational logs, which can be used for debugging, 
# performance monitoring, and general observability of the service.
app_logger = logging.getLogger("policygate.app")
app_logger.setLevel(logging.INFO)
app_logger.propagate = False
if not app_logger.handlers:
    app_logger.addHandler(handler)