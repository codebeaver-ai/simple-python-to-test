import pytest
from investment_tracker import InvestmentTracker


class TestInvestmentTracker:
    """Test class for InvestmentTracker"""

    def test_record_transaction(self):
        """
        Test the record_transaction method of InvestmentTracker.
        Verifies that a transaction can be recorded successfully.
        """
        tracker = InvestmentTracker()
        assert tracker.record_transaction(100, "food", "Grocery shopping")
