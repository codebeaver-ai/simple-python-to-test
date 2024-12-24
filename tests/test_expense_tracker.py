from expense_tracker import ExpenseTracker

import pytest

from unittest.mock import patch

def test_add_category():
    tracker = ExpenseTracker()

    # Test adding a new category
    assert tracker.add_category("shopping") == True
    assert "shopping" in tracker.categories

    # Test adding an existing category
    assert tracker.add_category("food") == False
    assert tracker.categories.count("food") == 1

    # Test adding invalid categories
    with pytest.raises(ValueError):
        tracker.add_category("")

    with pytest.raises(ValueError):
        tracker.add_category(42)

def test_get_total_expenses():
    tracker = ExpenseTracker()

    # Add sample expenses
    tracker.add_expense(10.0, "food", "Breakfast")
    tracker.add_expense(20.0, "transport", "Taxi ride")
    tracker.add_expense(15.0, "entertainment", "Movie tickets")

    # Verify total expenses
    assert tracker.get_total_expenses() == 45.0

def test_get_expenses_by_category_invalid():
    tracker = ExpenseTracker()

    # Add sample expenses
    tracker.add_expense(10.0, "food", "Breakfast")
    tracker.add_expense(20.0, "transport", "Taxi ride")
    tracker.add_expense(15.0, "entertainment", "Movie tickets")

    # Test getting expenses for an invalid category
    with pytest.raises(ValueError) as exc_info:
        tracker.get_expenses_by_category("invalid")
    assert str(exc_info.value) == "Category must be one of: food, transport, utilities, entertainment, other"

    # Test getting expenses for a valid category with no expenses
    with patch.object(tracker, 'categories', new={'food', 'new_category'}):
        expenses = tracker.get_expenses_by_category("new_category")
        assert expenses == []