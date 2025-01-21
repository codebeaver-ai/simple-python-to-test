import pytest

from datetime import datetime
from investment_tracker import InvestmentTracker

# TODO: add more tests

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
        """
        Test the register_new_category method of InvestmentTracker.

        This test verifies that:
        1. A new category can be successfully added.
        2. Adding an existing category returns False.
        3. The new category is actually added to the categories set.
        """
        tracker = InvestmentTracker()

        # Test adding a new category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test adding an existing category
        assert tracker.register_new_category("food") == False

        # Test adding a new category with mixed case
        assert tracker.register_new_category("Investments") == True
        assert "investments" in tracker.categories