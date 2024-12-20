from expense_tracker import ExpenseTracker

import pytest

def test_add_category():
    tracker = ExpenseTracker()

    # Add a new category
    new_category = "shopping"
    assert tracker.add_category(new_category) == True

    # Check that the new category was added
    assert new_category in tracker.categories

    # Try adding the same category again
    assert tracker.add_category(new_category) == False

def test_expense_tracking():
    tracker = ExpenseTracker()

    # Add some expenses
    tracker.add_expense(10.0, "food", "Lunch")
    tracker.add_expense(5.0, "transport", "Bus fare")
    tracker.add_expense(15.0, "food", "Dinner")

    # Check total expenses
    assert tracker.get_total_expenses() == 30.0

    # Check expenses by category
    food_expenses = tracker.get_expenses_by_category("food")
    assert len(food_expenses) == 2
    assert sum(expense["amount"] for expense in food_expenses) == 25.0

    transport_expenses = tracker.get_expenses_by_category("transport")
    assert len(transport_expenses) == 1
    assert transport_expenses[0]["amount"] == 5.0

def test_add_expense_invalid_data():
    tracker = ExpenseTracker()

    # Test adding expense with invalid amount
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        tracker.add_expense(-10, "food", "Invalid amount")

    with pytest.raises(ValueError, match="Amount must be a positive number"):
        tracker.add_expense("not a number", "food", "Invalid amount")

    # Test adding expense with invalid category
    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.add_expense(10, "invalid category", "Invalid category")