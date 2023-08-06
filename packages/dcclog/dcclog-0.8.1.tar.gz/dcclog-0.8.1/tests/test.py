import logging

import dcclog
from dcclog.cipher.rsa import RSAEncryption

dcclog.default_config(
    level=dcclog.INFO,
    filename=".logs/app.log",
    cipher=RSAEncryption("pubkey.pem"),
)
logger = dcclog.getLogger(name=__name__)
logging.basicConfig()

logger.error("error message.")
logger.warning("warning message.")
logger.info("info message.")
logger.debug("debug message.")


@dcclog.log
def logged_function(x: int, y: int) -> int:
    return x + y


logged_function(4, 6)
