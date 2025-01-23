import pytest

from datetime import datetime
from investment_tracker import InvestmentTracker

# TODO: add more tests

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_calculate_overall_spending(self):
        """
        Test that calculate_overall_spending correctly sums up all expenses.
        """
        tracker = InvestmentTracker()
        tracker.record_transaction(100, "food", "groceries")
        tracker.record_transaction(50, "transport", "gas")
        tracker.record_transaction(200, "utilities", "electricity")

        total_spending = tracker.calculate_overall_spending()
        assert total_spending == 350, f"Expected total spending to be 350, but got {total_spending}"