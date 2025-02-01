import pytest
from investment_tracker import InvestmentTracker


class TestInvestmentTracker:
    """Test suite for the InvestmentTracker class.

    This test ensures that a transaction is correctly recorded after registering
    a new category.
    """

    def test_record_transaction(self):
        tracker = InvestmentTracker()
        # First register the new category "buy" which is not among the default ones.
        registered = tracker.register_new_category("buy")
        assert registered is True

        # Record a transaction using the newly registered category.
        result = tracker.record_transaction(100, "buy", "stock")
        assert result is True

        # Verify that the expense list now contains one transaction.
        assert len(tracker.expenses) == 1
