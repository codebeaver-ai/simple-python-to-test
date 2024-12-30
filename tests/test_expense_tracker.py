import pytest
from expense_tracker import ExpenseTracker

import sys

def test_add_category():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Get the initial number of categories
    initial_categories_count = len(tracker.categories)

    # Add a new category
    new_category = "groceries"
    result = tracker.add_category(new_category)

    # Assert that the method returned True (successful addition)
    assert result == True

    # Assert that the new category was added to the set
    assert new_category in tracker.categories

    # Assert that the total number of categories increased by 1
    assert len(tracker.categories) == initial_categories_count + 1

    # Try to add the same category again
    result = tracker.add_category(new_category)

    # Assert that the method returned False (category already exists)
    assert result == False

    # Assert that the total number of categories didn't change
    assert len(tracker.categories) == initial_categories_count + 1

def test_get_total_expenses():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Add some expenses
    tracker.add_expense(50.0, "food", "Grocery shopping")
    tracker.add_expense(30.0, "transport", "Bus fare")
    tracker.add_expense(100.0, "utilities", "Electricity bill")

    # Calculate the expected total
    expected_total = 50.0 + 30.0 + 100.0

    # Get the total expenses from the tracker
    actual_total = tracker.get_total_expenses()

    # Assert that the actual total matches the expected total
    assert actual_total == expected_total, f"Expected {expected_total}, but got {actual_total}"

    # Add another expense and check again
    tracker.add_expense(25.5, "entertainment", "Movie ticket")
    expected_total += 25.5
    actual_total = tracker.get_total_expenses()

    # Assert that the new total is correct
    assert actual_total == expected_total, f"Expected {expected_total}, but got {actual_total}"

def test_get_category_total():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Add some expenses in different categories
    tracker.add_expense(50.0, "food", "Grocery shopping")
    tracker.add_expense(30.0, "transport", "Bus fare")
    tracker.add_expense(100.0, "food", "Restaurant dinner")
    tracker.add_expense(25.0, "entertainment", "Movie ticket")

    # Test getting total for a specific category
    food_total = tracker.get_category_total("food")
    expected_food_total = 50.0 + 100.0

    # Assert that the calculated total matches the expected total
    assert food_total == expected_food_total, f"Expected food total {expected_food_total}, but got {food_total}"

    # Test getting total for a category with no expenses
    utilities_total = tracker.get_category_total("utilities")
    assert utilities_total == 0, f"Expected utilities total 0, but got {utilities_total}"

    # Test error case with invalid category
    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.get_category_total("invalid_category")

def test_get_expenses_by_category():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Add some expenses in different categories
    tracker.add_expense(50.0, "food", "Grocery shopping")
    tracker.add_expense(30.0, "transport", "Bus fare")
    tracker.add_expense(100.0, "food", "Restaurant dinner")
    tracker.add_expense(25.0, "entertainment", "Movie ticket")

    # Test getting expenses for a specific category
    food_expenses = tracker.get_expenses_by_category("food")

    # Assert that the correct number of expenses are returned
    assert len(food_expenses) == 2, f"Expected 2 food expenses, but got {len(food_expenses)}"

    # Assert that the returned expenses are correct
    assert food_expenses[0]["amount"] == 50.0 and food_expenses[0]["description"] == "Grocery shopping"
    assert food_expenses[1]["amount"] == 100.0 and food_expenses[1]["description"] == "Restaurant dinner"

    # Test getting expenses for a category with no expenses
    utilities_expenses = tracker.get_expenses_by_category("utilities")
    assert len(utilities_expenses) == 0, f"Expected 0 utilities expenses, but got {len(utilities_expenses)}"

    # Test error case with invalid category
    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.get_expenses_by_category("invalid_category")

def test_add_expense_invalid_amount():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Try to add an expense with a negative amount
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        tracker.add_expense(-50.0, "food", "Invalid expense")

    # Try to add an expense with zero amount
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        tracker.add_expense(0, "food", "Another invalid expense")

    # Try to add an expense with a non-numeric amount
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        tracker.add_expense("not a number", "food", "Yet another invalid expense")

    # Verify that no expenses were added
    assert len(tracker.expenses) == 0

def test_add_expense_invalid_category():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Try to add an expense with an invalid category
    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.add_expense(50.0, "invalid_category", "This should fail")

    # Verify that no expenses were added
    assert len(tracker.expenses) == 0

    # Try to add an expense with a valid category (for comparison)
    result = tracker.add_expense(50.0, "food", "This should succeed")
    assert result == True

    # Verify that one expense was added
    assert len(tracker.expenses) == 1

