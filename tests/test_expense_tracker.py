import pytest

from expense_tracker import ExpenseTracker

class TestExpenseTracker:
    """Tests for the ExpenseTracker class."""

    def test_add_existing_category(self):
        """
        Test that adding an existing category returns False and that adding a new category returns True.
        This helps increase our test coverage for the add_category method.
        """
        tracker = ExpenseTracker()
        # Attempt to add a category that already exists in default set ("food").
        result_existing = tracker.add_category("food")
        assert result_existing is False, "Expected adding an existing category to return False."

        # Add a new category which is not in the default set.
        result_new = tracker.add_category("health")
        assert result_new is True, "Expected adding a new category to return True."
        # Verify that the new category is now present in the tracker
        assert "health" in tracker.categories