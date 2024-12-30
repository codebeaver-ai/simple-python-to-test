import pytest
from expense_tracker import ExpenseTracker

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