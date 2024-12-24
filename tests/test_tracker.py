import pytest
from expense_tracker import ExpenseTracker

from unittest.mock import patch
from io import StringIO
from expense_tracker import ExpenseTracker, main

def test_add_expense_invalid_category():
    tracker = ExpenseTracker()

    # Test adding an expense with an invalid category
    with pytest.raises(ValueError) as exc_info:
        tracker.add_expense(50.0, "invalid_category", "Test expense")
    assert str(exc_info.value) == "Category must be one of: food, transport, utilities, entertainment, other"

    # Test adding a new category and retrieving expenses by that category
    tracker.add_category("new_category")
    tracker.add_expense(75.0, "new_category", "New category expense")
    new_category_expenses = tracker.get_expenses_by_category("new_category")
    assert len(new_category_expenses) == 1
    assert new_category_expenses[0]["amount"] == 75.0
    assert new_category_expenses[0]["category"] == "new_category"
    assert new_category_expenses[0]["description"] == "New category expense"

def test_add_expense_invalid_amount():
    tracker = ExpenseTracker()

    with pytest.raises(ValueError) as exc_info:
        tracker.add_expense(0, "food", "Zero expense")
    assert str(exc_info.value) == "Amount must be a positive number"

    with pytest.raises(ValueError) as exc_info:
        tracker.add_expense(-10.0, "transport", "Negative expense") 
    assert str(exc_info.value) == "Amount must be a positive number"

def test_main_function(capsys):
    with patch('sys.stdout', new=StringIO()) as fake_output:
        main()

    captured = fake_output.getvalue()
    expected_output = '''Total expenses: $210.50

Food expenses:
$25.50 - Lunch at cafe
'''
    assert captured == expected_output