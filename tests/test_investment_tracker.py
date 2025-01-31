from investment_tracker import InvestmentTracker


class TestInvestment:
    def test_record_transaction(self):
        """
        Test that the record_transaction method correctly adds a transaction
        and returns True for a valid input.
        """
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True
