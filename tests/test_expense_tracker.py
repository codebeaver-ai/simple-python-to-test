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

    def test_get_total_expenses(self):
        # Create an instance of ExpenseTracker
        tracker = ExpenseTracker()

        # Test when no expenses have been added
        assert tracker.get_total_expenses() == 0

        # Add some expenses
        tracker.add_expense(50.00, "food", "Groceries")
        tracker.add_expense(30.00, "transport", "Bus fare")
        tracker.add_expense(100.00, "utilities", "Electricity bill")

        # Test the total expenses
        assert tracker.get_total_expenses() == 180.00

        # Add another expense and test again
        tracker.add_expense(20.50, "entertainment", "Movie ticket")
        assert tracker.get_total_expenses() == 200.50

    # ... (existing test methods)

    def test_get_category_total(self):
        # Create an instance of ExpenseTracker
        tracker = ExpenseTracker()

        # Add expenses to different categories
        tracker.add_expense(50.00, "food", "Groceries")
        tracker.add_expense(30.00, "food", "Restaurant")
        tracker.add_expense(100.00, "utilities", "Electricity bill")
        tracker.add_expense(20.00, "food", "Snacks")

        # Test the total for the "food" category
        assert tracker.get_category_total("food") == 100.00

        # Test the total for the "utilities" category
        assert tracker.get_category_total("utilities") == 100.00

        # Test the total for a category with no expenses
        assert tracker.get_category_total("transport") == 0.00

        # Test error handling for an invalid category
        with pytest.raises(ValueError):
            tracker.get_category_total("invalid_category")

    def test_add_expense_invalid_inputs(self):
        tracker = ExpenseTracker()

        # Test with negative amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.add_expense(-50.00, "food", "Negative expense")

        # Test with zero amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.add_expense(0, "food", "Zero expense")

        # Test with invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.add_expense(50.00, "invalid_category", "Invalid category expense")

        # Verify that no expenses were added
        assert tracker.get_total_expenses() == 0

    def test_get_expenses_by_category(self):
        # Create an instance of ExpenseTracker
        tracker = ExpenseTracker()

        # Add expenses to different categories
        tracker.add_expense(50.00, "food", "Groceries")
        tracker.add_expense(30.00, "transport", "Bus fare")
        tracker.add_expense(100.00, "food", "Restaurant")
        tracker.add_expense(20.00, "entertainment", "Movie ticket")

        # Test getting expenses for the "food" category
        food_expenses = tracker.get_expenses_by_category("food")
        assert len(food_expenses) == 2
        assert food_expenses[0]["amount"] == 50.00
        assert food_expenses[0]["description"] == "Groceries"
        assert food_expenses[1]["amount"] == 100.00
        assert food_expenses[1]["description"] == "Restaurant"

        # Test getting expenses for a category with no expenses
        utilities_expenses = tracker.get_expenses_by_category("utilities")
        assert len(utilities_expenses) == 0

        # Test error handling for an invalid category
        with pytest.raises(ValueError):
            tracker.get_expenses_by_category("invalid_category")