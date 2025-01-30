from investment_tracker import InvestmentTracker


class TestInvestment:
    def test_record_transaction(self):
        """
        Test the record_transaction method of InvestmentTracker.
        This test checks both valid and invalid inputs.
        """
        tracker = InvestmentTracker()

        # Test valid transaction
        assert tracker.record_transaction(25.50, "food", "Lunch at cafe") == True
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0] == {"amount": 25.50, "category": "food", "description": "Lunch at cafe"}

        # Test invalid amount
        try:
            tracker.record_transaction(-10, "food", "Invalid amount")
            assert False, "Should raise ValueError for negative amount"
        except ValueError:
            pass

        # Test invalid category
        try:
            tracker.record_transaction(30, "invalid_category", "Invalid category")
            assert False, "Should raise ValueError for invalid category"
        except ValueError:
            pass

        # Ensure the invalid transactions were not added
        assert len(tracker.expenses) == 1
