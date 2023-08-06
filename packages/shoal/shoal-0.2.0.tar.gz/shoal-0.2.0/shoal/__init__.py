"""shoal."""

from warnings import filterwarnings

from beartype.roar import BeartypeDecorHintPep585DeprecationWarning
from loguru import logger

__version__ = '0.2.0'
__pkg_name__ = 'shoal'

logger.disable(__pkg_name__)

# ====== Above is the recommended code from calcipy_template and may be updated on new releases ======

# FYI: https://github.com/beartype/beartype#are-we-on-the-worst-timeline
filterwarnings('ignore', category=BeartypeDecorHintPep585DeprecationWarning)

from ._ling import shoalling  # noqa: E402,E408
from ._log import get_logger  # noqa: E402,E408
from ._shell import capture_shell, shell  # noqa: E402,E408
from ._tang import Tang  # noqa: E402,E408
from ._tangs import register, register_fun  # noqa: E402,E408
