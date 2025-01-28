from investment_tracker import InvestmentTracker


class TestInvestment:
    def test_record_transaction(self):
        """
        Test that the record_transaction method correctly adds a new expense
        and returns True for a valid transaction.
        """
        tracker = InvestmentTracker()
        assert tracker.record_transaction(100, "food", "groceries") == True
