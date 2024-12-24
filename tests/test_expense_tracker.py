from expense_tracker import ExpenseTracker
import pytest

def test_add_category():
    tracker = ExpenseTracker()

    # Add a valid new category
    assert tracker.add_category("shopping") == True
    assert "shopping" in tracker.categories

    # Try adding the same category again
    assert tracker.add_category("shopping") == False

    # Try adding an invalid empty category
    with pytest.raises(ValueError):
        tracker.add_category("")

def test_get_category_total():
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(10.0, "food", "Groceries")
    tracker.add_expense(15.0, "food", "Lunch") 
    tracker.add_expense(5.0, "transport", "Bus fare")

    # Test getting total for a category
    assert tracker.get_category_total("food") == 25.0
    assert tracker.get_category_total("transport") == 5.0

    # Test getting total for a category with no expenses
    assert tracker.get_category_total("utilities") == 0.0

    # Test passing an invalid category 
    with pytest.raises(ValueError) as excinfo:
        tracker.get_category_total("invalid")
    assert str(excinfo.value) == "Category must be one of: food, transport, utilities, entertainment, other"

def test_get_expenses_by_category():
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(10.0, "food", "Groceries")
    tracker.add_expense(15.0, "food", "Lunch")
    tracker.add_expense(5.0, "transport", "Bus fare")

    # Test getting expenses for a specific category
    food_expenses = tracker.get_expenses_by_category("food")
    assert len(food_expenses) == 2
    assert food_expenses[0]["amount"] == 10.0
    assert food_expenses[0]["description"] == "Groceries"
    assert food_expenses[1]["amount"] == 15.0
    assert food_expenses[1]["description"] == "Lunch"

    # Test getting expenses for a category with no expenses
    utility_expenses = tracker.get_expenses_by_category("utilities")
    assert len(utility_expenses) == 0

    # Test passing an invalid category
    with pytest.raises(ValueError) as excinfo:
        tracker.get_expenses_by_category("invalid")
    assert str(excinfo.value) == "Category must be one of: food, transport, utilities, entertainment, other"