import pytest
from expense_tracker import ExpenseTracker

from unittest.mock import patch

from io import StringIO

from expense_tracker import ExpenseTracker, main

from investment_tracker import InvestmentTracker

import io
import sys
from investment_tracker import InvestmentTracker, main

def test_add_category():
    tracker = ExpenseTracker()

    # Add a new valid category
    assert tracker.add_category("shopping") == True
    assert "shopping" in tracker.categories

    # Try adding the same category again
    assert tracker.add_category("shopping") == False

    # Try adding an invalid empty string category
    with pytest.raises(ValueError):
        tracker.add_category("")

def test_get_total_expenses():
    tracker = ExpenseTracker()

    tracker.add_expense(10.50, "food", "groceries")
    tracker.add_expense(5.00, "transport", "bus fare") 
    tracker.add_expense(7.99, "entertainment", "movie ticket")

    assert tracker.get_total_expenses() == pytest.approx(23.49)

def test_get_expenses_by_category():
    tracker = ExpenseTracker()

    # Add sample expenses
    tracker.add_expense(10.0, "food", "Grocery shopping")
    tracker.add_expense(5.0, "transport", "Bus fare")
    tracker.add_expense(15.0, "food", "Dinner at restaurant")

    # Test with a valid category
    food_expenses = tracker.get_expenses_by_category("food")
    assert len(food_expenses) == 2
    assert food_expenses[0]["amount"] == 10.0
    assert food_expenses[0]["description"] == "Grocery shopping"
    assert food_expenses[1]["amount"] == 15.0
    assert food_expenses[1]["description"] == "Dinner at restaurant"

    # Test with an invalid category
    with pytest.raises(ValueError):
        tracker.get_expenses_by_category("invalid_category")

def test_get_category_total():
    tracker = ExpenseTracker()

    # Add sample expenses
    tracker.add_expense(10.0, "food", "Grocery shopping")
    tracker.add_expense(5.0, "transport", "Bus fare")
    tracker.add_expense(15.0, "food", "Dinner at restaurant")

    # Test with a valid category
    assert tracker.get_category_total("food") == 25.0

    # Test with a category that has no expenses
    assert tracker.get_category_total("entertainment") == 0.0

    # Test with an invalid category
    with pytest.raises(ValueError):
        tracker.get_category_total("invalid_category")

def test_add_expense_invalid_input():
    tracker = ExpenseTracker()

    # Test with an invalid amount (zero)
    with pytest.raises(ValueError) as excinfo:
        tracker.add_expense(0, "food", "Invalid amount")
    assert str(excinfo.value) == "Amount must be a positive number"

    # Test with an invalid amount (negative)
    with pytest.raises(ValueError) as excinfo:
        tracker.add_expense(-10, "food", "Invalid amount")
    assert str(excinfo.value) == "Amount must be a positive number"

    # Test with an invalid category
    with pytest.raises(ValueError) as excinfo:
        tracker.add_expense(10, "invalid_category", "Invalid category")
    assert str(excinfo.value) == "Category must be one of: food, transport, utilities, entertainment, other"

def test_add_expense_with_new_category():
    tracker = ExpenseTracker()

    # Mock user input for adding a new category
    with patch('builtins.input', side_effect=['shopping', '50.0', 'new shoes']):
        tracker.add_expense(input("Enter category: "), 
                            float(input("Enter amount: ")), 
                            input("Enter description: "))

    # Check that the new category was added
    assert 'shopping' in tracker.categories

    # Check that the expense was added correctly
    shopping_expenses = tracker.get_expenses_by_category('shopping')
    assert len(shopping_expenses) == 1
    assert shopping_expenses[0]['amount'] == 50.0
    assert shopping_expenses[0]['description'] == 'new shoes'

def test_main():
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(25.50, "food", "Lunch at cafe")
    tracker.add_expense(35.00, "transport", "Uber ride")
    tracker.add_expense(150.00, "utilities", "Electricity bill")

    # Patch print to capture output
    with patch('sys.stdout', new=StringIO()) as fake_out:
        main()

    # Get the printed output
    printed_output = fake_out.getvalue()

    # Check that the expected output is in the printed output
    assert "Total expenses: $210.50" in printed_output
    assert "Food expenses:" in printed_output 
    assert "$25.50 - Lunch at cafe" in printed_output

