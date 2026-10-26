"""Reference solutions for Module 07."""
import json
import logging

REQUIRED_FIELDS = ("charge_id", "guest_id", "amount", "charge_type")


def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


def parse_int(text, default=None):
    try:
        return int(text.strip())
    except (ValueError, AttributeError):
        return default


def validate_charge(charge):
    for field in REQUIRED_FIELDS:
        if charge.get(field) is None:
            raise ValueError(f"missing field: {field}")
    amount = charge["amount"]
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise ValueError("amount is not a number")
    kind = charge["charge_type"]
    if kind not in ("sale", "refund"):
        raise ValueError(f"invalid charge_type: {kind}")
    if kind == "sale" and amount <= 0:
        raise ValueError("sale must be positive")
    if kind == "refund" and amount >= 0:
        raise ValueError("refund must be negative")
    return True


class DataQualityError(Exception):
    """Raised when a dataset fails a quality check."""


def require_rows(rows, source="source"):
    if not rows:
        raise DataQualityError(f"no rows received from {source}")
    return len(rows)


def split_valid_invalid(charges):
    valid, rejected = [], []
    for row_number, charge in enumerate(charges, start=1):
        try:
            validate_charge(charge)
        except ValueError as e:
            rejected.append({"row": row_number, "error": str(e)})
        else:
            valid.append(charge)
    return valid, rejected


def retry(func, attempts=3, exceptions=(ConnectionError, TimeoutError)):
    for attempt in range(1, attempts + 1):
        try:
            return func()
        except exceptions:
            if attempt == attempts:
                raise


def read_config(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        raise ValueError(f"invalid config: {path}")


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s"))
        logger.addHandler(handler)
    return logger


def process_all(items, func):
    processed = failed = 0
    for item in items:
        try:
            func(item)
        except Exception:
            failed += 1
        else:
            processed += 1
    return {"processed": processed, "failed": failed, "status": "success" if failed == 0 else "partial"}
