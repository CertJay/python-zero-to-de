"""T: dedupe, standardize, parse, and split into clean + rejected rows."""
from onboard_pipeline.config import CLEAN_COLUMNS, DATE_FORMATS, OUTLET_MAP  # noqa: F401


def remove_exact_duplicates(raw):
    """TODO: return (deduplicated DataFrame, number removed)."""
    raise NotImplementedError


def standardize_outlet(series):
    """TODO: collapse spaces + lowercase, map with OUTLET_MAP, unknown -> title case."""
    raise NotImplementedError


def parse_dates(series):
    """TODO: parse each of DATE_FORMATS explicitly (errors="coerce") and combine."""
    raise NotImplementedError


def split_clean_rejected(raw, valid_guest_ids):
    """TODO: return (clean, rejected). See FR-4 and FR-5 in lesson.md and Module 17."""
    raise NotImplementedError
