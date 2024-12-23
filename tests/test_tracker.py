import pytest
from expense_tracker import ExpenseTracker

def test_add_category():
    tracker = ExpenseTracker()

    # Add valid new category
    assert tracker.add_category("Shopping") == True
    assert "shopping" in tracker.categories

    # Try adding invalid empty category 
    with pytest.raises(ValueError):
        tracker.add_category("")

    # Try adding duplicate category
    assert tracker.add_category("Food") == False
    assert len(tracker.categories) == 6  # no duplicates added

def test_get_category_total():
    tracker = ExpenseTracker()

    # Add sample expenses
    tracker.add_expense(10.0, "food", "groceries")
    tracker.add_expense(25.50, "food", "dinner out")
    tracker.add_expense(15.75, "transport", "taxi") 
    tracker.add_expense(50.00, "entertainment", "movie tickets")

    # Test category total
    assert tracker.get_category_total("food") == 35.50

    # Test invalid category raises error
    with pytest.raises(ValueError):
        tracker.get_category_total("invalid")

def test_add_expense():
    tracker = ExpenseTracker()

    # Test adding a valid expense
    assert tracker.add_expense(15.50, "food", "groceries") == True
    assert len(tracker.expenses) == 1
    assert tracker.expenses[0] == {"amount": 15.50, "category": "food", "description": "groceries"}

    # Test adding expense with invalid negative amount
    with pytest.raises(ValueError):
        tracker.add_expense(-10.00, "food", "negative")

    # Test adding expense with invalid empty category
    with pytest.raises(ValueError):
        tracker.add_expense(5.00, "", "no category")

    # Test adding expense with invalid category 
    with pytest.raises(ValueError):
        tracker.add_expense(12.00, "invalid", "test")

    # Check no invalid expenses were added
    assert len(tracker.expenses) == 1