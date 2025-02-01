import pytest
from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    def test_record_transaction(self):
        """
        Test that a transaction can be recorded successfully.
        """
        tracker = InvestmentTracker()
        result = tracker.record_transaction(100, "food", "Grocery shopping")
        assert result == True
