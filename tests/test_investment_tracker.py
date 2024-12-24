from expense_tracker import ExpenseTracker
import pytest

from investment_tracker import InvestmentTracker
from unittest.mock import patch

from investment_tracker import InvestmentTracker 

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

def test_record_transaction_invalid():
    tracker = InvestmentTracker()

    # Test adding an expense with an invalid negative amount
    with pytest.raises(ValueError) as excinfo:
        tracker.record_transaction(-10.0, "food", "Invalid expense")
    assert str(excinfo.value) == "Amount must be a positive number"

    # Test adding an expense with an invalid zero amount 
    with pytest.raises(ValueError) as excinfo:
        tracker.record_transaction(0, "transport", "Invalid expense")
    assert str(excinfo.value) == "Amount must be a positive number"

    # Test adding an expense with an invalid non-numeric amount
    with pytest.raises(ValueError) as excinfo:
        tracker.record_transaction("abc", "utilities", "Invalid expense") 
    assert str(excinfo.value) == "Amount must be a positive number"

    # Test adding an expense with an invalid category    
    with pytest.raises(ValueError) as excinfo:
        tracker.record_transaction(50.0, "invalid", "Invalid category")
    assert str(excinfo.value) == "Category must be one of: food, transport, utilities, entertainment, other"

    # Test that no expenses were added
    assert len(tracker.expenses) == 0

def test_register_new_category():
    tracker = InvestmentTracker()

    # Test adding a valid new category
    assert tracker.register_new_category("shopping") == True
    assert "shopping" in tracker.categories

    # Test adding the same category again 
    assert tracker.register_new_category("shopping") == False

    # Test adding an invalid empty category
    with pytest.raises(ValueError) as excinfo:
        tracker.register_new_category("")
    assert str(excinfo.value) == "Category must be a non-empty string"

    # Test adding an invalid category with only whitespace
    with pytest.raises(ValueError) as excinfo:
        tracker.register_new_category("  ")
    assert str(excinfo.value) == "Category must be a non-empty string"

def test_main(capsys):
    with patch("investment_tracker.InvestmentTracker") as mock_tracker:
        mock_instance = mock_tracker.return_value
        mock_instance.calculate_overall_spending.return_value = 210.50
        mock_instance.filter_by_category.return_value = [
            {"amount": 25.50, "description": "Lunch at cafe"}
        ]

        import investment_tracker
        investment_tracker.main()

        captured = capsys.readouterr()
        assert "Total expenses: $210.50" in captured.out
        assert "$25.50 - Lunch at cafe" in captured.out

        mock_tracker.assert_called_once()
        mock_instance.record_transaction.assert_any_call(25.50, "food", "Lunch at cafe")
        mock_instance.record_transaction.assert_any_call(35.00, "transport", "Uber ride")
        mock_instance.record_transaction.assert_any_call(150.00, "utilities", "Electricity bill")
        mock_instance.calculate_overall_spending.assert_called_once()
        mock_instance.filter_by_category.assert_called_once_with("food")