def test_main():
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(25.50, "food", "Lunch at cafe") 
    tracker.add_expense(35.00, "transport", "Uber ride")
    tracker.add_expense(150.00, "utilities", "Electricity bill")

    # Patch print to capture output
    with patch('sys.stdout', new=StringIO()) as fake_out:
        main()

    # Get the printed output
    printed_output = fake_out.getvalue()

    # Check that the expected output is in the printed output
    assert "Total expenses: $210.50" in printed_output
    assert "Food expenses:" in printed_output
    assert "$25.50 - Lunch at cafe" in printed_output

def test_main_with_mocked_input():
    tracker = ExpenseTracker()

    # Mock user input for adding expenses
    with patch('builtins.input', side_effect=['100', 'shopping', 'new shoes', 
                                               '50', 'food', 'groceries',
                                               '75', 'utilities', 'electricity bill']):
        main()

    # Check that the expenses were added correctly
    assert tracker.get_total_expenses() == 225.0

    shopping_expenses = tracker.get_expenses_by_category('shopping')
    assert len(shopping_expenses) == 1
    assert shopping_expenses[0]['amount'] == 100.0
    assert shopping_expenses[0]['description'] == 'new shoes'

    food_expenses = tracker.get_expenses_by_category('food')
    assert len(food_expenses) == 1
    assert food_expenses[0]['amount'] == 50.0
    assert food_expenses[0]['description'] == 'groceries'

    utilities_expenses = tracker.get_expenses_by_category('utilities')
    assert len(utilities_expenses) == 1
    assert utilities_expenses[0]['amount'] == 75.0 
    assert utilities_expenses[0]['description'] == 'electricity bill'

def test_main_with_invalid_input():
    tracker = ExpenseTracker()

    # Test with invalid category input
    with patch('builtins.input', side_effect=['invalid', '50', 'Invalid category']), \
         pytest.raises(ValueError), \
         patch('sys.stdout', new=StringIO()) as fake_out:
        main()

    # Check that the appropriate error message is printed
    printed_output = fake_out.getvalue()
    assert "Category must be one of: food, transport, utilities, entertainment, other" in printed_output

    # Test with invalid amount input  
    with patch('builtins.input', side_effect=['food', 'invalid', 'Invalid amount']), \
         pytest.raises(ValueError), \
         patch('sys.stdout', new=StringIO()) as fake_out:
        main()

    # Check that the appropriate error message is printed
    printed_output = fake_out.getvalue()
    assert "Amount must be a positive number" in printed_output

def test_register_new_category():
    tracker = InvestmentTracker()

    # Add a new valid category
    assert tracker.register_new_category("shopping") == True
    assert "shopping" in tracker.categories

    # Try adding the same category again
    assert tracker.register_new_category("shopping") == False

    # Try adding an invalid empty string category
    with pytest.raises(ValueError):
        tracker.register_new_category("")

def test_compute_category_sum():
    tracker = InvestmentTracker()

    # Add sample expenses
    tracker.record_transaction(10.0, "food", "groceries")
    tracker.record_transaction(25.0, "food", "restaurant")
    tracker.record_transaction(15.0, "transport", "taxi")

    # Test with a valid category
    assert tracker.compute_category_sum("food") == 35.0

    # Test with a category that has no expenses
    assert tracker.compute_category_sum("entertainment") == 0.0

    # Test with an invalid category
    with pytest.raises(ValueError) as excinfo:
        tracker.compute_category_sum("invalid")
    assert str(excinfo.value) == "Category must be one of: food, transport, utilities, entertainment, other"

