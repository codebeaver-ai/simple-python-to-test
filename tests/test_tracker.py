import pytest
from expense_tracker import ExpenseTracker

from expense_tracker import ExpenseTracker
import pytest

from expense_tracker import ExpenseTracker
import pytest










def test_add_category():
    tracker = ExpenseTracker()

    # Test adding a new valid category
    assert tracker.add_category("shopping") == True
    assert "shopping" in tracker.categories

    # Test adding an existing category
    assert tracker.add_category("food") == False
    assert len(tracker.categories) == 6  # Original 5 categories + "shopping"

    # Test adding an invalid category (empty string)
    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.add_category("")

    # Test adding an invalid category (non-string)
    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.add_category(123)


def test_get_category_total():
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(50.00, "food", "Groceries")
    tracker.add_expense(20.00, "food", "Snacks")
    tracker.add_expense(100.00, "utilities", "Electricity bill")

    # Test with a valid category that has expenses
    assert tracker.get_category_total("food") == 70.00

    # Test with a valid category that has no expenses
    assert tracker.get_category_total("transport") == 0

    # Test with an invalid category
    with pytest.raises(ValueError, match="Category must be one of: food, transport, utilities, entertainment, other"):
        tracker.get_category_total("invalid_category")


def test_get_expenses_by_category():
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(50.00, "food", "Groceries")
    tracker.add_expense(20.00, "transport", "Uber ride")
    tracker.add_expense(100.00, "utilities", "Electricity bill")
    tracker.add_expense(30.00, "food", "Restaurant dinner")

    # Test with a valid category
    food_expenses = tracker.get_expenses_by_category("food")
    assert len(food_expenses) == 2
    assert food_expenses[0]["amount"] == 50.00
    assert food_expenses[0]["description"] == "Groceries"
    assert food_expenses[1]["amount"] == 30.00
    assert food_expenses[1]["description"] == "Restaurant dinner"

    # Test with an invalid category
    with pytest.raises(ValueError, match="Category must be one of: food, transport, utilities, entertainment, other"):
        tracker.get_expenses_by_category("invalid_category")
