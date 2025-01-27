from investment_tracker import InvestmentTracker


class TestInvestment:
    def test_record_transaction(self):
        """
        Test the record_transaction method of InvestmentTracker.
        
        This test verifies that:
        1. A valid transaction is recorded successfully.
        2. The number of expenses increases after recording a transaction.
        3. The recorded transaction has the correct details.
        """
        tracker = InvestmentTracker()
        initial_expense_count = len(tracker.expenses)
        
        # Record a valid transaction
        result = tracker.record_transaction(50.0, "food", "Grocery shopping")
        
        assert result == True, "record_transaction should return True for a valid transaction"
        assert len(tracker.expenses) == initial_expense_count + 1, "Number of expenses should increase by 1"
        
        # Check if the recorded transaction has correct details
        latest_expense = tracker.expenses[-1]
        assert latest_expense["amount"] == 50.0
        assert latest_expense["category"] == "food"
        assert latest_expense["description"] == "Grocery shopping"
