import pytest
from expense_tracker import ExpenseTracker

from investment_tracker import InvestmentTracker

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

def test_get_expenses_by_category():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Add expenses to different categories
    tracker.add_expense(50.00, "food", "Grocery shopping")
    tracker.add_expense(30.00, "food", "Restaurant dinner")
    tracker.add_expense(25.00, "transport", "Bus ticket")
    tracker.add_expense(100.00, "utilities", "Electricity bill")

    # Test get_expenses_by_category for food category
    food_expenses = tracker.get_expenses_by_category("food")
    assert len(food_expenses) == 2
    assert all(expense["category"] == "food" for expense in food_expenses)
    assert sum(expense["amount"] for expense in food_expenses) == pytest.approx(80.00)

    # Test get_expenses_by_category for transport category
    transport_expenses = tracker.get_expenses_by_category("transport")
    assert len(transport_expenses) == 1
    assert transport_expenses[0]["category"] == "transport"
    assert transport_expenses[0]["amount"] == pytest.approx(25.00)

    # Test get_expenses_by_category for a category with no expenses
    entertainment_expenses = tracker.get_expenses_by_category("entertainment")
    assert len(entertainment_expenses) == 0

    # Test get_expenses_by_category with an invalid category
    with pytest.raises(ValueError):
        tracker.get_expenses_by_category("invalid_category")

def test_add_expense():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Test adding a valid expense
    assert tracker.add_expense(50.00, "food", "Grocery shopping") == True
    assert len(tracker.expenses) == 1
    assert tracker.expenses[0] == {"amount": 50.00, "category": "food", "description": "Grocery shopping"}

    # Test adding an expense with an invalid amount (negative)
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        tracker.add_expense(-10.00, "food", "Invalid expense")

    # Test adding an expense with an invalid amount (zero)
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        tracker.add_expense(0, "food", "Invalid expense")

    # Test adding an expense with an invalid category
    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.add_expense(30.00, "invalid_category", "Invalid category expense")

    # Verify that only the valid expense was added
    assert len(tracker.expenses) == 1

def test_expense_tracker_initialization():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Check that the initial expenses list is empty
    assert len(tracker.expenses) == 0

    # Verify that the initial categories set contains the expected default categories
    expected_categories = {"food", "transport", "utilities", "entertainment", "other"}
    assert tracker.categories == expected_categories

def test_add_expense_with_non_numeric_amount():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Test adding an expense with a non-numeric amount (string)
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        tracker.add_expense("50.00", "food", "Invalid amount expense")

    # Verify that no expense was added
    assert len(tracker.expenses) == 0

def test_category_case_insensitivity():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Add expenses with different cases for the same category
    tracker.add_expense(50.00, "Food", "Grocery shopping")
    tracker.add_expense(30.00, "food", "Restaurant dinner")
    tracker.add_expense(20.00, "FOOD", "Snacks")

    # Test get_category_total with different cases
    assert tracker.get_category_total("food") == pytest.approx(100.00)
    assert tracker.get_category_total("Food") == pytest.approx(100.00)
    assert tracker.get_category_total("FOOD") == pytest.approx(100.00)

    # Test get_expenses_by_category with different cases
    food_expenses = tracker.get_expenses_by_category("food")
    assert len(food_expenses) == 3
    assert all(expense["category"] == "food" for expense in food_expenses)

    # Verify that the category is stored in lowercase
    assert all(expense["category"] == "food" for expense in tracker.expenses)

def test_category_case_insensitivity_when_adding_expense():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Add expenses with different cases for the same category
    tracker.add_expense(50.00, "Food", "Grocery shopping")
    tracker.add_expense(30.00, "food", "Restaurant dinner")
    tracker.add_expense(20.00, "FOOD", "Snacks")

    # Test get_category_total to ensure all expenses are counted
    assert tracker.get_category_total("food") == pytest.approx(100.00)

    # Test get_expenses_by_category to ensure all expenses are retrieved
    food_expenses = tracker.get_expenses_by_category("food")
    assert len(food_expenses) == 3

    # Verify that all retrieved expenses have the category "food" (lowercase)
    assert all(expense["category"] == "food" for expense in food_expenses)

    # Verify that the original descriptions are preserved
    descriptions = [expense["description"] for expense in food_expenses]
    assert "Grocery shopping" in descriptions
    assert "Restaurant dinner" in descriptions
    assert "Snacks" in descriptions

