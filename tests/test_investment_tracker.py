from investment_tracker import InvestmentTracker


class TestInvestment:
    def test_record_transaction(self):
        """
        Test that the record_transaction method returns True when a valid transaction is recorded.
        This test verifies that the method correctly handles a valid input and returns the expected result.
        """
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True
