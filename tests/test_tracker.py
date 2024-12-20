import pytest
from expense_tracker import ExpenseTracker

from expense_tracker import ExpenseTracker
import pytest

from expense_tracker import ExpenseTracker
import pytest










def test_add_category():
    tracker = ExpenseTracker()
    
    # Adding a new valid category succeeds
    assert tracker.add_category("shopping") == True
    assert "shopping" in tracker.categories

    # Adding a category that already exists returns False 
    assert tracker.add_category("food") == False

    # Adding an invalid empty category raises ValueError
    with pytest.raises(ValueError):
        tracker.add_category("")


def test_get_category_total():
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(50.00, "food", "Grocery shopping")
    tracker.add_expense(20.00, "food", "Dining out")
    tracker.add_expense(30.00, "transport", "Gas")

    # Test getting total for a valid category
    assert tracker.get_category_total("food") == 70.00

    # Test getting total for an invalid category
    with pytest.raises(ValueError) as exc_info:
        tracker.get_category_total("invalid_category")
    assert str(exc_info.value) == "Category must be one of: food, transport, utilities, entertainment, other"


def test_get_expenses_by_category():
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(50.00, "food", "Grocery shopping")
    tracker.add_expense(20.00, "food", "Dining out")
    tracker.add_expense(30.00, "transport", "Gas")

    # Test getting expenses for a valid category
    food_expenses = tracker.get_expenses_by_category("food")
    assert len(food_expenses) == 2
    assert food_expenses[0]["amount"] == 50.00
    assert food_expenses[0]["description"] == "Grocery shopping"
    assert food_expenses[1]["amount"] == 20.00
    assert food_expenses[1]["description"] == "Dining out"

    # Test getting expenses for an invalid category
    with pytest.raises(ValueError) as exc_info:
        tracker.get_expenses_by_category("invalid_category")
    assert str(exc_info.value) == "Category must be one of: food, transport, utilities, entertainment, other"
