import pytest

from investment_tracker import InvestmentTracker

class TestInvestment:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_calculate_overall_spending(self):
        """
        Test that the calculate_overall_spending method correctly sums up all expenses.
        """
        tracker = InvestmentTracker()
        tracker.record_transaction(50, "food", "dinner")
        tracker.record_transaction(30, "transport", "bus ticket")
        tracker.record_transaction(100, "utilities", "electricity bill")

        assert tracker.calculate_overall_spending() == 180