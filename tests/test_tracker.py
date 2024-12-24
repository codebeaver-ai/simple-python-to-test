import pytest
from unittest.mock import patch
from io import StringIO

from expense_tracker import ExpenseTracker

def test_main_prints_total_and_food_expenses(capsys):
    with patch('sys.stdout', new=StringIO()) as fake_output:
        # Call the main function
        main()

    # Get the printed output from the main function
    captured = fake_output.getvalue()

    # Check that total expenses are printed
    assert "Total expenses: $210.50" in captured

    # Check that food expenses are printed with amount and description
    assert "Food expenses:" in captured
    assert "$25.50 - Lunch at cafe" in captured

def test_add_category():
    tracker = ExpenseTracker()

    # Test adding a new category
    assert tracker.add_category("shopping") == True
    assert "shopping" in tracker.categories

    # Test adding an existing category
    assert tracker.add_category("shopping") == False

    # Test adding an empty or non-string category
    with pytest.raises(ValueError):
        tracker.add_category("")

    with pytest.raises(ValueError):
        tracker.add_category(123)

def test_add_expense_invalid():
    tracker = ExpenseTracker()

    # Test adding an expense with invalid amount
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        tracker.add_expense(-10, "food", "Invalid expense")

    # Test adding an expense with invalid category  
    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.add_expense(50, "invalid category", "Invalid expense")