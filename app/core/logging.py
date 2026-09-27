import logging
import sys
from app.core.config import settings

def setup_logging():
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Specific logger for audit trail
    audit_logger = logging.getLogger("audit")
    audit_logger.setLevel(logging.INFO)
    
    return logging.getLogger("app")

logger = setup_logging()
audit_logger = logging.getLogger("audit")
