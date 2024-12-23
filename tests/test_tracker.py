from expense_tracker import ExpenseTracker

import pytest

def test_add_category():
    tracker = ExpenseTracker()

    # Test adding a new valid category
    assert tracker.add_category("shopping") == True
    assert "shopping" in tracker.categories

    # Test adding a category that already exists
    assert tracker.add_category("food") == False
    assert len(tracker.categories) == 6  # Original 5 plus "shopping"

    # Test adding an invalid empty category
    try:
        tracker.add_category("")
        assert False, "Expected ValueError for empty category"
    except ValueError:
        pass

    # Test adding an invalid non-string category    
    try:
        tracker.add_category(123)
        assert False, "Expected ValueError for non-string category"
    except ValueError:
        pass

def test_expense_tracking():
    tracker = ExpenseTracker()

    # Add sample expenses
    tracker.add_expense(50.00, "food", "Groceries")
    tracker.add_expense(20.00, "transport", "Gas")
    tracker.add_expense(100.00, "utilities", "Electricity")
    tracker.add_expense(30.00, "food", "Restaurant meal")
    tracker.add_expense(40.00, "entertainment", "Movie tickets")

    # Test total expenses
    assert tracker.get_total_expenses() == 240.00

    # Test expenses by category
    food_expenses = tracker.get_expenses_by_category("food")
    assert len(food_expenses) == 2
    assert food_expenses[0]["amount"] == 50.00
    assert food_expenses[1]["amount"] == 30.00

    # Test category total
    assert tracker.get_category_total("food") == 80.00
    assert tracker.get_category_total("transport") == 20.00
    assert tracker.get_category_total("utilities") == 100.00
    assert tracker.get_category_total("entertainment") == 40.00

def test_add_expense_invalid():
    tracker = ExpenseTracker()

    # Test adding an expense with a negative amount
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        tracker.add_expense(-50.00, "food", "Invalid expense")

    # Test adding an expense with an invalid category
    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.add_expense(50.00, "invalid", "Invalid category")