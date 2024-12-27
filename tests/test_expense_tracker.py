import pytest
from expense_tracker import ExpenseTracker

def test_add_category():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Test adding a new category
    assert tracker.add_category("groceries") == True
    assert "groceries" in tracker.categories

    # Test adding an existing category (should return False)
    assert tracker.add_category("groceries") == False

    # Test adding an invalid category (empty string)
    with pytest.raises(ValueError):
        tracker.add_category("")

    # Test adding an invalid category (non-string)
    with pytest.raises(ValueError):
        tracker.add_category(123)

def test_get_total_expenses():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(25.50, "food", "Lunch at cafe")
    tracker.add_expense(35.00, "transport", "Uber ride")
    tracker.add_expense(150.00, "utilities", "Electricity bill")

    # Calculate the expected total
    expected_total = 25.50 + 35.00 + 150.00

    # Get the total expenses from the tracker
    actual_total = tracker.get_total_expenses()

    # Assert that the actual total matches the expected total
    assert actual_total == pytest.approx(expected_total, rel=1e-9)

def test_get_category_total():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Add expenses to different categories
    tracker.add_expense(50.00, "food", "Grocery shopping")
    tracker.add_expense(30.00, "food", "Restaurant dinner")
    tracker.add_expense(25.00, "transport", "Bus ticket")
    tracker.add_expense(100.00, "utilities", "Electricity bill")

    # Test get_category_total for food category
    assert tracker.get_category_total("food") == pytest.approx(80.00)

    # Test get_category_total for transport category
    assert tracker.get_category_total("transport") == pytest.approx(25.00)

    # Test get_category_total for utilities category
    assert tracker.get_category_total("utilities") == pytest.approx(100.00)

    # Test get_category_total for a category with no expenses
    assert tracker.get_category_total("entertainment") == pytest.approx(0.00)

    # Test get_category_total with an invalid category
    with pytest.raises(ValueError):
        tracker.get_category_total("invalid_category")