from investment_tracker import InvestmentTracker


class TestInvestment:
    def test_record_transaction(self):
        """
        Test that the record_transaction method returns True when given valid inputs.
        This test checks if a transaction with amount 100, category 'food', and description 'groceries'
        is successfully recorded.
        """
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True
