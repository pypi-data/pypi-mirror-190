import logging

import dcclog
from dcclog.cipher.rsa import RSAEncryption

dcclog.default_config(
    level=dcclog.DEBUG,
    filename=".logs/app.log",
    # cipher=RSAEncryption("pubkey.pem"),
)
logger = dcclog.getLogger(__name__)
logging.basicConfig()

logger.error("error message.")
logger.warning("warning message.")
logger.info("info \nmessage.")
logger.debug("debug message.")


class A:
    @dcclog.log(skip_args=True)
    def aaa(self, x: str) -> None:
        pass


a = A()
a.aaa("22")


@dcclog.log(level=dcclog.ERROR)
def bbbb(y: int) -> None:
    print(f"{y=}")
    1 / 0


bbbb(6)
