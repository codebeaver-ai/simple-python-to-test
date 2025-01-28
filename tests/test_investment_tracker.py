from investment_tracker import InvestmentTracker
import pytest


class TestInvestment:
    def test_record_transaction(self):
        """
        Test the record_transaction method of InvestmentTracker.
        
        This test checks:
        1. If a valid transaction is recorded successfully
        2. If an invalid amount raises a ValueError
        3. If an invalid category raises a ValueError
        """
        tracker = InvestmentTracker()
        
        # Test valid transaction
        assert tracker.record_transaction(50.0, "food", "Groceries") == True
        
        # Test invalid amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(-10, "food", "Invalid amount")
        
        # Test invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(30.0, "invalid_category", "Invalid category")
