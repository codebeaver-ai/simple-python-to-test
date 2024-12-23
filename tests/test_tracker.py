from expense_tracker import ExpenseTracker

import pytest

def test_add_expense_invalid_category():
    tracker = ExpenseTracker()

    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.add_expense(50.0, "invalid category", "Test expense")

def test_add_expense_valid_category():
    tracker = ExpenseTracker()

    result = tracker.add_expense(50.0, "food", "Test expense")
    assert result == True

    expenses = tracker.get_expenses_by_category("food")
    assert len(expenses) == 1
    assert expenses[0]["amount"] == 50.0
    assert expenses[0]["category"] == "food"
    assert expenses[0]["description"] == "Test expense"

def test_add_category():
    tracker = ExpenseTracker()

    # Test adding a new category
    result = tracker.add_category("shopping")
    assert result == True
    assert "shopping" in tracker.categories

    # Test adding a duplicate category
    result = tracker.add_category("shopping")
    assert result == False
    assert len(tracker.categories) == 6

    # Test adding an empty category (should raise ValueError)
    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.add_category("")