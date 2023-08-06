import datetime
import functools

from frozenlist2 import frozenlist
from frozendict.core import frozendict  # pylint: disable=no-name-in-module

from .attr import PULP2_PY_CONVERTER


def get_converter(field, value):
    """Given an attrs target field and an input value from Pulp,
    return a converter function which should be used to convert the Pulp value
    into a Python representation."""

    metadata_converter = field.metadata.get(PULP2_PY_CONVERTER)
    if metadata_converter:
        # explicitly defined for this field, just return it
        return metadata_converter

    # Nothing explicitly defined, but check the types, there may still be
    # some applicable default
    if field.type is datetime.datetime and isinstance(value, str):
        return read_timestamp

    return null_convert


def null_convert(value):
    return value


def read_timestamp(value):
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        # irritatingly (probably a bug), some values were missing the "Z"
        # technically meaning we don't know the timezone.
        # So we try parsing again without it and we just assume it's UTC.
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")


def tolerant_timestamp(value):
    # Converter for fields which can accept a timestamp string, but which
    # falls back to returning the input verbatim if conversion fails.
    #
    # Since it tolerates failed conversions, this is intended to be combined
    # with a validator.
    if isinstance(value, str):
        try:
            return read_timestamp(value)
        except ValueError:
            # Not a timestamp, conversion doesn't happen
            pass

    return value


def timestamp_converter(value):
    # Converter for fields which are stored as strings,
    # but which model is expecting datetime
    # falls back to returning the input verbatim if not a datetime.
    #
    if isinstance(value, datetime.datetime):
        return value.strftime("%Y-%m-%dT%H:%M:%SZ")

    return value


def write_timestamp(value):
    # defaults to current time if value is None
    if value is None:
        value = datetime.datetime.utcnow()
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def frozenlist_or_none_converter(obj, map_fn=(lambda x: x)):
    if obj is not None:
        return frozenlist(map_fn(obj))
    return None


frozenlist_or_none_sorted_converter = functools.partial(
    frozenlist_or_none_converter, map_fn=lambda x: sorted(set(x))
)


def frozendict_or_none_converter(obj):
    # Convert object and values to immutable structures.
    # Skip convert if the obj is already frozendict.
    # This happens when the class containing the value is copied (e.g: with attr.evolve).
    if obj is not None and not isinstance(obj, frozendict):
        for (key, value) in obj.items():
            if isinstance(value, list):
                obj[key] = frozenlist_or_none_converter(value)
            if isinstance(value, dict):
                obj[key] = frozendict_or_none_converter(value)
        return frozendict(obj)
    return obj
