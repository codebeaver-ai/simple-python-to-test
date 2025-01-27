from investment_tracker import InvestmentTracker


class TestInvestment:
    def test_record_transaction(self):
        """
        Test that the record_transaction method correctly records a valid transaction
        and returns True.
        """
        tracker = InvestmentTracker()
        result = tracker.record_transaction(50.00, "food", "Dinner")
        
        assert result == True
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0] == {
            "amount": 50.00,
            "category": "food",
            "description": "Dinner"
        }
