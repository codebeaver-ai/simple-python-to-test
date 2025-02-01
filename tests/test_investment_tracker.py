from investment_tracker import InvestmentTracker


class TestInvestment:
    def test_record_transaction(self):
        """
        Test that the record_transaction method of InvestmentTracker
        correctly records a transaction and returns True.
        """
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True
