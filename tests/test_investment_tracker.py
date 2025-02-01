from investment_tracker import InvestmentTracker

class TestInvestment:
    def test_record_transaction(self):
        """
        Test that the record_transaction method of InvestmentTracker
        correctly records a transaction and returns True.
        """
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_calculate_overall_spending(self):
        """
        Test that the calculate_overall_spending method correctly
        computes the sum of all recorded transactions.
        """
        tracker = InvestmentTracker()
        tracker.record_transaction(100, "food", "groceries")
        tracker.record_transaction(50, "transport", "gas")
        tracker.record_transaction(75.50, "entertainment", "movie tickets")

        total_spending = tracker.calculate_overall_spending()
        expected_total = 100 + 50 + 75.50

        assert total_spending == expected_total, f"Expected {expected_total}, but got {total_spending}"
