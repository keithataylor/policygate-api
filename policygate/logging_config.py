
from datetime import datetime
import logging


formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)
formatter.converter = datetime.time.gmtime

handler = logging.StreamHandler()
handler.setFormatter(formatter)

audit_logger = logging.getLogger("policygate.audit")
audit_logger.setLevel(logging.INFO)
audit_logger.propagate = False
if not audit_logger.handlers:
    audit_logger.addHandler(handler)

app_logger = logging.getLogger("policygate.app")
app_logger.setLevel(logging.INFO)
app_logger.propagate = False
if not app_logger.handlers:
    app_logger.addHandler(handler)