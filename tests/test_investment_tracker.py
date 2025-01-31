from investment_tracker import InvestmentTracker

class TestInvestment:
    def test_record_transaction(self):
        """
        Test that the record_transaction method returns True when a valid transaction is recorded.
        """
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
        """
        Test that the register_new_category method successfully adds a new category
        and returns True, and returns False when trying to add an existing category.
        """
        tracker = InvestmentTracker()

        # Test adding a new category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test adding an existing category
        assert tracker.register_new_category("food") == False

        # Test adding a new category with uppercase letters
        assert tracker.register_new_category("INVESTMENTS") == True
        assert "investments" in tracker.categories