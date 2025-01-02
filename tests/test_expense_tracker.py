import pytest

from expense_tracker import ExpenseTracker

class TestExpenseTracker:
    def test_add_category(self):
        tracker = ExpenseTracker()
        initial_category_count = len(tracker.categories)

        # Test adding a new category
        result = tracker.add_category("groceries")
        assert result == True
        assert len(tracker.categories) == initial_category_count + 1
        assert "groceries" in tracker.categories

        # Test adding an existing category
        result = tracker.add_category("groceries")
        assert result == False
        assert len(tracker.categories) == initial_category_count + 1

        # Test adding an invalid category
        with pytest.raises(ValueError):
            tracker.add_category("")

        with pytest.raises(ValueError):
            tracker.add_category(123)

    def test_get_category_total(self):
        tracker = ExpenseTracker()

        # Add some expenses
        tracker.add_expense(50.0, "food", "Grocery shopping")
        tracker.add_expense(30.0, "food", "Restaurant dinner")
        tracker.add_expense(20.0, "transport", "Bus ticket")

        # Test getting total for a specific category
        assert tracker.get_category_total("food") == 80.0
        assert tracker.get_category_total("transport") == 20.0
        assert tracker.get_category_total("utilities") == 0.0  # No expenses in this category

        # Test invalid category
        with pytest.raises(ValueError):
            tracker.get_category_total("invalid_category")

    def test_get_expenses_by_category(self):
        tracker = ExpenseTracker()

        # Add expenses in different categories
        tracker.add_expense(50.0, "food", "Grocery shopping")
        tracker.add_expense(30.0, "food", "Restaurant dinner")
        tracker.add_expense(20.0, "transport", "Bus ticket")
        tracker.add_expense(100.0, "utilities", "Electricity bill")

        # Test getting expenses for a specific category
        food_expenses = tracker.get_expenses_by_category("food")
        assert len(food_expenses) == 2
        assert all(expense["category"] == "food" for expense in food_expenses)
        assert {"amount": 50.0, "category": "food", "description": "Grocery shopping"} in food_expenses
        assert {"amount": 30.0, "category": "food", "description": "Restaurant dinner"} in food_expenses

        # Test category with single expense
        transport_expenses = tracker.get_expenses_by_category("transport")
        assert len(transport_expenses) == 1
        assert transport_expenses[0] == {"amount": 20.0, "category": "transport", "description": "Bus ticket"}

        # Test category with no expenses
        entertainment_expenses = tracker.get_expenses_by_category("entertainment")
        assert len(entertainment_expenses) == 0

        # Test invalid category
        with pytest.raises(ValueError):
            tracker.get_expenses_by_category("invalid_category")

    def test_get_total_expenses(self):
        tracker = ExpenseTracker()

        # Test with no expenses
        assert tracker.get_total_expenses() == 0

        # Add expenses across different categories
        tracker.add_expense(50.0, "food", "Grocery shopping")
        tracker.add_expense(30.0, "transport", "Taxi ride")
        tracker.add_expense(100.0, "utilities", "Electricity bill")
        tracker.add_expense(20.5, "entertainment", "Movie ticket")

        # Test total expenses
        expected_total = 50.0 + 30.0 + 100.0 + 20.5
        assert tracker.get_total_expenses() == expected_total

        # Add another expense and recheck
        tracker.add_expense(15.75, "food", "Coffee and snack")
        expected_total += 15.75
        assert tracker.get_total_expenses() == expected_total

    def test_add_expense_invalid_inputs(self):
        tracker = ExpenseTracker()

        # Test invalid amount (negative number)
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.add_expense(-50.0, "food", "Invalid expense")

        # Test invalid amount (zero)
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.add_expense(0, "food", "Invalid expense")

        # Test invalid amount (non-numeric)
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.add_expense("not a number", "food", "Invalid expense")

        # Test invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.add_expense(50.0, "invalid_category", "Invalid category expense")

        # Test valid expense (to ensure the method still works correctly)
        assert tracker.add_expense(50.0, "food", "Valid expense") == True

        # Verify that only the valid expense was added
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0] == {"amount": 50.0, "category": "food", "description": "Valid expense"}

    def test_add_expense_case_insensitive_category(self):
        tracker = ExpenseTracker()

        # Test adding an expense with uppercase category
        assert tracker.add_expense(30.0, "FOOD", "Lunch") == True

        # Verify that the expense was added with lowercase category
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0] == {"amount": 30.0, "category": "food", "description": "Lunch"}

        # Test adding an expense with mixed case category
        assert tracker.add_expense(20.0, "EnTeRtAiNmEnT", "Movie") == True

        # Verify that the expense was added with lowercase category
        assert len(tracker.expenses) == 2
        assert tracker.expenses[1] == {"amount": 20.0, "category": "entertainment", "description": "Movie"}

        # Verify that get_expenses_by_category works with case-insensitive input
        food_expenses = tracker.get_expenses_by_category("FoOd")
        assert len(food_expenses) == 1
        assert food_expenses[0] == {"amount": 30.0, "category": "food", "description": "Lunch"}

    def test_add_expense_with_spaced_category(self):
        tracker = ExpenseTracker()

        # Test adding an expense with spaces in the category name
        result = tracker.add_expense(40.0, "  FoOd  ", "Dinner")

        # Check if the expense was added successfully
        assert result == True

        # Verify that the expense was added with the correct category (stripped and lowercase)
        assert len(tracker.expenses) == 1
        added_expense = tracker.expenses[0]
        assert added_expense["amount"] == 40.0
        assert added_expense["category"] == "food"
        assert added_expense["description"] == "Dinner"

        # Verify that get_expenses_by_category works with the stripped category
        food_expenses = tracker.get_expenses_by_category("food")
        assert len(food_expenses) == 1
        assert food_expenses[0] == added_expense

    def test_add_category_with_spaces(self):
        tracker = ExpenseTracker()
        initial_category_count = len(tracker.categories)

        # Test adding a category with leading and trailing spaces
        result = tracker.add_category("  New Category  ")
        assert result == True
        assert len(tracker.categories) == initial_category_count + 1
        assert "new category" in tracker.categories  # Should be lowercase and stripped

        # Test adding the same category with different spacing
        result = tracker.add_category("New Category")
        assert result == False  # Should not add duplicate category
        assert len(tracker.categories) == initial_category_count + 1

        # Verify that the category can be used in add_expense
        assert tracker.add_expense(50.0, "  New Category  ", "Test expense") == True
        expenses

