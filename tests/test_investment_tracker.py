from investment_tracker import InvestmentTracker
import pytest


class TestInvestment:
    def test_record_transaction(self):
        """
        Test the record_transaction method of InvestmentTracker.
        
        This test checks:
        1. Successful transaction recording
        2. Handling of invalid amount
        3. Handling of invalid category
        """
        tracker = InvestmentTracker()
        
        # Test successful transaction
        assert tracker.record_transaction(50.0, "food", "Groceries") == True
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0] == {"amount": 50.0, "category": "food", "description": "Groceries"}
        
        # Test invalid amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(-10, "food", "Invalid amount")
        
        # Test invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(30.0, "invalid_category", "Invalid category")
