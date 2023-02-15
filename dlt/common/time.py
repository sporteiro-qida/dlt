import contextlib
from typing import Any, Optional  # noqa
import datetime

from dlt.common.pendulum import pendulum
from pendulum.parsing import parse_iso8601, _parse_common as parse_datetime_common
from pendulum.tz import UTC

PAST_TIMESTAMP: float = 0.0
FUTURE_TIMESTAMP: float = 9999999999.0
DAY_DURATION_SEC: float = 24 * 60 * 60.0


def timestamp_within(timestamp: float, min_exclusive: Optional[float], max_inclusive: Optional[float]) -> bool:
    """
    check if timestamp within range uniformly treating none and range inclusiveness
    """
    return timestamp > (min_exclusive or PAST_TIMESTAMP) and timestamp <= (max_inclusive or FUTURE_TIMESTAMP)


def timestamp_before(timestamp: float, max_inclusive: Optional[float]) -> bool:
    """
    check if timestamp is before max timestamp, inclusive
    """
    return timestamp <= (max_inclusive or FUTURE_TIMESTAMP)


def parse_iso_like_datetime(value: Any) -> datetime.datetime:
    # we use internal pendulum parse function. the generic function for example parses string "now" as now()
    # it also tries to parse ISO intervals but the code is very low quality
    # so it does not seem to be under control

    # only iso dates are allowed
    dtv = None
    with contextlib.suppress(ValueError):
        dtv = parse_iso8601(value)
    # now try to parse a set of ISO like dates
    if not dtv:
        dtv = parse_datetime_common(value)
    if isinstance(dtv, datetime.time):
        raise ValueError(value)
    if isinstance(dtv, datetime.datetime):
        return pendulum.datetime(
            dtv.year,
            dtv.month,
            dtv.day,
            dtv.hour,
            dtv.minute,
            dtv.second,
            dtv.microsecond,
            tz=dtv.tzinfo or UTC  # type: ignore
        )
    return dtv