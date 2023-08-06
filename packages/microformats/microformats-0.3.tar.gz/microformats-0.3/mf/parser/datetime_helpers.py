"""Helper functions to deal wit datetime strings"""

import re
from datetime import datetime

DATE_RE = r"(\d{4}-\d{2}-\d{2})|(\d{4}-\d{3})"
SEC_RE = r"(:(?P<second>\d{2})(\.\d+)?)"
RAWTIME_RE = rf"(?P<hour>\d{{1,2}})(:(?P<minute>\d{{2}}){SEC_RE}?)?"
AMPM_RE = r"am|pm|a\.m\.|p\.m\.|AM|PM|A\.M\.|P\.M\."
TIMEZONE_RE = r"Z|[+-]\d{1,2}:?\d{2}?"
TIME_RE = (
    rf"(?P<rawtime>{RAWTIME_RE})( ?(?P<ampm>{AMPM_RE}))?( ?(?P<tz>{TIMEZONE_RE}))?"
)
DATETIME_RE = rf"(?P<date>{DATE_RE})(?P<separator>[T ])(?P<time>{TIME_RE})"


def normalize_datetime(dtstr, match=None):
    """Try to normalize a datetime string.
    1. Convert 12-hour time to 24-hour time

    pass match in if we have already calculated it to avoid rework
    """
    match = match or (dtstr and re.match(DATETIME_RE + "$", dtstr))
    if match:
        datestr = match.group("date")
        hourstr = match.group("hour")
        minutestr = match.group("minute") or "00"
        secondstr = match.group("second")
        ampmstr = match.group("ampm")
        separator = match.group("separator")

        # convert ordinal date YYYY-DDD to YYYY-MM-DD
        try:
            datestr = datetime.strptime(datestr, "%Y-%j").strftime("%Y-%m-%d")
        except ValueError:
            # datestr was not in YYYY-DDD format
            pass

        # 12 to 24 time conversion
        if ampmstr:
            hourstr = match.group("hour")
            hourint = int(hourstr)

            if (ampmstr.startswith("a") or ampmstr.startswith("A")) and hourint == 12:
                hourstr = "00"

            if (ampmstr.startswith("p") or ampmstr.startswith("P")) and hourint < 12:
                hourstr = hourint + 12

        dtstr = f"{datestr}{separator}{hourstr}:{minutestr}"

        if secondstr:
            dtstr += ":" + secondstr

        tzstr = match.group("tz")
        if tzstr:
            dtstr += tzstr
    return dtstr
