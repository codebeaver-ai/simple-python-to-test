import pytest
from datetime import datetime
from investment_tracker import InvestmentTracker


class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
        tracker = InvestmentTracker()

        # Test adding a new category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test adding an existing category (should return False)
        assert tracker.register_new_category("savings") == False

        # Test adding a category with spaces and uppercase (should be normalized)
        assert tracker.register_new_category("  New Category  ") == True
        assert "new category" in tracker.categories
