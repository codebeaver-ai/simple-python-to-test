import pytest
from investment_tracker import InvestmentTracker


class TestInvestmentTracker:
    """Test class for InvestmentTracker"""

    def test_record_transaction(self):
        """
        Test that a transaction can be recorded successfully.
        This test creates an InvestmentTracker instance and records a valid transaction.
        """
        tracker = InvestmentTracker()
        result = tracker.record_transaction(100, "food", "Grocery shopping")
        assert result == True
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0]["amount"] == 100
        assert tracker.expenses[0]["category"] == "food"
        assert tracker.expenses[0]["description"] == "Grocery shopping"
