import pytest

from investment_tracker import InvestmentTracker

class TestInvestment:
    def test_record_transaction(self):
        """
        Test the record_transaction method of InvestmentTracker.

        This test checks:
        1. Valid transaction recording
        2. Expense list update
        3. Invalid amount handling
        4. Invalid category handling
        """
        tracker = InvestmentTracker()

        # Test valid transaction
        assert tracker.record_transaction(50.0, "food", "Grocery shopping") == True
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0] == {"amount": 50.0, "category": "food", "description": "Grocery shopping"}

        # Test invalid amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(-10, "food", "Invalid amount")

        # Test invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(30, "invalid_category", "Invalid category")
