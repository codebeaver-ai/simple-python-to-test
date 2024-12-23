from expense_tracker import ExpenseTracker
import pytest

def test_add_category():
    tracker = ExpenseTracker()

    # Test adding a valid category
    assert tracker.add_category("shopping") == True
    assert "shopping" in tracker.categories

    # Test adding an invalid category (empty string)
    with pytest.raises(ValueError):
        tracker.add_category("")

def test_get_category_total():
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(50.00, "food", "Groceries")
    tracker.add_expense(30.00, "food", "Dinner")
    tracker.add_expense(20.00, "transport", "Taxi")

    # Test getting total for a valid category
    assert tracker.get_category_total("food") == 80.00

    # Test getting total for an invalid category
    with pytest.raises(ValueError):
        tracker.get_category_total("invalid_category")

def test_get_expenses_by_category():
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(50.00, "food", "Groceries")
    tracker.add_expense(30.00, "food", "Dinner")
    tracker.add_expense(20.00, "transport", "Taxi")

    # Test getting expenses for a valid category
    food_expenses = tracker.get_expenses_by_category("food")
    assert len(food_expenses) == 2
    assert food_expenses[0]["amount"] == 50.00
    assert food_expenses[0]["description"] == "Groceries"
    assert food_expenses[1]["amount"] == 30.00
    assert food_expenses[1]["description"] == "Dinner"

    # Test getting expenses for an invalid category
    with pytest.raises(ValueError):
        tracker.get_expenses_by_category("invalid_category")