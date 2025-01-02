import pytest

from datetime import datetime
from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
        tracker = InvestmentTracker()

        # Test adding a new category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test adding an existing category (should return False)
        assert tracker.register_new_category("savings") == False

        # Test adding a category with spaces and uppercase (should be normalized)
        assert tracker.register_new_category("  New Category  ") == True
        assert "new category" in tracker.categories

    def test_calculate_overall_spending(self):
        tracker = InvestmentTracker()

        # Add transactions across different categories
        tracker.record_transaction(100, "food", "Grocery shopping")
        tracker.record_transaction(50, "transport", "Bus ticket")
        tracker.record_transaction(200, "utilities", "Electricity bill")
        tracker.record_transaction(75, "entertainment", "Movie tickets")

        # Calculate total spending
        total_spending = tracker.calculate_overall_spending()

        # Assert that the total is correct (100 + 50 + 200 + 75 = 425)
        assert total_spending == 425, f"Expected total spending to be 425, but got {total_spending}"

    def test_filter_by_category(self):
        tracker = InvestmentTracker()

        # Add transactions across different categories
        tracker.record_transaction(100, "food", "Grocery shopping")
        tracker.record_transaction(50, "transport", "Bus ticket")
        tracker.record_transaction(200, "food", "Restaurant dinner")
        tracker.record_transaction(75, "entertainment", "Movie tickets")

        # Filter expenses by the 'food' category
        food_expenses = tracker.filter_by_category("food")

        # Assert that the filtered list contains only food expenses
        assert len(food_expenses) == 2, f"Expected 2 food expenses, but got {len(food_expenses)}"
        assert all(expense['category'] == 'food' for expense in food_expenses), "Non-food expenses found in filtered list"

        # Check the amounts of the food expenses
        food_amounts = [expense['amount'] for expense in food_expenses]
        assert 100 in food_amounts and 200 in food_amounts, "Incorrect amounts in food expenses"

        # Test filtering for a category with no expenses
        utilities_expenses = tracker.filter_by_category("utilities")
        assert len(utilities_expenses) == 0, f"Expected 0 utilities expenses, but got {len(utilities_expenses)}"

        # Test filtering with an invalid category (should raise ValueError)
        with pytest.raises(ValueError):
            tracker.filter_by_category("invalid_category")

    def test_compute_category_sum(self):
        tracker = InvestmentTracker()

        # Add transactions across different categories
        tracker.record_transaction(100, "food", "Grocery shopping")
        tracker.record_transaction(50, "transport", "Bus ticket")
        tracker.record_transaction(200, "food", "Restaurant dinner")
        tracker.record_transaction(75, "entertainment", "Movie tickets")
        tracker.record_transaction(30, "food", "Snacks")

        # Compute sum for 'food' category
        food_sum = tracker.compute_category_sum("food")

        # Assert that the sum is correct (100 + 200 + 30 = 330)
        assert food_sum == 330, f"Expected food sum to be 330, but got {food_sum}"

        # Compute sum for 'transport' category
        transport_sum = tracker.compute_category_sum("transport")

        # Assert that the sum is correct (50)
        assert transport_sum == 50, f"Expected transport sum to be 50, but got {transport_sum}"

        # Test computing sum for a category with no expenses
        utilities_sum = tracker.compute_category_sum("utilities")
        assert utilities_sum == 0, f"Expected utilities sum to be 0, but got {utilities_sum}"

        # Test computing sum with an invalid category (should raise ValueError)
        with pytest.raises(ValueError):
            tracker.compute_category_sum("invalid_category")

    def test_record_transaction_invalid_amount(self):
        tracker = InvestmentTracker()

        # Test with zero amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(0, "food", "Invalid transaction")

        # Test with negative amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(-50, "food", "Invalid transaction")

        # Test with non-numeric amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction("not a number", "food", "Invalid transaction")

        # Verify that no transactions were added
        assert len(tracker.expenses) == 0, "Invalid transactions should not be recorded"

    def test_record_transaction_invalid_category(self):
        tracker = InvestmentTracker()

        # Test with an invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(100, "invalid_category", "Invalid transaction")

        # Test with an empty category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(100, "", "Invalid transaction")

        # Test with a category that's not a string
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(100, 123, "Invalid transaction")

        # Verify that no transactions were added
        assert len(tracker.expenses) == 0, "Invalid transactions should not be recorded"

        # Test with a valid category to ensure the method still works correctly
        assert tracker.record_transaction(100, "food", "Valid transaction") == True
        assert len(tracker.expenses) == 1, "Valid transaction should be recorded"

    def test_register_new_category_invalid_input(self):
        tracker = InvestmentTracker()

        # Test with an empty string
        with pytest.raises(ValueError, match="Category must be a non-empty string"):
            tracker.register_new_category("")

        # Test with only whitespace
        with pytest.raises(ValueError, match="Category must be a non-empty string"):
            tracker.register_new_category("   ")

        # Test with a non-string input
        with pytest.raises(ValueError, match="Category must be a non-empty string"):
            tracker.register_new_category(123)

        # Verify that no new categories were added
        original_categories = set(["food", "transport", "utilities", "entertainment", "other"])
        assert tracker.categories == original_categories, "Invalid categories should not be added"

        # Test with a valid category to ensure the method still works correctly
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories, "Valid category should be added"

    def test_category_case_insensitivity(self):
        tracker = InvestmentTracker()

        # Record transactions with different case for the same category
        tracker.record_transaction(100, "Food", "Lowercase food")
        tracker.record_transaction(200, "FOOD", "Uppercase food")
        tracker.record_transaction(300, "FoOd", "Mixed case food")

        # Test filter_by_category with different cases
        food_expenses = tracker.filter_by_category("fOoD")
        assert len(food_expenses) == 3, "Should find all food expenses regardless of case"

        # Test compute_category_sum with different case
        food_sum = tracker.compute_category_sum("FOOd")
        assert food_sum == 600, "Should sum all food expenses regardless of case"

        # Test adding a new category with different case
        assert tracker.register_new_category("New Category") == True
        assert tracker.register_new_category("new category") == False, "Should recognize existing category regardless of case"

        # Verify that the new category is store

