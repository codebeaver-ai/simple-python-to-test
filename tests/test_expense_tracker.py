import pytest
from expense_tracker import ExpenseTracker

class TestExpenseTracker:
    def test_add_category(self):
        # Create an instance of ExpenseTracker
        tracker = ExpenseTracker()

        # Test adding a new category
        assert tracker.add_category("groceries") == True
        assert "groceries" in tracker.categories

        # Test adding an existing category (should return False)
        assert tracker.add_category("groceries") == False

        # Test adding an invalid category (empty string)
        with pytest.raises(ValueError):
            tracker.add_category("")

        # Test adding an invalid category (non-string)
        with pytest.raises(ValueError):
            tracker.add_category(123)