from investment_tracker import InvestmentTracker


class TestInvestment:
    def test_record_transaction(self):
        """
        Test that recording a valid transaction returns True.
        This test ensures that the record_transaction method of InvestmentTracker
        correctly handles a valid transaction and returns True.
        """
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True
