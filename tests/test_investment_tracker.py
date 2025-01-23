from investment_tracker import InvestmentTracker


class TestInvestment:
    def test_record_transaction(self):
        """
        Test the record_transaction method of InvestmentTracker.
        
        This test checks:
        1. Successful recording of a valid transaction
        2. Raising ValueError for invalid amount
        3. Raising ValueError for invalid category
        """
        tracker = InvestmentTracker()

        # Test successful transaction
        assert tracker.record_transaction(50.0, "food", "Groceries") == True

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