def test_add_expense_valid_input():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Add a valid expense
    result = tracker.add_expense(50.0, "food", "Grocery shopping")

    # Assert that the method returned True (successful addition)
    assert result == True

    # Assert that the expense was added to the list
    assert len(tracker.expenses) == 1

    # Assert that the added expense has correct values
    added_expense = tracker.expenses[0]
    assert added_expense["amount"] == 50.0
    assert added_expense["category"] == "food"
    assert added_expense["description"] == "Grocery shopping"

    # Add another valid expense with a different category
    result = tracker.add_expense(30.0, "transport", "Bus fare")

    # Assert that the method returned True again
    assert result == True

    # Assert that we now have two expenses
    assert len(tracker.expenses) == 2

    # Assert that the second expense was added correctly
    second_expense = tracker.expenses[1]
    assert second_expense["amount"] == 30.0
    assert second_expense["category"] == "transport"
    assert second_expense["description"] == "Bus fare"

def test_add_category_invalid_input():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Test adding an empty string as a category
    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.add_category("")

    # Test adding a whitespace-only string as a category
    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.add_category("   ")

    # Test adding a non-string value as a category
    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.add_category(123)

    # Verify that no new categories were added
    initial_categories = set(["food", "transport", "utilities", "entertainment", "other"])
    assert tracker.categories == initial_categories

def test_add_expense_case_insensitive_category():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Add an expense with a category name in uppercase
    result = tracker.add_expense(50.0, "FOOD", "Grocery shopping")

    # Assert that the method returned True (successful addition)
    assert result == True

    # Assert that the expense was added to the list
    assert len(tracker.expenses) == 1

    # Assert that the added expense has the correct category (in lowercase)
    added_expense = tracker.expenses[0]
    assert added_expense["category"] == "food"

    # Add another expense with mixed case category
    result = tracker.add_expense(30.0, "EnTeRtAiNmEnT", "Movie ticket")

    # Assert that the method returned True again
    assert result == True

    # Assert that we now have two expenses
    assert len(tracker.expenses) == 2

    # Assert that the second expense was added with the correct lowercase category
    second_expense = tracker.expenses[1]
    assert second_expense["category"] == "entertainment"

    # Verify that get_expenses_by_category works with case-insensitive input
    food_expenses = tracker.get_expenses_by_category("FoOd")
    assert len(food_expenses) == 1
    assert food_expenses[0]["amount"] == 50.0

    entertainment_expenses = tracker.get_expenses_by_category("ENTERTAINMENT")
    assert len(entertainment_expenses) == 1
    assert entertainment_expenses[0]["amount"] == 30.0

def test_add_expense_case_insensitive_category():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Add an expense with a category name in uppercase
    result = tracker.add_expense(50.0, "FOOD", "Grocery shopping")

    # Assert that the method returned True (successful addition)
    assert result == True

    # Assert that the expense was added to the list
    assert len(tracker.expenses) == 1

    # Assert that the added expense has the correct category (in lowercase)
    added_expense = tracker.expenses[0]
    assert added_expense["category"] == "food"

    # Add another expense with mixed case category
    result = tracker.add_expense(30.0, "EnTeRtAiNmEnT", "Movie ticket")

    # Assert that the method returned True again
    assert result == True

    # Assert that we now have two expenses
    assert len(tracker.expenses) == 2

    # Assert that the second expense was added with the correct lowercase category
    second_expense = tracker.expenses[1]
    assert second_expense["category"] == "entertainment"

    # Verify that get_expenses_by_category works with case-insensitive input
    food_expenses = tracker.get_expenses_by_category("FoOd")
    assert len(food_expenses) == 1
    assert food_expenses[0]["amount"] == 50.0

    entertainment_expenses = tracker.get_expenses_by_category("ENTERTAINMENT")
    assert len(entertainment_expenses) == 1
    assert entertainment_expenses[0]["amount"] == 30.0

