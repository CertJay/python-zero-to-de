"""Unit tests for transform.py. One example; write at least 10 tests across tests/."""
import pandas as pd

from onboard_pipeline.transform import standardize_outlet


def test_standardize_outlet_maps_known_variants():
    s = pd.Series([" the BAR ", "Resto", "pool deck"])
    assert standardize_outlet(s).tolist() == ["Bar", "Restaurant", "Pool Deck"]
