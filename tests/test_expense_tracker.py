import pytest

from expense_tracker import ExpenseTracker

class TestExpenseTracker:
    def test_add_category(self):
        """
        Test the add_category method of ExpenseTracker.

        This test checks:
        1. Adding a new valid category returns True
        2. Adding an existing category returns False
        3. Adding an invalid category (empty string) raises a ValueError
        """
        tracker = ExpenseTracker()

        # Test adding a new valid category
        assert tracker.add_category("groceries") == True
        assert "groceries" in tracker.categories

        # Test adding an existing category
        assert tracker.add_category("groceries") == False

        # Test adding an invalid category (empty string)
        with pytest.raises(ValueError):
            tracker.add_category("")