def test_add_category_valid_input():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Get the initial number of categories
    initial_categories_count = len(tracker.categories)

    # Add a new valid category
    new_category = "savings"
    result = tracker.add_category(new_category)

    # Assert that the method returned True (successful addition)
    assert result == True

    # Assert that the new category was added to the set
    assert new_category in tracker.categories

    # Assert that the total number of categories increased by 1
    assert len(tracker.categories) == initial_categories_count + 1

    # Assert that the new category is stored in lowercase
    assert "savings" in tracker.categories
    assert "SAVINGS" not in tracker.categories

    # Try to add the same category again (should return False)
    result = tracker.add_category(new_category)
    assert result == False

    # Assert that the total number of categories didn't change
    assert len(tracker.categories) == initial_categories_count + 1

def test_add_expense_case_insensitive_category():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Add an expense with a category name in uppercase
    result = tracker.add_expense(50.0, "FOOD", "Grocery shopping")

    # Assert that the method returned True (successful addition)
    assert result == True

    # Assert that the expense was added to the list
    assert len(tracker.expenses) == 1

    # Assert that the added expense has the correct category (in lowercase)
    added_expense = tracker.expenses[0]
    assert added_expense["category"] == "food"

    # Add another expense with mixed case category
    result = tracker.add_expense(30.0, "EnTeRtAiNmEnT", "Movie ticket")

    # Assert that the method returned True again
    assert result == True

    # Assert that we now have two expenses
    assert len(tracker.expenses) == 2

    # Assert that the second expense was added with the correct lowercase category
    second_expense = tracker.expenses[1]
    assert second_expense["category"] == "entertainment"

    # Verify that get_expenses_by_category works with case-insensitive input
    food_expenses = tracker.get_expenses_by_category("FoOd")
    assert len(food_expenses) == 1
    assert food_expenses[0]["amount"] == 50.0

    entertainment_expenses = tracker.get_expenses_by_category("ENTERTAINMENT")
    assert len(entertainment_expenses) == 1
    assert entertainment_expenses[0]["amount"] == 30.0

def test_get_total_expenses_empty():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Get the total expenses when no expenses have been added
    total = tracker.get_total_expenses()

    # Assert that the total is 0
    assert total == 0, f"Expected total to be 0, but got {total}"

    # Add an expense and check again
    tracker.add_expense(50.0, "food", "Grocery shopping")
    new_total = tracker.get_total_expenses()

    # Assert that the new total is correct
    assert new_total == 50.0, f"Expected total to be 50.0, but got {new_total}"

def test_get_total_expenses_multiple_categories():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Add expenses in different categories
    tracker.add_expense(50.0, "food", "Grocery shopping")
    tracker.add_expense(30.0, "transport", "Bus fare")
    tracker.add_expense(100.0, "utilities", "Electricity bill")
    tracker.add_expense(25.5, "entertainment", "Movie ticket")

    # Calculate the expected total
    expected_total = 50.0 + 30.0 + 100.0 + 25.5

    # Get the total expenses from the tracker
    actual_total = tracker.get_total_expenses()

    # Assert that the actual total matches the expected total
    assert actual_total == expected_total, f"Expected {expected_total}, but got {actual_total}"

    # Add another expense and check again
    tracker.add_expense(15.0, "food", "Snacks")
    expected_total += 15.0
    actual_total = tracker.get_total_expenses()

    # Assert that the new total is correct
    assert actual_total == expected_total, f"Expected {expected_total}, but got {actual_total}"

def test_add_category_with_whitespace():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Get the initial number of categories
    initial_categories_count = len(tracker.categories)

    # Add a new category with leading and trailing whitespace
    new_category = "  savings  "
    result = tracker.add_category(new_category)

    # Assert that the method returned True (successful addition)
    assert result == True

    # Assert that the new category was added to the set, stripped of whitespace
    assert "savings" in tracker.categories

    # Assert that the original string with whitespace is not in the set
    assert new_category not in tracker.categories

    # Assert that the total number of categories increased by 1
    assert len(tracker.categories) == initial_categories_count + 1

    # Try to add the same category again (should return False)
    result = tracker.add_category("savings")
    assert result == False

    # Assert that the total number of categories didn't change
    assert len(tracker.categories) == initial_categories_count + 1

def test_get_total_expenses_empty():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Get the total expenses when no expenses have been added
    total = tracker.get_total_expenses()

    # Assert that the total is 0
    assert total == 0, f"Expected total to be 0, but got {total}"

    # Add an expense and check again
    tracker.add_expense(50.0, "food", "Grocery shopping")
    new_total = tracker.get_total_expenses()

    # Assert that the new total is correct
    assert new_total == 50.0, f"Expected total to be 50.0, but got {new_total}"

