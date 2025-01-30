import pytest

from investment_tracker import InvestmentTracker

def test_register_new_category():
    """
    Test the register_new_category method of InvestmentTracker.

    This test checks if:
    1. A new category can be successfully added.
    2. Adding an existing category returns False.
    3. Adding an empty string raises a ValueError.
    """
    tracker = InvestmentTracker()

    # Test adding a new category
    assert tracker.register_new_category("savings") == True
    assert "savings" in tracker.categories

    # Test adding an existing category
    assert tracker.register_new_category("food") == False

    # Test adding an empty string
    with pytest.raises(ValueError):
        tracker.register_new_category("")