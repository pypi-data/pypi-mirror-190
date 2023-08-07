A few conveniences to do with dates and times.

*Latest release 20230210*:
* Drop Python 2 support.
* Make timezones mandatory where previously they were assumed.

There are some other PyPI modules providing richer date handling
than the stdlib `datetime` module.
This module mostly contains conveniences used in my other code;
you're welcome to it, but it does not pretend to be large or complete.

## Function `datetime2unixtime(dt)`

Convert a timezone aware `datetime` to a UNIX timestamp.

## Function `isodate(when=None, dashed=True)`

Return a date in ISO8601 YYYY-MM-DD format, or YYYYMMDD if not `dashed`.

Modern Pythons have a `datetime.isoformat` method, you use that.

## Function `localdate2unixtime(d)`

Convert a localtime `date` into a UNIX timestamp.

## Class `tzinfoHHMM(datetime.tzinfo)`

tzinfo class based on +HHMM / -HHMM strings.

## Function `unixtime2datetime(unixtime, *, tz: datetime.tzinfo)`

Convert a a UNIX timestamp to a `datetime` in the timezone `tz`.

## Class `UNIXTimeMixin`

A mixin for classes with a `.unixtime` attribute,
a `float` storing a UNIX timestamp.

*Method `UNIXTimeMixin.as_datetime(self, tz: datetime.tzinfo = datetime.timezone.utc)`*:
Return `self.unixtime` as a `datetime`
with the timezone `tz` (default `UTC`).

*Property `UNIXTimeMixin.datetime`*:
The `unixtime` as a UTC `datetime`.

# Release Log



*Release 20230210*:
* Drop Python 2 support.
* Make timezones mandatory where previously they were assumed.

*Release 20210306*:
Initial release, used by cs.sqltags.
