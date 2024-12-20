import pytest
from expense_tracker import ExpenseTracker

import pytest 

def test_add_expense_invalid_category():
    tracker = ExpenseTracker()
    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.add_expense(50.0, "invalid category", "Test expense")

def test_add_valid_expense():
    tracker = ExpenseTracker()

    amount = 10.50
    category = "food"
    description = "Lunch"

    tracker.add_expense(amount, category, description)

    assert tracker.get_total_expenses() == amount

    expenses = tracker.get_expenses_by_category(category)
    assert len(expenses) == 1
    assert expenses[0]["amount"] == amount
    assert expenses[0]["category"] == category
    assert expenses[0]["description"] == description

def test_add_category():
    tracker = ExpenseTracker()

    # Test adding a valid new category
    assert tracker.add_category("shopping") == True
    assert "shopping" in tracker.categories

    # Test adding a category that already exists
    assert tracker.add_category("food") == False
    assert len(tracker.categories) == 6 # Unchanged

    # Test adding an invalid empty category 
    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.add_category("")

    # Test adding an invalid whitespace category
    with pytest.raises(ValueError, match="Category must be a non-empty string"):  
        tracker.add_category("  ")