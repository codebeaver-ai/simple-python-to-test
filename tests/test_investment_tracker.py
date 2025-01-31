from investment_tracker import InvestmentTracker

class TestInvestment:
    def test_record_transaction(self):
        """
        Test that the record_transaction method successfully records a transaction
        and returns True when given valid input.
        """
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
        """
        Test that the register_new_category method successfully adds a new category
        and returns True when given a valid category name.
        """
        tracker = InvestmentTracker()
        initial_category_count = len(tracker.categories)
        result = tracker.register_new_category("savings")

        assert result == True
        assert len(tracker.categories) == initial_category_count + 1
        assert "savings" in tracker.categories
