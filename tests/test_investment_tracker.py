from investment_tracker import InvestmentTracker


class TestInvestment:
    def test_record_transaction(self):
        """
        Test that a transaction can be recorded successfully and that it raises
        appropriate exceptions for invalid inputs.
        """
        tracker = InvestmentTracker()
        
        # Test successful transaction
        assert tracker.record_transaction(50.0, "food", "Groceries") == True
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0] == {"amount": 50.0, "category": "food", "description": "Groceries"}
        
        # Test invalid amount
        try:
            tracker.record_transaction(-10, "food", "Invalid")
            assert False, "Should raise ValueError for negative amount"
        except ValueError:
            pass
        
        # Test invalid category
        try:
            tracker.record_transaction(30, "invalid_category", "Invalid")
            assert False, "Should raise ValueError for invalid category"
        except ValueError:
            pass
