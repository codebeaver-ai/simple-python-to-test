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

    def test_get_category_total(self):
        """
        Test the get_category_total method of ExpenseTracker.

        This test checks:
        1. The correct total is returned for a specific category
        2. The method raises a ValueError for an invalid category
        """
        tracker = ExpenseTracker()

        # Add some expenses
        tracker.add_expense(50.00, "food", "Groceries")
        tracker.add_expense(30.00, "food", "Restaurant")
        tracker.add_expense(20.00, "transport", "Bus ticket")

        # Test getting total for a valid category
        assert tracker.get_category_total("food") == 80.00

        # Test getting total for a category with no expenses
        assert tracker.get_category_total("utilities") == 0.00

        # Test raising ValueError for an invalid category
        with pytest.raises(ValueError):
            tracker.get_category_total("invalid_category")

    def test_get_expenses_by_category(self):
        """
        Test the get_expenses_by_category method of ExpenseTracker.

        This test checks:
        1. The correct expenses are returned for a specific category
        2. An empty list is returned for a category with no expenses
        3. The method raises a ValueError for an invalid category
        """
        tracker = ExpenseTracker()

        # Add some expenses
        tracker.add_expense(50.00, "food", "Groceries")
        tracker.add_expense(30.00, "food", "Restaurant")
        tracker.add_expense(20.00, "transport", "Bus ticket")

        # Test getting expenses for a valid category
        food_expenses = tracker.get_expenses_by_category("food")
        assert len(food_expenses) == 2
        assert food_expenses[0]["amount"] == 50.00
        assert food_expenses[1]["amount"] == 30.00

        # Test getting expenses for a category with no expenses
        utilities_expenses = tracker.get_expenses_by_category("utilities")
        assert len(utilities_expenses) == 0

        # Test raising ValueError for an invalid category
        with pytest.raises(ValueError):
            tracker.get_expenses_by_category("invalid_category")

    def test_get_total_expenses(self):
        """
        Test the get_total_expenses method of ExpenseTracker.

        This test checks:
        1. The correct total is returned when there are expenses
        2. The total is 0 when there are no expenses
        3. The total is correctly updated after adding new expenses
        """
        tracker = ExpenseTracker()

        # Test when there are no expenses
        assert tracker.get_total_expenses() == 0.00

        # Add some expenses
        tracker.add_expense(50.00, "food", "Groceries")
        tracker.add_expense(30.00, "transport", "Bus ticket")
        tracker.add_expense(20.00, "entertainment", "Movie")

        # Test the total after adding expenses
        assert tracker.get_total_expenses() == 100.00

        # Add another expense and check if the total is updated
        tracker.add_expense(25.50, "food", "Restaurant")
        assert tracker.get_total_expenses() == 125.50

    def test_add_expense_invalid_inputs(self):
        """
        Test the add_expense method of ExpenseTracker with invalid inputs.

        This test checks:
        1. Adding an expense with a negative amount raises a ValueError
        2. Adding an expense with a non-numeric amount raises a ValueError
        3. Adding an expense with an invalid category raises a ValueError
        """
        tracker = ExpenseTracker()

        # Test adding an expense with a negative amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.add_expense(-50.00, "food", "Negative expense")

        # Test adding an expense with a non-numeric amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.add_expense("not a number", "food", "Invalid amount")

        # Test adding an expense with an invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.add_expense(50.00, "invalid_category", "Invalid category")

    def test_add_expense_valid(self):
        """
        Test the add_expense method of ExpenseTracker with valid inputs.

        This test checks:
        1. Adding a valid expense returns True
        2. The expense is correctly added to the expenses list
        3. The expense details (amount, category, description) are correctly stored
        """
        tracker = ExpenseTracker()

        # Add a valid expense
        result = tracker.add_expense(75.50, "food", "Dinner at restaurant")

        # Check if the method returns True
        assert result == True

        # Check if the expense was added to the list
        assert len(tracker.expenses) == 1

        # Check if the expense details are correct
        added_expense = tracker.expenses[0]
        assert added_expense["amount"] == 75.50
        assert added_expense["category"] == "food"
        assert added_expense["description"] == "Dinner at restaurant"

    def test_category_case_insensitivity(self):
        """
        Test that category names are case-insensitive in the add_expense method.

        This test checks:
        1. Expenses can be added with differently cased category names
        2. The get_category_total method treats differently cased category names as the same category
        """
        tracker = ExpenseTracker()

        # Add expenses with differently cased category names
        tracker.add_expense(50.00, "Food", "Groceries")
        tracker.add_expense(30.00, "food", "Restaurant")
        tracker.add_expense(20.00, "FOOD", "Snacks")

        # Check if all expenses are summed together regardless of case
        assert tracker.get_category_total("food") == 100.00
        assert tracker.get_category_total("Food") == 100.00
        assert tracker.get_category_total("FOOD") == 100.00

        # Verify that the number of expenses in the "food" category is correct
        food_expenses = tracker.get_expenses_by_category("food")
        assert len(food_expenses) == 3