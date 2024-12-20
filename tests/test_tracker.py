import pytest
from expense_tracker import ExpenseTracker

import pytest
from expense_tracker import ExpenseTracker

import pytest
from expense_tracker import ExpenseTracker










def test_add_category():
    tracker = ExpenseTracker()

    # Test adding a new valid category
    assert tracker.add_category("shopping") == True
    assert "shopping" in tracker.categories

    # Test adding a category that already exists
    assert tracker.add_category("food") == False
    assert len(tracker.categories) == 6

    # Test adding an invalid category (empty string)
    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.add_category("")

    # Test adding an invalid category (not a string)
    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.add_category(123)


def test_add_expense():
    tracker = ExpenseTracker()

    # Test adding a valid expense
    assert tracker.add_expense(50.0, "food", "Groceries") == True
    assert len(tracker.expenses) == 1
    assert tracker.expenses[0]["amount"] == 50.0
    assert tracker.expenses[0]["category"] == "food"
    assert tracker.expenses[0]["description"] == "Groceries"
    assert tracker.get_total_expenses() == 50.0

    # Test adding an expense with an invalid amount
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        tracker.add_expense(-10.0, "transport", "Bus fare")

    # Test adding an expense with an invalid category
    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.add_expense(20.0, "invalid", "Invalid category")


def test_get_expenses_by_category_and_total():
    tracker = ExpenseTracker()

    # Add sample expenses
    tracker.add_expense(50.0, "food", "Groceries")
    tracker.add_expense(20.0, "transport", "Uber ride")
    tracker.add_expense(30.0, "food", "Restaurant dinner")
    tracker.add_expense(100.0, "utilities", "Electricity bill")

    # Test getting expenses by category
    food_expenses = tracker.get_expenses_by_category("food")
    assert len(food_expenses) == 2
    assert food_expenses[0]["amount"] == 50.0
    assert food_expenses[0]["description"] == "Groceries"
    assert food_expenses[1]["amount"] == 30.0
    assert food_expenses[1]["description"] == "Restaurant dinner"

    # Test getting category total
    food_total = tracker.get_category_total("food")
    assert food_total == 80.0

    # Test getting expenses for an invalid category
    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.get_expenses_by_category("invalid")

    # Test getting total for an invalid category
    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.get_category_total("invalid")