def test_add_category_case_insensitivity():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Add categories with different cases
    assert tracker.add_category("NewCategory") == True
    assert tracker.add_category("newcategory") == False
    assert tracker.add_category("NEWCATEGORY") == False

    # Check if the category is stored in lowercase
    assert "newcategory" in tracker.categories
    assert "NewCategory" not in tracker.categories
    assert "NEWCATEGORY" not in tracker.categories

    # Verify that only one version of the category was added
    assert len([cat for cat in tracker.categories if cat.lower() == "newcategory"]) == 1

    # Try to add expenses with different cases of the new category
    tracker.add_expense(10.00, "NewCategory", "Expense 1")
    tracker.add_expense(20.00, "newcategory", "Expense 2")
    tracker.add_expense(30.00, "NEWCATEGORY", "Expense 3")

    # Verify that all expenses are categorized correctly
    new_category_expenses = tracker.get_expenses_by_category("newcategory")
    assert len(new_category_expenses) == 3
    assert sum(expense["amount"] for expense in new_category_expenses) == 60.00

def test_register_new_category():
    # Create an instance of InvestmentTracker
    tracker = InvestmentTracker()

    # Test registering a new valid category
    assert tracker.register_new_category("savings") == True
    assert "savings" in tracker.categories

    # Test registering an existing category (should return False)
    assert tracker.register_new_category("savings") == False

    # Test registering a category with leading/trailing spaces
    assert tracker.register_new_category("  investments  ") == True
    assert "investments" in tracker.categories

    # Test registering an invalid category (empty string)
    with pytest.raises(ValueError):
        tracker.register_new_category("")

    # Test registering an invalid category (non-string)
    with pytest.raises(ValueError):
        tracker.register_new_category(123)

    # Verify that the new categories are added in lowercase
    assert "savings" in tracker.categories
    assert "investments" in tracker.categories
    assert "SAVINGS" not in tracker.categories
    assert "INVESTMENTS" not in tracker.categories

def test_calculate_overall_spending():
    # Create an instance of InvestmentTracker
    tracker = InvestmentTracker()

    # Test when no expenses have been added
    assert tracker.calculate_overall_spending() == 0

    # Add some expenses
    tracker.record_transaction(50.00, "food", "Grocery shopping")
    tracker.record_transaction(30.00, "transport", "Bus ticket")
    tracker.record_transaction(100.00, "utilities", "Electricity bill")

    # Calculate the expected total
    expected_total = 50.00 + 30.00 + 100.00

    # Get the total expenses from the tracker
    actual_total = tracker.calculate_overall_spending()

    # Assert that the actual total matches the expected total
    assert actual_total == pytest.approx(expected_total, rel=1e-9)

    # Add another expense
    tracker.record_transaction(25.50, "food", "Restaurant dinner")

    # Recalculate the expected total
    expected_total += 25.50

    # Get the updated total expenses from the tracker
    actual_total = tracker.calculate_overall_spending()

    # Assert that the actual total matches the new expected total
    assert actual_total == pytest.approx(expected_total, rel=1e-9)

def test_filter_by_category():
    # Create an instance of InvestmentTracker
    tracker = InvestmentTracker()

    # Add some sample expenses
    tracker.record_transaction(50.00, "food", "Grocery shopping")
    tracker.record_transaction(30.00, "transport", "Bus ticket")
    tracker.record_transaction(100.00, "food", "Restaurant dinner")
    tracker.record_transaction(75.00, "utilities", "Electricity bill")

    # Test filtering by a valid category
    food_expenses = tracker.filter_by_category("food")
    assert len(food_expenses) == 2
    assert all(expense["category"] == "food" for expense in food_expenses)
    assert sum(expense["amount"] for expense in food_expenses) == pytest.approx(150.00)

    # Test filtering by another valid category
    transport_expenses = tracker.filter_by_category("transport")
    assert len(transport_expenses) == 1
    assert transport_expenses[0]["category"] == "transport"
    assert transport_expenses[0]["amount"] == pytest.approx(30.00)

    # Test filtering by a category with no expenses
    entertainment_expenses = tracker.filter_by_category("entertainment")
    assert len(entertainment_expenses) == 0

    # Test filtering by an invalid category
    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.filter_by_category("invalid_category")

    # Test case insensitivity
    food_expenses_upper = tracker.filter_by_category("FOOD")
    assert len(food_expenses_upper) == 2
    assert all(expense["category"] == "food" for expense in food_expenses_upper)

