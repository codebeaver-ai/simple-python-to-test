from investment_tracker import InvestmentTracker

class TestInvestment:
    def test_record_transaction(self):
        """
        Test that the record_transaction method correctly adds a transaction
        and returns True for a valid input.
        """
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
        """
        Test that the register_new_category method correctly adds a new category
        and returns True for a valid input, and False for an existing category.
        """
        tracker = InvestmentTracker()

        # Test adding a new category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test adding an existing category
        assert tracker.register_new_category("food") == False

        # Test adding a category with different case
        assert tracker.register_new_category("INVESTMENTS") == True
        assert "investments" in tracker.categories