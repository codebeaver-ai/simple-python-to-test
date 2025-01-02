import pytest

from expense_tracker import ExpenseTracker

class TestExpenseTracker:
    def test_add_category(self):
        tracker = ExpenseTracker()
        initial_category_count = len(tracker.categories)

        # Test adding a new category
        result = tracker.add_category("groceries")
        assert result == True
        assert len(tracker.categories) == initial_category_count + 1
        assert "groceries" in tracker.categories

        # Test adding an existing category
        result = tracker.add_category("groceries")
        assert result == False
        assert len(tracker.categories) == initial_category_count + 1

        # Test adding an invalid category
        with pytest.raises(ValueError):
            tracker.add_category("")

        with pytest.raises(ValueError):
            tracker.add_category(123)

    # ... existing tests ...

    def test_get_category_total(self):
        tracker = ExpenseTracker()

        # Add some expenses
        tracker.add_expense(50.0, "food", "Grocery shopping")
        tracker.add_expense(30.0, "food", "Restaurant dinner")
        tracker.add_expense(20.0, "transport", "Bus ticket")

        # Test getting total for a specific category
        assert tracker.get_category_total("food") == 80.0
        assert tracker.get_category_total("transport") == 20.0
        assert tracker.get_category_total("utilities") == 0.0  # No expenses in this category

        # Test invalid category
        with pytest.raises(ValueError):
            tracker.get_category_total("invalid_category")

    # ... existing tests ...

    def test_get_expenses_by_category(self):
        tracker = ExpenseTracker()

        # Add some expenses
        tracker.add_expense(50.0, "food", "Grocery shopping")
        tracker.add_expense(30.0, "food", "Restaurant dinner")
        tracker.add_expense(20.0, "transport", "Bus ticket")
        tracker.add_expense(100.0, "utilities", "Electricity bill")

        # Test getting expenses for a category with multiple entries
        food_expenses = tracker.get_expenses_by_category("food")
        assert len(food_expenses) == 2
        assert food_expenses[0]["amount"] == 50.0
        assert food_expenses[0]["description"] == "Grocery shopping"
        assert food_expenses[1]["amount"] == 30.0
        assert food_expenses[1]["description"] == "Restaurant dinner"

        # Test getting expenses for a category with one entry
        transport_expenses = tracker.get_expenses_by_category("transport")
        assert len(transport_expenses) == 1
        assert transport_expenses[0]["amount"] == 20.0
        assert transport_expenses[0]["description"] == "Bus ticket"

        # Test getting expenses for a category with no entries
        entertainment_expenses = tracker.get_expenses_by_category("entertainment")
        assert len(entertainment_expenses) == 0

        # Test invalid category
        with pytest.raises(ValueError):
            tracker.get_expenses_by_category("invalid_category")

    # ... existing tests ...

    def test_get_total_expenses(self):
        tracker = ExpenseTracker()

        # Test when there are no expenses
        assert tracker.get_total_expenses() == 0

        # Add some expenses
        tracker.add_expense(50.0, "food", "Grocery shopping")
        tracker.add_expense(30.0, "transport", "Bus ticket")
        tracker.add_expense(100.0, "utilities", "Electricity bill")
        tracker.add_expense(20.5, "entertainment", "Movie ticket")

        # Calculate expected total
        expected_total = 50.0 + 30.0 + 100.0 + 20.5

        # Test getting total expenses
        assert tracker.get_total_expenses() == expected_total

        # Add one more expense and test again
        tracker.add_expense(15.75, "food", "Snacks")
        assert tracker.get_total_expenses() == expected_total + 15.75

