"""Settings shared by every step. Change behaviour here, not deep inside the code."""

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%b %d %Y"]

OUTLET_MAP = {
    "bar": "Bar", "the bar": "Bar", "resto": "Restaurant", "restaurant": "Restaurant",
    "spa": "Spa", "shore excursions": "Excursions", "excursions": "Excursions",
    "cafe": "Cafe", "café": "Cafe", "boutique": "Boutique",
}

CLEAN_COLUMNS = ["charge_id", "guest_id", "outlet", "charge_date", "amount", "charge_type"]

REJECT_REASONS = ("invalid amount", "invalid date", "unknown guest_id")