def test_compute_category_sum():
    # Create an instance of InvestmentTracker
    tracker = InvestmentTracker()

    # Add some sample expenses
    tracker.record_transaction(50.00, "food", "Grocery shopping")
    tracker.record_transaction(30.00, "transport", "Bus ticket")
    tracker.record_transaction(100.00, "food", "Restaurant dinner")
    tracker.record_transaction(75.00, "utilities", "Electricity bill")

    # Test computing sum for a category with multiple expenses
    assert tracker.compute_category_sum("food") == pytest.approx(150.00)

    # Test computing sum for a category with a single expense
    assert tracker.compute_category_sum("transport") == pytest.approx(30.00)

    # Test computing sum for a category with no expenses
    assert tracker.compute_category_sum("entertainment") == pytest.approx(0.00)

    # Test computing sum for an invalid category
    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.compute_category_sum("invalid_category")

    # Test case insensitivity
    assert tracker.compute_category_sum("FOOD") == pytest.approx(150.00)

def test_record_transaction():
    # Create an instance of InvestmentTracker
    tracker = InvestmentTracker()

    # Test recording a valid transaction
    assert tracker.record_transaction(50.00, "food", "Grocery shopping") == True
    assert len(tracker.expenses) == 1
    assert tracker.expenses[0] == {"amount": 50.00, "category": "food", "description": "Grocery shopping"}

    # Test recording a transaction with an invalid amount (negative)
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        tracker.record_transaction(-10.00, "food", "Invalid expense")

    # Test recording a transaction with an invalid amount (zero)
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        tracker.record_transaction(0, "food", "Invalid expense")

    # Test recording a transaction with an invalid category
    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.record_transaction(30.00, "invalid_category", "Invalid category expense")

    # Test recording a transaction with a non-numeric amount
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        tracker.record_transaction("50.00", "food", "Invalid amount expense")

    # Test case insensitivity for category
    assert tracker.record_transaction(25.00, "FOOD", "Case insensitive test") == True
    assert len(tracker.expenses) == 2
    assert tracker.expenses[1]["category"] == "food"

    # Verify that only the valid expenses were added
    assert len(tracker.expenses) == 2
    assert tracker.calculate_overall_spending() == pytest.approx(75.00)

def test_register_new_category_edge_cases():
    tracker = InvestmentTracker()

    # Test adding a new category with mixed case and spaces
    assert tracker.register_new_category("  New Category  ") == True
    assert "new category" in tracker.categories

    # Test that the category is stored in lowercase and stripped
    assert "New Category" not in tracker.categories
    assert "  New Category  " not in tracker.categories

    # Test adding the same category (case-insensitive) returns False
    assert tracker.register_new_category("NEW CATEGORY") == False

    # Test adding an empty category name
    with pytest.raises(ValueError):
        tracker.register_new_category("")

    # Test adding a category with only spaces
    with pytest.raises(ValueError):
        tracker.register_new_category("   ")

def test_record_transaction_case_insensitivity():
    # Create an instance of InvestmentTracker
    tracker = InvestmentTracker()

    # Record transactions with different cases for the same category
    tracker.record_transaction(50.00, "Food", "Grocery shopping")
    tracker.record_transaction(30.00, "food", "Restaurant dinner")
    tracker.record_transaction(20.00, "FOOD", "Snacks")

    # Verify that all transactions are recorded
    assert tracker.calculate_overall_spending() == pytest.approx(100.00)

    # Verify that all transactions are categorized correctly regardless of case
    food_expenses = tracker.filter_by_category("food")
    assert len(food_expenses) == 3

    # Check that all expenses are retrieved with lowercase category
    assert all(expense["category"] == "food" for expense in food_expenses)

    # Verify the amounts and descriptions are correct
    amounts = [expense["amount"] for expense in food_expenses]
    descriptions = [expense["description"] for expense in food_expenses]

    assert 50.00 in amounts
    assert 30.00 in amounts
    assert 20.00 in amounts
    assert "Grocery shopping" in descriptions
    assert "Restaurant dinner" in descriptions
    assert "Snacks" in descriptions

    # Verify that computing category sum works with different cases
    assert tracker.compute_category_sum("Food") == pytest.approx(100.00)
    assert tracker.compute_category_sum("food") == pytest.approx(100.00)
    assert tracker.compute_category_sum("FOOD") == pytest.approx(100.00)

