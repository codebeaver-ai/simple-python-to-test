import pytest

from datetime import datetime
from investment_tracker import InvestmentTracker

# TODO: add more tests

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_calculate_overall_spending(self):
        tracker = InvestmentTracker()
        tracker.record_transaction(50.00, "food", "Dinner")
        tracker.record_transaction(30.00, "transport", "Bus ticket")
        tracker.record_transaction(100.00, "utilities", "Internet bill")

        total_spending = tracker.calculate_overall_spending()

        assert total_spending == 180.00, f"Expected total spending to be 180.00, but got {total_spending}"