def test_add_expense_with_float_amount():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Add an expense with a floating-point amount
    result = tracker.add_expense(24.99, "food", "Lunch at restaurant")

    # Assert that the method returned True (successful addition)
    assert result == True

    # Assert that the expense was added to the list
    assert len(tracker.expenses) == 1

    # Assert that the added expense has the correct values
    added_expense = tracker.expenses[0]
    assert added_expense["amount"] == 24.99
    assert added_expense["category"] == "food"
    assert added_expense["description"] == "Lunch at restaurant"

    # Verify that get_total_expenses returns the correct amount
    total = tracker.get_total_expenses()
    assert total == 24.99, f"Expected total to be 24.99, but got {total}"

    # Add another expense with an integer amount
    tracker.add_expense(10, "transport", "Bus fare")

    # Verify that get_total_expenses correctly sums float and int amounts
    new_total = tracker.get_total_expenses()
    expected_total = 24.99 + 10
    assert new_total == expected_total, f"Expected total to be {expected_total}, but got {new_total}"

def test_add_multiple_expenses_same_category():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Add multiple expenses in the same category
    tracker.add_expense(50.0, "food", "Grocery shopping")
    tracker.add_expense(30.0, "food", "Restaurant dinner")
    tracker.add_expense(10.0, "food", "Snacks")

    # Get all food expenses
    food_expenses = tracker.get_expenses_by_category("food")

    # Assert that we have the correct number of food expenses
    assert len(food_expenses) == 3, f"Expected 3 food expenses, but got {len(food_expenses)}"

    # Assert that the total amount for food expenses is correct
    food_total = tracker.get_category_total("food")
    expected_total = 50.0 + 30.0 + 10.0
    assert food_total == expected_total, f"Expected food total {expected_total}, but got {food_total}"

    # Verify that each expense is correctly recorded
    assert food_expenses[0]["amount"] == 50.0 and food_expenses[0]["description"] == "Grocery shopping"
    assert food_expenses[1]["amount"] == 30.0 and food_expenses[1]["description"] == "Restaurant dinner"
    assert food_expenses[2]["amount"] == 10.0 and food_expenses[2]["description"] == "Snacks"

    # Verify that the total expenses match the sum of all food expenses
    total_expenses = tracker.get_total_expenses()
    assert total_expenses == expected_total, f"Expected total expenses {expected_total}, but got {total_expenses}"

def test_add_expense_with_float_amount():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Add an expense with a float amount
    result = tracker.add_expense(24.99, "food", "Lunch")

    # Assert that the expense was added successfully
    assert result == True

    # Verify that the expense was added to the list
    assert len(tracker.expenses) == 1

    # Check that the expense details are correct
    added_expense = tracker.expenses[0]
    assert added_expense["amount"] == 24.99
    assert added_expense["category"] == "food"
    assert added_expense["description"] == "Lunch"

    # Verify that the total expenses are calculated correctly
    total_expenses = tracker.get_total_expenses()
    assert total_expenses == 24.99

    # Add another expense with an integer amount
    tracker.add_expense(10, "transport", "Bus fare")

    # Verify that the total expenses are updated correctly
    new_total_expenses = tracker.get_total_expenses()
    assert new_total_expenses == 34.99  # 24.99 + 10

def test_add_expense_with_large_amount():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()

    # Get the maximum integer value for the system
    max_int = sys.maxsize

    # Try to add an expense with the maximum integer value
    result = tracker.add_expense(max_int, "other", "Very large expense")

    # Assert that the method returned True (successful addition)
    assert result == True

    # Assert that the expense was added to the list
    assert len(tracker.expenses) == 1

    # Assert that the added expense has the correct values
    added_expense = tracker.expenses[0]
    assert added_expense["amount"] == max_int
    assert added_expense["category"] == "other"
    assert added_expense["description"] == "Very large expense"

    # Verify that get_total_expenses returns the correct amount
    total = tracker.get_total_expenses()
    assert total == max_int, f"Expected total to be {max_int}, but got {total}"

    # Try to add another expense
    tracker.add_expense(100, "food", "Regular expense")

    # Verify that get_total_expenses correctly sums the large amount and the regular amount
    new_total = tracker.get_total_expenses()
    expected_total = max_int + 100
    assert new_total == expected_total, f"Expected total to be {expected_total}, but got {new_total}"