def test_add_expense_with_float_amount(self):
    tracker = ExpenseTracker()

    # Add an expense with a float amount
    result = tracker.add_expense(15.75, "food", "Lunch")

    # Check if the expense was added successfully
    assert result == True

    # Verify that the total expenses reflect the float amount accurately
    assert tracker.get_total_expenses() == 15.75

    # Check if the expense details are correctly stored
    assert len(tracker.expenses) == 1
    assert tracker.expenses[0] == {"amount": 15.75, "category": "food", "description": "Lunch"}

    # Add another float expense and check the total
    tracker.add_expense(10.50, "transport", "Bus fare")
    assert tracker.get_total_expenses() == 26.25  # 15.75 + 10.50

    # Verify that both expenses are stored correctly
    assert len(tracker.expenses) == 2
    assert tracker.expenses[1] == {"amount": 10.50, "category": "transport", "description": "Bus fare"}

def test_add_expense_with_integer_amount(self):
    tracker = ExpenseTracker()

    # Add an expense with an integer amount
    result = tracker.add_expense(20, "food", "Dinner")

    # Check if the expense was added successfully
    assert result == True

    # Verify that the total expenses reflect the integer amount accurately
    assert tracker.get_total_expenses() == 20

    # Check if the expense details are correctly stored
    assert len(tracker.expenses) == 1
    assert tracker.expenses[0] == {"amount": 20, "category": "food", "description": "Dinner"}

    # Add another integer expense and check the total
    tracker.add_expense(15, "transport", "Taxi")
    assert tracker.get_total_expenses() == 35  # 20 + 15

    # Verify that both expenses are stored correctly
    assert len(tracker.expenses) == 2
    assert tracker.expenses[1] == {"amount": 15, "category": "transport", "description": "Taxi"}