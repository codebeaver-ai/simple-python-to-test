from investment_tracker import InvestmentTracker


class TestInvestment:
    def test_record_transaction(self):
        """
        Test that recording a valid transaction returns True and doesn't raise any exceptions.
        """
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True
