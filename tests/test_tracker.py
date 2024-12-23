from expense_tracker import ExpenseTracker

import pytest

def test_add_category():
    tracker = ExpenseTracker()

    # Test adding a new valid category
    assert tracker.add_category("shopping") == True
    assert "shopping" in tracker.categories

    # Test adding a category that already exists
    assert tracker.add_category("food") == False
    assert len(tracker.categories) == 6  # Ensure no duplicates added

    # Test adding an invalid category (empty string)
    with pytest.raises(ValueError):
        tracker.add_category("")

def test_get_category_total():
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(25.50, "food", "Lunch at cafe")
    tracker.add_expense(35.00, "transport", "Uber ride")
    tracker.add_expense(150.00, "utilities", "Electricity bill")
    tracker.add_expense(50.00, "food", "Dinner at restaurant")

    # Test getting total for a valid category
    assert tracker.get_category_total("food") == 75.50

    # Test getting total for a category with no expenses
    assert tracker.get_category_total("entertainment") == 0

    # Test getting total for an invalid category
    with pytest.raises(ValueError):
        tracker.get_category_total("invalid_category")

def test_get_expenses_by_category():
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(25.50, "food", "Lunch at cafe")
    tracker.add_expense(35.00, "transport", "Uber ride")
    tracker.add_expense(150.00, "utilities", "Electricity bill")
    tracker.add_expense(50.00, "food", "Dinner at restaurant")

    # Test getting expenses for a valid category
    food_expenses = tracker.get_expenses_by_category("food")
    assert len(food_expenses) == 2
    assert food_expenses[0]["amount"] == 25.50
    assert food_expenses[0]["description"] == "Lunch at cafe"
    assert food_expenses[1]["amount"] == 50.00
    assert food_expenses[1]["description"] == "Dinner at restaurant"

    # Test getting expenses for a category with no expenses
    entertainment_expenses = tracker.get_expenses_by_category("entertainment")
    assert len(entertainment_expenses) == 0

    # Test getting expenses for an invalid category
    with pytest.raises(ValueError):
        tracker.get_expenses_by_category("invalid_category")