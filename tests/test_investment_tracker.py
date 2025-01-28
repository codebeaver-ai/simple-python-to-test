from investment_tracker import InvestmentTracker


class TestInvestment:
    def test_record_transaction(self):
        """
        Test that a valid transaction is correctly recorded in the InvestmentTracker.
        """
        tracker = InvestmentTracker()
        result = tracker.record_transaction(50.0, "food", "Grocery shopping")
        
        assert result == True, "record_transaction should return True for a valid transaction"
        assert len(tracker.expenses) == 1, "One expense should be recorded"
        assert tracker.expenses[0] == {
            "amount": 50.0,
            "category": "food",
            "description": "Grocery shopping"
        }, "The recorded expense should match the input"
