import pytest
from datetime import datetime
from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_calculate_overall_spending(self):
        tracker = InvestmentTracker()

        # Add some sample transactions
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Gas")
        tracker.record_transaction(200, "utilities", "Electricity bill")

        # Calculate and assert the total spending
        total_spending = tracker.calculate_overall_spending()
        assert total_spending == 350, f"Expected total spending to be 350, but got {total_spending}"