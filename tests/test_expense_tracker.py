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