def test_category_case_insensitivity(self):
    tracker = ExpenseTracker()

    # Add expenses with different case for the same category
    tracker.add_expense(50.0, "Food", "Grocery shopping")
    tracker.add_expense(30.0, "food", "Restaurant dinner")
    tracker.add_expense(20.0, "FOOD", "Snacks")

    # Test that all expenses are retrieved regardless of case
    food_expenses = tracker.get_expenses_by_category("FoOd")
    assert len(food_expenses) == 3

    # Test that the total is correct regardless of case
    assert tracker.get_category_total("FoOd") == 100.0

    # Test that adding a new category is case-insensitive
    assert tracker.add_category("NeW_CaTeGoRy") == True
    assert tracker.add_category("new_category") == False

    # Test that the new category can be used with any case
    tracker.add_expense(15.0, "NEW_CATEGORY", "Test expense")
    assert tracker.get_category_total("new_category") == 15.0

    # ... existing tests ...

    def test_remove_expense(self):
        tracker = ExpenseTracker()

        # Add some expenses
        tracker.add_expense(50.0, "food", "Grocery shopping")
        tracker.add_expense(30.0, "transport", "Bus ticket")
        tracker.add_expense(100.0, "utilities", "Electricity bill")

        initial_total = tracker.get_total_expenses()
        assert initial_total == 180.0

        # Remove an expense
        removed_expense = tracker.remove_expense(1)  # Remove the second expense (index 1)

        # Check if the correct expense was removed
        assert removed_expense["amount"] == 30.0
        assert removed_expense["category"] == "transport"
        assert removed_expense["description"] == "Bus ticket"

        # Check if the total expenses were updated correctly
        new_total = tracker.get_total_expenses()
        assert new_total == 150.0

        # Try to remove an expense with an invalid index
        with pytest.raises(IndexError):
            tracker.remove_expense(10)

        # Check that the total hasn't changed after an invalid removal attempt
        assert tracker.get_total_expenses() == 150.0

    # ... existing tests ...

    def test_edit_expense(self):
        tracker = ExpenseTracker()

        # Add an initial expense
        tracker.add_expense(50.0, "food", "Grocery shopping")

        # Edit the expense
        edited = tracker.edit_expense(0, 60.0, "food", "Grocery shopping with extra items")

        # Check if the edit was successful
        assert edited == True

        # Verify the expense was updated correctly
        expenses = tracker.get_expenses_by_category("food")
        assert len(expenses) == 1
        assert expenses[0]["amount"] == 60.0
        assert expenses[0]["description"] == "Grocery shopping with extra items"

        # Try to edit a non-existent expense
        with pytest.raises(IndexError):
            tracker.edit_expense(1, 30.0, "transport", "Bus ticket")

        # Verify total expenses are correct after editing
        assert tracker.get_total_expenses() == 60.0

        # Try to edit with an invalid category
        with pytest.raises(ValueError):
            tracker.edit_expense(0, 70.0, "invalid_category", "Test")

        # Try to edit with an invalid amount
        with pytest.raises(ValueError):
            tracker.edit_expense(0, -10.0, "food", "Test")

    # ... existing tests ...

    def test_floating_point_precision(self):
        tracker = ExpenseTracker()

        # Add expenses with floating point numbers
        tracker.add_expense(10.1, "food", "Snack")
        tracker.add_expense(10.2, "food", "Another snack")
        tracker.add_expense(10.3, "food", "Yet another snack")

        # The sum should be 30.6, but due to floating point precision,
        # it might not be exactly equal
        total = tracker.get_total_expenses()
        assert abs(total - 30.6) < 1e-10  # Check if the difference is very small

        # Check if the category total is also correct
        category_total = tracker.get_category_total("food")
        assert abs(category_total - 30.6) < 1e-10

        # Add another expense with many decimal places
        tracker.add_expense(0.1234567890, "food", "Precise snack")

        # Check if the new total is correct
        new_total = tracker.get_total_expenses()
        assert abs(new_total - 30.7234567890) < 1e-10

        # Verify that get_expenses_by_category returns the correct amounts
        food_expenses = tracker.get_expenses_by_category("food")
        expected_amounts = [10.1, 10.2, 10.3, 0.1234567890]
        for expense, expected_amount in zip(food_expenses, expected_amounts):
            assert abs(expense["amount"] - expected_amount) < 1e-10

    # ... existing tests ...

    def test_large_expense_amounts(self):
        tracker = ExpenseTracker()

        # Add an expense with a very large amount
        large_amount = 1000000000000  # 1 trillion
        tracker.add_expense(large_amount, "other", "Extremely large expense")

        # Verify that the expense was added correctly
        assert tracker.get_total_expenses() == large_amount

        # Add another large expense
        tracker.add_expense(large_amount, "other", "Another large expense")

        # Verify that the total is correct
        assert tracker.get_total_expenses() == 2 * large_amount

        # Check if the category total is correct
        assert tracker.get_category_total("other") == 2 * large_amount

        # Verify that get_expenses_by_category returns the correct expenses
        large_expenses = tracker.get_expenses_by_category("other")
        assert len(large_expenses) == 2
        assert all(expense["amount"] == large_amount for expense in large_expenses)

        # Try to add an expense that's too large for Python's int
        with pytest.raises(OverflowError):
            tracker.add_expense(2**1000, "other", "Impossibly large expense")

def test_add_and_remove_categories(self):
    tracker = ExpenseTracker()
    initial_categories = set(tracker.categories)  # Store initial categories

    # Add new categories
    assert tracker.add_category("savings") == True
    assert tracker.add_category("gifts") == True
    assert "savings" in tracker.categories
    assert "gifts" in tracker.categories

    # Try to add an existing category
    assert tracker.add_category("food") == False

    # Remove categories
    assert tracker.remove_category("savings") == True
    assert "savings" not in tracker.categories
    assert tracker.remove_category("gifts") == True
    assert "gifts" not in tracker.categories

    # Try to remove a non-existent category
    assert tracker.remove_category("non_existent") == False

    # Try to remove a default category
    with pytest.raises(ValueError):
        tracker.remove_category("food")

    # Ensure we're back to the initial set of categories
    assert tracker.categories == initial_categories