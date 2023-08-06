from __future__ import annotations

import functools
import logging
import time
from typing import Any
from typing import Callable


logger = logging.getLogger(__name__)


def debug(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.debug(
            f"[start] - {func.__name__}(args={args}, kwargs={kwargs})",
        )
        s = time.perf_counter()
        res = func(*args, **kwargs)
        e = time.perf_counter()
        logger.debug(f"[end] - {func.__name__} in {e - s:.2f}")
        return res

    return wrapper
