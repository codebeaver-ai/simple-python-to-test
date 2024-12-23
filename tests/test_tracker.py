from expense_tracker import ExpenseTracker

import pytest

def test_add_category():
    tracker = ExpenseTracker()

    # Test adding a new category
    assert tracker.add_category("shopping") == True
    assert "shopping" in tracker.categories

    # Test adding an existing category
    assert tracker.add_category("food") == False
    assert len(tracker.categories) == 6  # Original 5 categories + "shopping"

    # Test adding an invalid category (empty string)
    try:
        tracker.add_category("")
        assert False, "Expected ValueError for empty category"
    except ValueError:
        pass

    # Test adding an invalid category (non-string)
    try:
        tracker.add_category(123)
        assert False, "Expected ValueError for non-string category"
    except ValueError:
        pass

def test_add_expense_invalid_category():
    tracker = ExpenseTracker()

    # Test adding an expense with an invalid category
    with pytest.raises(ValueError) as exc_info:
        tracker.add_expense(50.00, "invalid_category", "Some expense")

    assert str(exc_info.value) == "Category must be one of: food, transport, utilities, entertainment, other"

def test_get_category_total():
    tracker = ExpenseTracker()

    # Add sample expenses
    tracker.add_expense(10.0, "food", "Groceries")
    tracker.add_expense(15.0, "food", "Lunch")
    tracker.add_expense(20.0, "transport", "Gas")

    # Test getting total for a valid category
    assert tracker.get_category_total("food") == 25.0

    # Test getting total for a category with no expenses
    assert tracker.get_category_total("entertainment") == 0.0

    # Test getting total for an invalid category
    with pytest.raises(ValueError) as exc_info:
        tracker.get_category_total("invalid_category")
    assert str(exc_info.value) == "Category must be one of: food, transport, utilities, entertainment, other"