from investment_tracker import InvestmentTracker
import pytest


class TestInvestment:
    def test_record_transaction(self):
        """
        Test the record_transaction method of InvestmentTracker.
        
        This test checks:
        1. Valid transaction recording
        2. Invalid amount (negative number)
        3. Invalid category
        """
        tracker = InvestmentTracker()
        
        # Test valid transaction
        assert tracker.record_transaction(50.0, "food", "Grocery shopping") == True
        
        # Test invalid amount (negative number)
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(-10, "food", "Invalid amount")
        
        # Test invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(30, "invalid_category", "Invalid category")
