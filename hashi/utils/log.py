import logging
import sys

TRACE_LEVEL = 5

logger = logging.getLogger("hashi")
logger.setLevel(logging.INFO)
default_handler = logging.StreamHandler(sys.stdout)
default_handler.setFormatter(
    logging.Formatter("[%(asctime)s %(name)s] %(levelname)s: %(message)s")
)
logger.addHandler(default_handler)


def trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LEVEL):
        self._log(TRACE_LEVEL, message, args, **kws)


logging.addLevelName(TRACE_LEVEL, "TRACE")
logging.Logger.trace = trace  # type:ignore
