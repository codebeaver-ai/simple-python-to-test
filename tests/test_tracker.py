import pytest
from expense_tracker import ExpenseTracker

def test_add_category():
    tracker = ExpenseTracker()

    # Test adding a new valid category
    assert tracker.add_category("shopping") == True
    assert "shopping" in tracker.categories

    # Test adding a duplicate category
    assert tracker.add_category("shopping") == False
    assert len(tracker.categories) == 6  # Expecting 5 original categories + 1 new

    # Test adding an invalid empty string category
    with pytest.raises(ValueError):
        tracker.add_category("")

def test_add_whitespace_category():
    tracker = ExpenseTracker()

    with pytest.raises(ValueError):
        tracker.add_category("   ")

    assert len(tracker.categories) == 5  # Should still only have the original 5 categories

def test_add_expenses_and_get_totals():
    tracker = ExpenseTracker()

    # Add valid expenses
    assert tracker.add_expense(10.50, "food", "Groceries") == True
    assert tracker.add_expense(5.00, "transport", "Bus fare") == True
    assert tracker.add_expense(7.50, "food", "Takeout") == True

    # Adding invalid expense with non-positive amount should raise ValueError
    with pytest.raises(ValueError):
        tracker.add_expense(-5.00, "entertainment", "Movie")

    # Adding invalid expense with invalid category should raise ValueError  
    with pytest.raises(ValueError):
        tracker.add_expense(12.00, "invalid category", "Something")

    # Check total expenses
    assert tracker.get_total_expenses() == 23.00

    # Check getting food expenses
    food_expenses = tracker.get_expenses_by_category("food")
    assert len(food_expenses) == 2
    assert food_expenses[0]['amount'] == 10.50
    assert food_expenses[1]['amount'] == 7.50

    # Check food category total
    assert tracker.get_category_total("food") == 18.00

    # Check transport category total
    assert tracker.get_category_total("transport") == 5.00

    # Getting invalid category should raise ValueError
    with pytest.raises(ValueError):
        tracker.get_expenses_by_category("invalid")

    with pytest.raises(ValueError):  
        tracker.get_category_total("invalid")