import pytest

from datetime import datetime
from investment_tracker import InvestmentTracker

# TODO: add more tests

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_calculate_overall_spending(self):
        """
        Test that calculate_overall_spending correctly sums up all expenses.
        """
        tracker = InvestmentTracker()
        tracker.record_transaction(100, "food", "groceries")
        tracker.record_transaction(50, "transport", "gas")
        tracker.record_transaction(200, "utilities", "electricity")

        total_spending = tracker.calculate_overall_spending()
        assert total_spending == 350, f"Expected total spending to be 350, but got {total_spending}"

    def test_register_new_category(self):
        """
        Test that register_new_category correctly adds a new category
        and returns True for a new category, False for an existing one.
        """
        tracker = InvestmentTracker()

        # Test adding a new category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test adding an existing category
        assert tracker.register_new_category("food") == False

        # Test adding an invalid category (empty string)
        with pytest.raises(ValueError):
            tracker.register_new_category("")

        # Test adding an invalid category (non-string)
        with pytest.raises(ValueError):
            tracker.register_new_category(123)

    def test_filter_by_category(self):
        """
        Test that filter_by_category correctly returns expenses for a specific category
        and raises a ValueError for an invalid category.
        """
        tracker = InvestmentTracker()
        tracker.record_transaction(100, "food", "groceries")
        tracker.record_transaction(50, "transport", "gas")
        tracker.record_transaction(200, "food", "restaurant")
        tracker.record_transaction(150, "utilities", "electricity")

        food_expenses = tracker.filter_by_category("food")
        assert len(food_expenses) == 2
        assert all(expense["category"] == "food" for expense in food_expenses)
        assert sum(expense["amount"] for expense in food_expenses) == 300

        with pytest.raises(ValueError):
            tracker.filter_by_category("invalid_category")

    def test_compute_category_sum(self):
        """
        Test that compute_category_sum correctly calculates the total expenses for a specific category
        and raises a ValueError for an invalid category.
        """
        tracker = InvestmentTracker()
        tracker.record_transaction(100, "food", "groceries")
        tracker.record_transaction(50, "transport", "gas")
        tracker.record_transaction(200, "food", "restaurant")
        tracker.record_transaction(150, "utilities", "electricity")

        food_sum = tracker.compute_category_sum("food")
        assert food_sum == 300, f"Expected food sum to be 300, but got {food_sum}"

        transport_sum = tracker.compute_category_sum("transport")
        assert transport_sum == 50, f"Expected transport sum to be 50, but got {transport_sum}"

        with pytest.raises(ValueError):
            tracker.compute_category_sum("invalid_category")

    def test_record_transaction_invalid_inputs(self):
        """
        Test that record_transaction raises ValueError for invalid inputs:
        - Negative or zero amount
        - Invalid category
        """
        tracker = InvestmentTracker()

        # Test negative amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(-50, "food", "groceries")

        # Test zero amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(0, "food", "groceries")

        # Test invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(100, "invalid_category", "description")

    def test_record_transaction_non_numeric_amount(self):
        """
        Test that record_transaction raises ValueError when given a non-numeric amount.
        This covers the case where the amount is neither an int nor a float.
        """
        tracker = InvestmentTracker()

        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction("100", "food", "groceries")  # amount as string

        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction([100], "food", "groceries")  # amount as list

        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction({100}, "food", "groceries")  # amount as set

    def test_filter_by_empty_category(self):
        """
        Test that filter_by_category returns an empty list for a category
        that exists but has no recorded transactions.
        """
        tracker = InvestmentTracker()
        tracker.record_transaction(100, "food", "groceries")
        tracker.record_transaction(50, "transport", "gas")

        # 'utilities' is a valid category but has no transactions
        utilities_expenses = tracker.filter_by_category("utilities")
        assert isinstance(utilities_expenses, list), "Expected a list to be returned"
        assert len(utilities_expenses) == 0, "Expected an empty list for category with no transactions"

    def test_register_new_category_with_whitespace(self):
        """
        Test that register_new_category correctly handles category names with leading/trailing whitespace.
        It should strip the whitespace and add the category successfully.
        """
        tracker = InvestmentTracker()

        # Test adding a new category with leading and trailing whitespace
        assert tracker.register_new_category("  savings  ") == True
        assert "savings" in tracker.categories

        # Verify that the category was added without the whitespace
        assert "  savings  " not in tracker.categories

        # Try to add the same category again (this time without whitespace)
        assert tracker.register_new_category("savings") == False

    def test_record_transaction_case_insensitive_category(self):
        """
        Test that record_transaction handles category names case-insensitively.
        This ensures that categories like 'Food', 'FOOD', and 'food' are treated the same.
        """
        tracker = InvestmentTracker()

        # Record transactions with different cases for the 'food' category
        assert tracker.record_transaction(100, "Food", "Groceries") == True
        assert tracker.record_transaction(50, "FOOD", "Restaurant") == True
        assert tracker.record_transaction(25, "food", "Snacks") == True

        # Check that all transactions are recorded under the same category
        food_expenses = tracker.filter_by_category("food")
        assert len(food_expenses) == 3, f"Expected 3 food expenses, but got {len(food_expenses)}"

        # Verify that the total amount for the 'food' category is correct
        total_food_expenses = tracker.compute_category_sum("food")
        assert total_food_expenses == 175, f"Expected total food expenses to be 175, but got {total_food_expenses}"

        # Check that filtering works with any case
        assert len(tracker.filter_by_category("FOOD")) == 3
        assert len(tracker.filter_by_category("Food")) == 3
        assert len(tracker.filter_by_category("food")) == 3

    def test_floating_point_amounts(self):
        """
        Test that the InvestmentTracker correctly handles floating-point amounts,
        especially when calculating totals and category sums.
        """
        tracker = InvestmentTracker()

        # Record transactions with floating-point amounts
        tracker.record_transaction(10.99, "food", "Lunch")
        tracker.record_transaction(5.50, "food", "Coffee")
        tracker.record_transaction(20.75, "transport", "Taxi")

        # Check overall spending
        total_spending = tracker.calculate_overall_spending()
        expected_total = 37.24  # 10.99 + 5.50 + 20.75
        assert abs(total_spending - expected_total) < 0.01, f"Expected total spending to be close to {expected_total}, but got {total_spending}"

        # Check category sum for food
        food_sum = tracker.compute_category_sum("food")
        expected_food_sum = 16.49  # 10.99 + 5.50
        assert abs(food_sum - expected_food_sum) < 0.01, f"Expected food sum to be close to {expected_food_sum}, but got {food_sum}"

        # Check that filtered expenses have correct amounts
        food_expenses = tracker.filter_by_category("food")
        assert len(food_expenses) == 2
        assert any(abs(expense['amount'] - 10.99) < 0.01 for expense in food_expenses)
        assert any(abs(expense['amount'] - 5.50) < 0.01 for expense in food_expenses)