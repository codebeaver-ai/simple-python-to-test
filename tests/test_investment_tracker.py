from investment_tracker import InvestmentTracker
import pytest


class TestInvestment:
    def test_record_transaction(self):
        """
        Test that the record_transaction method correctly adds a new expense to the tracker.
        It should return True for a valid transaction and raise ValueError for invalid inputs.
        """
        tracker = InvestmentTracker()
        
        # Test valid transaction
        assert tracker.record_transaction(25.50, "food", "Lunch at cafe") == True
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0] == {"amount": 25.50, "category": "food", "description": "Lunch at cafe"}
        
        # Test invalid amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(-10, "food", "Invalid amount")
        
        # Test invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(30, "invalid_category", "Invalid category")
