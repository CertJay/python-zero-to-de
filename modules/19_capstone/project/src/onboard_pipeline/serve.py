"""Serve layer: reporting tables rebuilt from the charges table on every run."""


def build_daily_outlet_revenue(conn):
    """TODO: charge_date, outlet, total (rounded 2), charges -> table daily_outlet_revenue."""
    raise NotImplementedError


def build_guest_spend(conn):
    """TODO: guest_id, loyalty_tier, total_spend, n_charges, rank (dense, 1 = highest) -> table guest_spend."""
    raise NotImplementedError
