from investment_tracker import InvestmentTracker

class TestInvestment:
    def test_record_transaction(self):
        """
        Test that recording a valid transaction returns True and doesn't raise any exceptions.
        """
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
        """
        Test that registering a new category works correctly and that
        attempting to register a duplicate category returns False.
        """
        tracker = InvestmentTracker()

        # Test registering a new category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test registering an existing category (should return False)
        assert tracker.register_new_category("food") == False

        # Test that the number of categories has increased by only one
        assert len(tracker.categories) == 6  # 5 default + 1 new