import pytest
from expense_tracker import ExpenseTracker

def test_add_invalid_category():
    tracker = ExpenseTracker()

    with pytest.raises(ValueError) as exc_info:
        tracker.add_expense(50.0, "invalid", "Test expense")

    assert str(exc_info.value) == "Category must be one of: food, transport, utilities, entertainment, other"

    assert len(tracker.expenses) == 0

def test_add_valid_expense():
    tracker = ExpenseTracker()

    result = tracker.add_expense(10.0, "food", "Snacks")

    assert result == True
    assert len(tracker.expenses) == 1
    assert tracker.expenses[0] == {"amount": 10.0, "category": "food", "description": "Snacks"}

def test_get_category_total():
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(10.0, "food", "Breakfast")
    tracker.add_expense(20.0, "food", "Lunch")
    tracker.add_expense(15.0, "transport", "Uber")

    # Test getting total for a valid category
    assert tracker.get_category_total("food") == 30.0

    # Test getting total for an invalid category
    with pytest.raises(ValueError) as exc_info:
        tracker.get_category_total("invalid")

    assert str(exc_info.value) == "Category must be one of: food, transport, utilities, entertainment, other"