def test_record_transaction_with_float_amount():
    # Create an instance of InvestmentTracker
    tracker = InvestmentTracker()

    # Record a transaction with a float amount
    assert tracker.record_transaction(25.75, "food", "Lunch at cafe") == True

    # Verify that the transaction was recorded correctly
    assert len(tracker.expenses) == 1
    recorded_expense = tracker.expenses[0]
    assert recorded_expense["amount"] == pytest.approx(25.75)
    assert recorded_expense["category"] == "food"
    assert recorded_expense["description"] == "Lunch at cafe"

    # Verify that the overall spending is correct
    assert tracker.calculate_overall_spending() == pytest.approx(25.75)

    # Verify that the category sum is correct
    assert tracker.compute_category_sum("food") == pytest.approx(25.75)

    # Try to record another transaction with a different float amount
    assert tracker.record_transaction(10.99, "entertainment", "Movie ticket") == True

    # Verify that both transactions are recorded
    assert len(tracker.expenses) == 2
    assert tracker.calculate_overall_spending() == pytest.approx(25.75 + 10.99)

    # Verify that filtering by category works correctly
    food_expenses = tracker.filter_by_category("food")
    assert len(food_expenses) == 1
    assert food_expenses[0]["amount"] == pytest.approx(25.75)

    entertainment_expenses = tracker.filter_by_category("entertainment")
    assert len(entertainment_expenses) == 1
    assert entertainment_expenses[0]["amount"] == pytest.approx(10.99)

def test_calculate_overall_spending_with_multiple_transactions():
    # Create an instance of InvestmentTracker
    tracker = InvestmentTracker()

    # Record multiple transactions
    tracker.record_transaction(50.75, "food", "Grocery shopping")
    tracker.record_transaction(30.50, "transport", "Bus ticket")
    tracker.record_transaction(100.25, "utilities", "Electricity bill")
    tracker.record_transaction(25.00, "entertainment", "Movie ticket")

    # Calculate the expected total
    expected_total = 50.75 + 30.50 + 100.25 + 25.00

    # Get the total expenses from the tracker
    actual_total = tracker.calculate_overall_spending()

    # Assert that the actual total matches the expected total
    assert actual_total == pytest.approx(expected_total, rel=1e-9)

    # Add another transaction
    tracker.record_transaction(15.75, "food", "Lunch")

    # Update the expected total
    expected_total += 15.75

    # Get the updated total expenses from the tracker
    updated_actual_total = tracker.calculate_overall_spending()

    # Assert that the updated actual total matches the new expected total
    assert updated_actual_total == pytest.approx(expected_total, rel=1e-9)

def test_investment_tracker_initialization():
    # Create an instance of InvestmentTracker
    tracker = InvestmentTracker()

    # Check that the initial expenses list is empty
    assert len(tracker.expenses) == 0

    # Verify that the initial categories set contains the expected default categories
    expected_categories = {"food", "transport", "utilities", "entertainment", "other"}
    assert tracker.categories == expected_categories

    # Verify that the categories are stored in lowercase
    assert all(category.islower() for category in tracker.categories)

    # Check that the total number of default categories is correct
    assert len(tracker.categories) == 5

    # Verify that adding a new expense doesn't affect the categories
    tracker.record_transaction(50.00, "food", "Grocery shopping")
    assert tracker.categories == expected_categories

    # Verify that the expenses list now contains one item
    assert len(tracker.expenses) == 1

    # Check the contents of the added expense
    added_expense = tracker.expenses[0]
    assert added_expense["amount"] == 50.00
    assert added_expense["category"] == "food"
    assert added_expense["description"] == "Grocery shopping"