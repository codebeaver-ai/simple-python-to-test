import pytest
from unittest.mock import patch
from io import StringIO

from expense_tracker import ExpenseTracker

import expense_tracker

from investment_tracker import InvestmentTracker

import investment_tracker

def test_main_output(monkeypatch):
    import expense_tracker

    # Capture stdout
    fake_stdout = StringIO()
    monkeypatch.setattr('sys.stdout', fake_stdout)

    # Run main() 
    expense_tracker.main()

    # Get printed output
    output = fake_stdout.getvalue()

    # Make assertions on output
    assert "Total expenses: $210.50" in output
    assert "Food expenses:" in output
    assert "$25.50 - Lunch at cafe" in output

def test_add_expense_invalid_category():
    tracker = ExpenseTracker()

    with pytest.raises(ValueError) as exc_info:
        tracker.add_expense(50.0, "invalid_category", "Test expense")

    assert str(exc_info.value) == "Category must be one of: food, transport, utilities, entertainment, other"
    assert len(tracker.expenses) == 0

def test_add_category():
    tracker = ExpenseTracker()

    # Add a new valid category
    assert tracker.add_category("shopping") == True
    assert "shopping" in tracker.categories

    # Try to add an existing category
    assert tracker.add_category("shopping") == False
    assert len(tracker.categories) == 6  # Original 5 + "shopping"

    # Try to add invalid categories
    with pytest.raises(ValueError):
        tracker.add_category("")

    with pytest.raises(ValueError):
        tracker.add_category(42)

def test_get_category_total_invalid_category():
    tracker = ExpenseTracker()

    # Add a sample expense
    tracker.add_expense(50.0, "food", "Groceries")

    # Try to get total for an invalid category
    with pytest.raises(ValueError) as exc_info:
        tracker.get_category_total("invalid_category")

    assert str(exc_info.value) == "Category must be one of: food, transport, utilities, entertainment, other"

def test_get_expenses_by_category_empty():
    tracker = ExpenseTracker()

    # Add expenses in various categories
    tracker.add_expense(10.0, "food", "Groceries")
    tracker.add_expense(20.0, "transport", "Gas")
    tracker.add_expense(30.0, "utilities", "Electricity")

    # Try to get expenses for a category with no expenses
    entertainment_expenses = tracker.get_expenses_by_category("entertainment")

    # Assert that the returned list is empty
    assert len(entertainment_expenses) == 0

def test_get_expenses_by_category_invalid():
    from expense_tracker import ExpenseTracker

    tracker = ExpenseTracker()

    # Add a sample expense
    tracker.add_expense(50.0, "food", "Groceries")

    # Try to get expenses for an invalid category
    with pytest.raises(ValueError) as exc_info:
        tracker.get_expenses_by_category("invalid_category")

    assert str(exc_info.value) == "Category must be one of: food, transport, utilities, entertainment, other"

def test_get_total_expenses_with_no_expenses():
    tracker = ExpenseTracker()

    # Call get_total_expenses() when there are no expenses
    total = tracker.get_total_expenses()

    # Assert that the total is 0
    assert total == 0

def test_multiple_expenses():
    tracker = ExpenseTracker()

    # Add multiple expenses in different categories
    tracker.add_expense(10.0, "food", "Groceries")
    tracker.add_expense(20.0, "transport", "Gas")
    tracker.add_expense(30.0, "utilities", "Electricity")
    tracker.add_expense(15.0, "food", "Lunch")
    tracker.add_expense(25.0, "transport", "Taxi")

    # Check total expenses
    assert tracker.get_total_expenses() == 100.0

    # Check category totals
    assert tracker.get_category_total("food") == 25.0
    assert tracker.get_category_total("transport") == 45.0
    assert tracker.get_category_total("utilities") == 30.0

def test_add_expense_invalid_amount():
    tracker = ExpenseTracker()

    # Try to add an expense with an invalid amount (zero)
    with pytest.raises(ValueError) as exc_info:
        tracker.add_expense(0, "food", "Test expense")
    assert str(exc_info.value) == "Amount must be a positive number"

    # Try to add an expense with an invalid amount (negative)
    with pytest.raises(ValueError) as exc_info:
        tracker.add_expense(-50, "food", "Test expense")
    assert str(exc_info.value) == "Amount must be a positive number"

    # Ensure no expenses were added
    assert len(tracker.expenses) == 0