def test_empty_category_operations(self):
    tracker = InvestmentTracker()

    # Add transactions to some categories, but not to 'utilities'
    tracker.record_transaction(100, "food", "Grocery shopping")
    tracker.record_transaction(50, "transport", "Bus ticket")
    tracker.record_transaction(75, "entertainment", "Movie tickets")

    # Test filtering for 'utilities' category (should return an empty list)
    utilities_expenses = tracker.filter_by_category("utilities")
    assert len(utilities_expenses) == 0, "Expected empty list for utilities category"

    # Test computing sum for 'utilities' category (should return 0)
    utilities_sum = tracker.compute_category_sum("utilities")
    assert utilities_sum == 0, "Expected sum of 0 for utilities category"

    # Ensure that 'utilities' is still a valid category
    assert "utilities" in tracker.categories, "Utilities should still be a valid category"

    # Test that operations on empty category don't raise exceptions
    try:
        tracker.filter_by_category("utilities")
        tracker.compute_category_sum("utilities")
    except Exception as e:
        pytest.fail(f"Operations on empty category raised an exception: {e}")

def test_floating_point_transactions(self):
    tracker = InvestmentTracker()

    # Record transactions with floating-point amounts
    tracker.record_transaction(10.50, "food", "Sandwich")
    tracker.record_transaction(3.75, "food", "Coffee")
    tracker.record_transaction(25.99, "entertainment", "Movie ticket")

    # Test overall spending calculation
    total_spending = tracker.calculate_overall_spending()
    expected_total = 10.50 + 3.75 + 25.99
    assert abs(total_spending - expected_total) < 0.01, f"Expected total spending to be {expected_total:.2f}, but got {total_spending:.2f}"

    # Test category sum calculation
    food_sum = tracker.compute_category_sum("food")
    expected_food_sum = 10.50 + 3.75
    assert abs(food_sum - expected_food_sum) < 0.01, f"Expected food sum to be {expected_food_sum:.2f}, but got {food_sum:.2f}"

    # Test filtering by category
    food_expenses = tracker.filter_by_category("food")
    assert len(food_expenses) == 2, f"Expected 2 food expenses, but got {len(food_expenses)}"
    food_amounts = [expense['amount'] for expense in food_expenses]
    assert 10.50 in food_amounts and 3.75 in food_amounts, "Incorrect amounts in food expenses"