def test_main_with_mocked_input():
    with patch('builtins.input', side_effect=['100', 'shopping', 'new shoes', 
                                              '50', 'food', 'groceries',
                                              '75', 'utilities', 'electricity bill',
                                              '0', 'food', 'invalid amount',
                                              'entertainment', '-50', 'movies']), \
         patch('sys.stdout.write') as mock_print:

        # Call the main function
        main()

        # Check that the correct output was printed
        mock_print.assert_any_call("Total expenses: $225.00\n")
        mock_print.assert_any_call("\nFood expenses:\n")
        mock_print.assert_any_call("$50.00 - groceries\n")

        # Check that the expected exceptions were raised
        mock_print.assert_any_call("Amount must be a positive number\n")
        mock_print.assert_any_call("Amount must be a positive number\n")

def test_main_with_mocked_input_and_print():
    tracker = InvestmentTracker()

    # Mock user input and print output
    with patch('builtins.input', side_effect=['100', 'shopping', 'new shoes', 
                                              '50', 'food', 'groceries',
                                              '75', 'utilities', 'electricity bill',
                                              '0', 'food', 'invalid amount',
                                              'entertainment', '-50', 'movies']), \
         patch('sys.stdout', new=io.StringIO()) as mock_stdout:

        # Call the main function
        main()

        # Get the printed output
        printed_output = mock_stdout.getvalue()

        # Check that the correct output was printed
        assert "Total expenses: $225.00" in printed_output
        assert "Food expenses:" in printed_output
        assert "$50.00 - groceries" in printed_output

        # Check that the expected exceptions were handled and printed
        assert "Amount must be a positive number" in printed_output
        assert "Amount must be a positive number" in printed_output

def test_record_transaction_invalid_category():
    tracker = InvestmentTracker()

    with pytest.raises(ValueError) as excinfo:
        tracker.record_transaction(100.0, "invalid_category", "Test transaction")

    assert str(excinfo.value) == "Category must be one of: food, transport, utilities, entertainment, other"
    assert len(tracker.expenses) == 0

def test_record_transaction_invalid_amount():
    tracker = InvestmentTracker()

    # Test with an invalid amount (zero)
    with pytest.raises(ValueError) as excinfo:
        tracker.record_transaction(0, "food", "Invalid amount")
    assert str(excinfo.value) == "Amount must be a positive number"
    assert len(tracker.expenses) == 0

    # Test with an invalid amount (negative)
    with pytest.raises(ValueError) as excinfo:
        tracker.record_transaction(-10, "food", "Invalid amount")
    assert str(excinfo.value) == "Amount must be a positive number"
    assert len(tracker.expenses) == 0

def test_main_with_mocked_input_and_exceptions():
    tracker = InvestmentTracker()

    # Mock user input and print output
    with patch('builtins.input', side_effect=['100', 'invalid_category', 'invalid transaction',
                                              '0', 'food', 'zero amount',
                                              '-50', 'transport', 'negative amount',
                                              '75', 'utilities', 'electricity bill']), \
         patch('sys.stdout', new=io.StringIO()) as mock_stdout:

        # Call the main function
        main()

        # Get the printed output
        printed_output = mock_stdout.getvalue()

        # Check that the correct output was printed
        assert "Total expenses: $75.00" in printed_output
        assert "Utilities expenses:" in printed_output
        assert "$75.00 - electricity bill" in printed_output

        # Check that the expected exceptions were handled and printed
        assert "Category must be one of: food, transport, utilities, entertainment, other" in printed_output
        assert "Amount must be a positive number" in printed_output
        assert "Amount must be a positive number" in printed_output

def test_register_new_category_success():
    tracker = InvestmentTracker()

    # Register a new valid category
    assert tracker.register_new_category("shopping") == True
    assert "shopping" in tracker.categories

def test_register_new_category_invalid_empty():
    tracker = InvestmentTracker()

    with pytest.raises(ValueError) as excinfo:
        tracker.register_new_category("")

    assert str(excinfo.value) == "Category must be a non-empty string"

def test_register_existing_category():
    tracker = InvestmentTracker()

    # Register an existing category
    assert tracker.register_new_category("food") == False
    assert "food" in tracker.categories
    assert len(tracker.categories) == 5