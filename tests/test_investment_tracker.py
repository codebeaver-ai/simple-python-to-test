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

        # Filter expenses by the "food" category
        food_expenses = tracker.filter_by_category("food")

        # Check that only food expenses are returned
        assert len(food_expenses) == 2, f"Expected 2 food expenses, but got {len(food_expenses)}"

        # Check that the returned expenses have the correct amounts and descriptions
        assert food_expenses[0]["amount"] == 100 and food_expenses[0]["description"] == "Grocery shopping"
        assert food_expenses[1]["amount"] == 200 and food_expenses[1]["description"] == "Restaurant dinner"

        # Verify that filtering by a different category returns the correct result
        transport_expenses = tracker.filter_by_category("transport")
        assert len(transport_expenses) == 1
        assert transport_expenses[0]["amount"] == 50 and transport_expenses[0]["description"] == "Bus ticket"

    def test_compute_category_sum_and_invalid_category(self):
        tracker = InvestmentTracker()

        # Add transactions across different categories
        tracker.record_transaction(100, "food", "Grocery shopping")
        tracker.record_transaction(50, "food", "Restaurant")
        tracker.record_transaction(200, "utilities", "Electricity bill")
        tracker.record_transaction(75, "entertainment", "Movie tickets")

        # Test compute_category_sum for a valid category
        food_sum = tracker.compute_category_sum("food")
        assert food_sum == 150, f"Expected food sum to be 150, but got {food_sum}"

        # Test compute_category_sum for another valid category
        utilities_sum = tracker.compute_category_sum("utilities")
        assert utilities_sum == 200, f"Expected utilities sum to be 200, but got {utilities_sum}"

        # Test compute_category_sum for invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.compute_category_sum("invalid_category")

        # Test filter_by_category for invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.filter_by_category("invalid_category")

    def test_record_transaction_invalid_amount(self):
        tracker = InvestmentTracker()

        # Test negative amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(-50, "food", "Negative amount")

        # Test non-numeric amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction("not a number", "food", "Non-numeric amount")

        # Test zero amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(0, "food", "Zero amount")

    def test_register_new_category_invalid_input(self):
        tracker = InvestmentTracker()
        original_categories = tracker.categories.copy()

        # Test empty string
        with pytest.raises(ValueError, match="Category must be a non-empty string"):
            tracker.register_new_category("")

        # Test whitespace-only string
        with pytest.raises(ValueError, match="Category must be a non-empty string"):
            tracker.register_new_category("   ")

        # Test non-string input
        with pytest.raises(ValueError, match="Category must be a non-empty string"):
            tracker.register_new_category(123)

        # Verify that categories haven't changed
        assert tracker.categories == original_categories, "Categories should not change after invalid inputs"

    def test_record_transaction_invalid_category(self):
        tracker = InvestmentTracker()

        # Attempt to record a transaction with an invalid category
        with pytest.raises(ValueError) as excinfo:
            tracker.record_transaction(100, "invalid_category", "Test transaction")

        # Check that the error message contains the list of valid categories
        error_message = str(excinfo.value)
        assert "Category must be one of:" in error_message
        for category in tracker.categories:
            assert category in error_message

        # Verify that no transaction was added
        assert len(tracker.expenses) == 0
