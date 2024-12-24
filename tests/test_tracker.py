import pytest
from unittest.mock import patch
from io import StringIO

from expense_tracker import ExpenseTracker

from investment_tracker import InvestmentTracker

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

def test_compute_category_sum():
    tracker = InvestmentTracker()

    # Add sample expenses
    tracker.record_transaction(10.0, "food", "Groceries")
    tracker.record_transaction(20.0, "transport", "Gas")
    tracker.record_transaction(5.0, "food", "Snacks")

    # Test with a valid category
    assert tracker.compute_category_sum("food") == 15.0

    # Test with an invalid category
    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.compute_category_sum("invalid")

def test_register_new_category():
    tracker = InvestmentTracker()

    # Test registering a new valid category
    assert tracker.register_new_category("shopping") == True
    assert "shopping" in tracker.categories

    # Test registering an existing category
    assert tracker.register_new_category("shopping") == False
    assert len(tracker.categories) == 6  # Original 5 categories + "shopping"

    # Test registering an invalid category (empty string)
    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.register_new_category("")

    # Test registering an invalid category (non-string)
    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.register_new_category(123)

def test_filter_by_category():
    tracker = InvestmentTracker()

    # Add sample expenses
    tracker.record_transaction(10.0, "food", "Groceries")
    tracker.record_transaction(20.0, "transport", "Gas") 
    tracker.record_transaction(5.0, "food", "Snacks")
    tracker.record_transaction(15.0, "utilities", "Electric bill")

    # Test filtering with a valid category
    food_expenses = tracker.filter_by_category("food")
    assert len(food_expenses) == 2
    assert food_expenses[0]['amount'] == 10.0
    assert food_expenses[0]['description'] == "Groceries"
    assert food_expenses[1]['amount'] == 5.0
    assert food_expenses[1]['description'] == "Snacks"

    # Test filtering with an invalid category
    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.filter_by_category("invalid")