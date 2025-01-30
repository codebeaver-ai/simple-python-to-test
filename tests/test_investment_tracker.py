import pytest
from investment_tracker import InvestmentTracker


class TestInvestmentTracker:
    def test_register_new_category(self):
        """
        Test the register_new_category method of InvestmentTracker.
        
        This test checks if:
        1. A new category can be successfully added.
        2. Attempting to add an existing category returns False.
        """
        tracker = InvestmentTracker()
        
        # Test adding a new category
        result = tracker.register_new_category("investments")
        assert result == True
        assert "investments" in tracker.categories
        
        # Test adding an existing category
        result = tracker.register_new_category("investments")
        assert result == False
