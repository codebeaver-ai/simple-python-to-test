import pytest
import unittest

from datetime import datetime
from investment_tracker import InvestmentTracker

class TestInvestmentTracker(unittest.TestCase):
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

def test_register_and_transaction_with_new_category():
    """
    Test that registering a new expense category works correctly,
    that duplicate registrations return False,
    and that a transaction using the new category is recorded and summed accurately.
    """
    tracker = InvestmentTracker()

    # Register a new unique category 'travel'
    assert tracker.register_new_category("travel") is True, (
        "Registering a unique category should return True."
    )

    # Attempt to register the same 'travel' category again should return False.
    assert tracker.register_new_category("travel") is False, (
        "Registering a duplicate category should return False."
    )

    # Record a transaction using the newly registered 'travel' category.
    assert tracker.record_transaction(200.0, "travel", "Flight ticket") is True, (
        "Recording a transaction with a newly registered category should succeed."
    )

    # Verify that compute_category_sum returns the correct sum for the 'travel' category.
    travel_total = tracker.compute_category_sum("travel")
    assert travel_total == 200.0, "The computed sum for 'travel' should equal the recorded transaction amount."