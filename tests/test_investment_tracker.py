import pytest

from datetime import datetime
from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
        """
        Test the register_new_category method:
        - Registering a new category should succeed
        - The new category should be in the categories set
        - Registering the same category again should fail
        """
        tracker = InvestmentTracker()

        # Register a new category
        result = tracker.register_new_category("savings")
        assert result == True
        assert "savings" in tracker.categories

        # Try to register the same category again
        result = tracker.register_new_category("savings")
        assert result == False