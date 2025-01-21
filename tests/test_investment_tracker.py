import pytest

from investment_tracker import InvestmentTracker

class TestInvestment:
    def test_record_transaction(self):
        raise Exception("Not implemented")

    def test_record_transaction(self):
        """
        Test the record_transaction method of InvestmentTracker.

        This test covers:
        1. Successfully recording a valid transaction
        2. Attempting to record a transaction with an invalid amount (should raise ValueError)
        3. Attempting to record a transaction with an invalid category (should raise ValueError)
        """
        tracker = InvestmentTracker()

        # Test valid transaction
        assert tracker.record_transaction(50.0, "food", "Groceries") == True
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0] == {"amount": 50.0, "category": "food", "description": "Groceries"}

        # Test invalid amount
        with pytest.raises(ValueError):
            tracker.record_transaction(-10, "food", "Invalid amount")

        # Test invalid category
        with pytest.raises(ValueError):
            tracker.record_transaction(30.0, "invalid_category", "Invalid category")

    def test_register_new_category(self):
        """
        Test the register_new_category method of InvestmentTracker.

        This test covers:
        1. Successfully adding a new category
        2. Attempting to add an existing category (should return False)
        3. Attempting to add an invalid category (should raise ValueError)
        """
        tracker = InvestmentTracker()

        # Test adding a new category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test adding an existing category
        assert tracker.register_new_category("food") == False

        # Test adding an invalid category
        with pytest.raises(ValueError):
            tracker.register_new_category("")

        with pytest.raises(ValueError):
            tracker.register_new_category(123)