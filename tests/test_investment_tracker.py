from investment_tracker import InvestmentTracker


class TestInvestment:
    def test_record_transaction(self):
        """
        Test that a transaction is correctly recorded in the InvestmentTracker.
        
        This test checks if:
        1. A valid transaction is successfully added.
        2. The expense list is updated correctly.
        3. The method returns True for a successful addition.
        """
        tracker = InvestmentTracker()
        result = tracker.record_transaction(100.00, "food", "Grocery shopping")
        
        assert result == True
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0] == {
            "amount": 100.00,
            "category": "food",
            "description": "Grocery shopping"
        }
