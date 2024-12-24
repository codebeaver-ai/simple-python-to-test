import pytest
from expense_tracker import ExpenseTracker

def test_add_category():
    tracker = ExpenseTracker()

    # Test adding a valid category
    assert tracker.add_category("shopping") == True
    assert "shopping" in tracker.categories

    # Test adding a category that already exists
    assert tracker.add_category("food") == False
    assert len(tracker.categories) == 6  # Original 5 categories + "shopping"

    # Test adding an invalid category (empty string)
    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.add_category("")

    # Test adding an invalid category (not a string)
    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.add_category(123)

def test_get_total_expenses():
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(10.0, "food", "Breakfast")
    tracker.add_expense(20.0, "transport", "Taxi")
    tracker.add_expense(30.0, "utilities", "Electricity bill")

    # Assert that get_total_expenses returns the correct total
    assert tracker.get_total_expenses() == 60.0

def test_get_expenses_by_category_nonexistent():
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(10.0, "food", "Breakfast")
    tracker.add_expense(20.0, "transport", "Taxi")

    # Try to get expenses for a nonexistent category
    with pytest.raises(ValueError, match="Category must be one of: food, transport, utilities, entertainment, other"):
        tracker.get_expenses_by_category("nonexistent")