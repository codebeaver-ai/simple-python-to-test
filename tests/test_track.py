import pytest
from expense_tracker import ExpenseTracker

from expense_tracker import ExpenseTracker
import pytest

from expense_tracker import ExpenseTracker
import pytest

import pytest
from datetime import datetime
from expense_tracker import record_transaction

import pytest
from expense_tracker import record_transaction

from expense_tracker import record_transaction
from unittest.mock import patch
from datetime import datetime



















def test_add_category():
    tracker = ExpenseTracker()

    # Test adding a new valid category
    assert tracker.add_category("shopping") == True
    assert "shopping" in tracker.categories

    # Test adding an existing category
    assert tracker.add_category("food") == False
    assert len(tracker.categories) == 6  # Original 5 categories + "shopping"

    # Test adding an invalid category (empty string)
    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.add_category("")

    # Test adding an invalid category (non-string)
    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.add_category(123)


def test_get_category_total():
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(50.00, "food", "Groceries")
    tracker.add_expense(20.00, "food", "Snacks")
    tracker.add_expense(100.00, "utilities", "Electricity bill")

    # Test with a valid category that has expenses
    assert tracker.get_category_total("food") == 70.00

    # Test with a valid category that has no expenses
    assert tracker.get_category_total("transport") == 0

    # Test with an invalid category
    with pytest.raises(ValueError, match="Category must be one of: food, transport, utilities, entertainment, other"):
        tracker.get_category_total("invalid_category")


def test_get_expenses_by_category():
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(50.00, "food", "Groceries")
    tracker.add_expense(20.00, "transport", "Uber ride")
    tracker.add_expense(100.00, "utilities", "Electricity bill")
    tracker.add_expense(30.00, "food", "Restaurant dinner")

    # Test with a valid category
    food_expenses = tracker.get_expenses_by_category("food")
    assert len(food_expenses) == 2
    assert food_expenses[0]["amount"] == 50.00
    assert food_expenses[0]["description"] == "Groceries"
    assert food_expenses[1]["amount"] == 30.00
    assert food_expenses[1]["description"] == "Restaurant dinner"

    # Test with an invalid category
    with pytest.raises(ValueError, match="Category must be one of: food, transport, utilities, entertainment, other"):
        tracker.get_expenses_by_category("invalid_category")


def test_record_transaction():
    # Test a successful transaction
    assert record_transaction(100, "food", "groceries") == True

    # Test an invalid category
    with pytest.raises(ValueError, match="Category must be one of: food, transport, utilities, entertainment, other"):
        record_transaction(50, "invalid_category", "some description")


def test_record_transaction_invalid_amount():
    # Test with an invalid amount (negative value)
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        record_transaction(-50, "food", "some description")

    # Test with an invalid amount (non-numeric)
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        record_transaction("invalid_amount", "food", "some description")


@patch('expense_tracker.datetime')
def test_record_transaction_success(mock_datetime):
    # Set up the mock datetime to return a fixed timestamp
    fixed_timestamp = datetime(2023, 6, 1, 12, 0, 0)
    mock_datetime.now.return_value = fixed_timestamp

    # Test a successful transaction
    assert record_transaction(100, "food", "groceries") == True

    # Assert that the transaction was recorded correctly
    with open('transactions.csv', 'r') as file:
        lines = file.readlines()
        last_line = lines[-1].strip()
        expected_line = f"{fixed_timestamp},100,food,groceries"
        assert last_line == expected_line