def test_add_new_category():
    tracker = ExpenseTracker()

    # Add a new valid category
    assert tracker.add_category("shopping") == True
    assert "shopping" in tracker.categories

    # Try to add an existing category
    assert tracker.add_category("shopping") == False
    assert len(tracker.categories) == 6  # Original 5 + "shopping"

def test_record_transaction_invalid_amount():
    tracker = InvestmentTracker()

    with pytest.raises(ValueError) as excinfo:
        tracker.record_transaction("invalid", "food", "Test expense")

    assert str(excinfo.value) == "Amount must be a positive number"
    assert len(tracker.expenses) == 0

def test_register_new_category_empty_string():
    tracker = InvestmentTracker()

    with pytest.raises(ValueError) as excinfo:
        tracker.register_new_category("")

    assert str(excinfo.value) == "Category must be a non-empty string"

def test_main_output():
    # Create a StringIO object to capture the printed output
    with patch('sys.stdout', new=StringIO()) as fake_output:
        # Call the main() function
        investment_tracker.main()

        # Get the printed output from the StringIO object
        printed_output = fake_output.getvalue()

        # Assert the expected output
        assert "Total expenses: $210.50" in printed_output
        assert "Food expenses:" in printed_output
        assert "$25.50 - Lunch at cafe" in printed_output

def test_register_new_category_valid():
    tracker = InvestmentTracker()

    # Register a new valid category
    new_category = "new_category"
    result = tracker.register_new_category(new_category)

    # Assert that the category was added successfully
    assert result == True
    assert new_category in tracker.categories

def test_compute_category_sum():
    tracker = InvestmentTracker()

    # Add sample expenses
    tracker.record_transaction(10.0, "food", "Groceries")
    tracker.record_transaction(20.0, "transport", "Gas") 
    tracker.record_transaction(15.0, "food", "Lunch")

    # Check category sum for a valid category
    assert tracker.compute_category_sum("food") == 25.0

    # Check that an invalid category raises ValueError
    with pytest.raises(ValueError) as exc_info:
        tracker.compute_category_sum("invalid_category")

    assert str(exc_info.value) == "Category must be one of: food, transport, utilities, entertainment, other"

def test_filter_by_category_no_expenses():
    tracker = InvestmentTracker()

    # Add expenses in various categories
    tracker.record_transaction(10.0, "food", "Groceries")
    tracker.record_transaction(20.0, "transport", "Gas")
    tracker.record_transaction(30.0, "utilities", "Electricity")

    # Try to filter expenses for a category with no expenses
    entertainment_expenses = tracker.filter_by_category("entertainment")

    # Assert that the returned list is empty
    assert len(entertainment_expenses) == 0

def test_register_existing_category():
    tracker = InvestmentTracker()

    # Try to register an already existing category
    existing_category = "food"
    result = tracker.register_new_category(existing_category)

    # Assert that the category was not added
    assert result == False
    assert len(tracker.categories) == 5  # Original 5 categories

def test_calculate_overall_spending():
    tracker = InvestmentTracker()

    # Add sample expenses
    tracker.record_transaction(10.0, "food", "Groceries")
    tracker.record_transaction(20.0, "transport", "Gas")
    tracker.record_transaction(15.0, "food", "Lunch")

    # Calculate total expenses
    total_expenses = tracker.calculate_overall_spending()

    # Assert the expected total
    assert total_expenses == 45.0

def test_filter_by_category_valid():
    tracker = InvestmentTracker()

    # Add sample expenses
    tracker.record_transaction(10.0, "food", "Groceries")
    tracker.record_transaction(20.0, "transport", "Gas")
    tracker.record_transaction(15.0, "food", "Lunch")

    # Filter expenses by a valid category
    food_expenses = tracker.filter_by_category("food")

    # Assert that the returned list contains the expected expenses
    assert len(food_expenses) == 2
    assert food_expenses[0]["amount"] == 10.0
    assert food_expenses[0]["category"] == "food"
    assert food_expenses[0]["description"] == "Groceries"
    assert food_expenses[1]["amount"] == 15.0
    assert food_expenses[1]["category"] == "food"
    assert food_expenses[1]["description"] == "Lunch"

def test_record_transaction_valid():
    tracker = InvestmentTracker()

    # Record a valid transaction
    result = tracker.record_transaction(100.0, "food", "Groceries")

    # Assert that the transaction was recorded successfully
    assert result == True
    assert len(tracker.expenses) == 1
    assert tracker.expenses[0]["amount"] == 100.0
    assert tracker.expenses[0]["category"] == "food"
    assert tracker.expenses[0]["description"] == "Groceries"