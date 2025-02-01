from investment_tracker import InvestmentTracker

class TestInvestment:
    def test_record_transaction(self):
        """
        Test that the record_transaction method returns True when given valid inputs.
        This test checks if a transaction with amount 100, category 'food', and description 'groceries'
        is successfully recorded.
        """
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
        """
        Test that the register_new_category method successfully adds a new category
        and returns True when given a valid category name that doesn't already exist.
        Also verify that trying to add the same category again returns False.
        """
        tracker = InvestmentTracker()

        # Test adding a new category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test adding the same category again
        assert tracker.register_new_category("savings") == False

        # Verify the total number of categories
        assert len(tracker.categories) == 6  # 5 default categories + 1 new