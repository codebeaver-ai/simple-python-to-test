import pytest

from datetime import datetime
from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_and_use_new_category(self):
        """
        Test registering a new category ('health'), ensuring that a duplicate registration fails,
        and verifying that transactions in the new category are correctly recorded and computed.
        """
        tracker = InvestmentTracker()

        # Register a new category not in the default set.
        result_new = tracker.register_new_category("health")
        assert result_new is True, "Expected registering a new category to return True"

        # Attempting to register the same category again should return False.
        result_duplicate = tracker.register_new_category("health")
        assert result_duplicate is False, "Expected duplicate registration to return False"

        # Record a transaction using the new 'health' category.
        tracker.record_transaction(200, "health", "Gym membership")

        # Verify that compute_category_sum correctly sums the transaction.
        category_sum = tracker.compute_category_sum("health")
        assert category_sum == 200, "Expected the sum for category 'health' to equal 200"