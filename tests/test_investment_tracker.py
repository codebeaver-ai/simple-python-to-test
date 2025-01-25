import pytest
import unittest

from datetime import datetime
from investment_tracker import InvestmentTracker

class TestInvestmentTracker(unittest.TestCase):
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
        """
        Test the register_new_category method of InvestmentTracker.

        This test covers:
        1. Successfully adding a new category
        2. Failing to add an existing category
        3. Raising ValueError for an invalid category
        """
        tracker = InvestmentTracker()

        # Test successful category addition
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test adding an existing category
        assert tracker.register_new_category("food") == False

        # Test adding an invalid category (empty string)
        with pytest.raises(ValueError):
            tracker.register_new_category("")

    def test_calculate_overall_spending(self):
        """
        Test the calculate_overall_spending method of InvestmentTracker.

        This test covers:
        1. Adding multiple transactions with different amounts and categories
        2. Verifying that the calculate_overall_spending method returns the correct total
        """
        tracker = InvestmentTracker()

        # Add multiple transactions
        tracker.record_transaction(50.75, "food", "Dinner")
        tracker.record_transaction(30.00, "transport", "Bus fare")
        tracker.record_transaction(100.50, "utilities", "Water bill")
        tracker.record_transaction(20.00, "entertainment", "Movie ticket")

        # Calculate the expected total
        expected_total = 50.75 + 30.00 + 100.50 + 20.00

        # Assert that the calculated total matches the expected total
        assert tracker.calculate_overall_spending() == pytest.approx(expected_total)

    def test_filter_by_category(self):
        """
        Test the filter_by_category method of InvestmentTracker.

        This test covers:
        1. Adding multiple transactions with different categories
        2. Filtering expenses by a specific category
        3. Verifying that only expenses from the specified category are returned
        4. Raising ValueError for an invalid category
        """
        tracker = InvestmentTracker()

        # Add multiple transactions
        tracker.record_transaction(50.75, "food", "Dinner")
        tracker.record_transaction(30.00, "transport", "Bus fare")
        tracker.record_transaction(100.50, "food", "Groceries")
        tracker.record_transaction(20.00, "entertainment", "Movie ticket")

        # Filter by 'food' category
        food_expenses = tracker.filter_by_category("food")

        # Check if all returned expenses are in the 'food' category
        assert len(food_expenses) == 2
        for expense in food_expenses:
            assert expense["category"] == "food"

        # Check specific amounts and descriptions
        assert any(expense["amount"] == 50.75 and expense["description"] == "Dinner" for expense in food_expenses)
        assert any(expense["amount"] == 100.50 and expense["description"] == "Groceries" for expense in food_expenses)

        # Test invalid category
        with pytest.raises(ValueError):
            tracker.filter_by_category("invalid_category")

    def test_compute_category_sum(self):
        """
        Test the compute_category_sum method of InvestmentTracker.

        This test covers:
        1. Adding multiple transactions with different categories
        2. Computing the sum of expenses for a specific category
        3. Verifying that the computed sum is correct
        4. Raising ValueError for an invalid category
        """
        tracker = InvestmentTracker()

        # Add multiple transactions
        tracker.record_transaction(50.75, "food", "Dinner")
        tracker.record_transaction(30.00, "transport", "Bus fare")
        tracker.record_transaction(100.50, "food", "Groceries")
        tracker.record_transaction(20.00, "entertainment", "Movie ticket")

        # Compute sum for 'food' category
        food_sum = tracker.compute_category_sum("food")

        # Check if the computed sum is correct
        assert food_sum == pytest.approx(50.75 + 100.50)

        # Test sum for a category with single transaction
        transport_sum = tracker.compute_category_sum("transport")
        assert transport_sum == pytest.approx(30.00)

        # Test sum for a category with no transactions
        utilities_sum = tracker.compute_category_sum("utilities")
        assert utilities_sum == 0

        # Test invalid category
        with pytest.raises(ValueError):
            tracker.compute_category_sum("invalid_category")

    def test_record_transaction_errors(self):
        """
        Test error handling in the record_transaction method of InvestmentTracker.

        This test covers:
        1. Raising ValueError for a non-positive amount
        2. Raising ValueError for an invalid category
        """
        tracker = InvestmentTracker()

        # Test non-positive amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(0, "food", "Invalid amount")

        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(-10, "food", "Negative amount")

        # Test invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(50, "invalid_category", "Invalid category")

    def test_register_new_category_with_whitespace(self):
        """
        Test registering a new category with leading and trailing whitespace.

        This test covers:
        1. Successfully adding a new category with whitespace
        2. Verifying that the category is added without the whitespace
        """
        tracker = InvestmentTracker()

        # Test registering a category with whitespace
        assert tracker.register_new_category("  savings  ") == True

        # Verify that the category is added without whitespace
        assert "savings" in tracker.categories
        assert "  savings  " not in tracker.categories

        # Verify that trying to add the same category (with or without whitespace) returns False
        assert tracker.register_new_category("savings") == False
        assert tracker.register_new_category("  savings  ") == False

    def test_record_transaction_non_numeric_amount(self):
        """
        Test that record_transaction raises a ValueError when given a non-numeric amount.

        This test covers:
        1. Attempting to record a transaction with a string amount
        2. Verifying that a ValueError is raised
        3. Checking the error message
        """
        tracker = InvestmentTracker()

        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction("not a number", "food", "Invalid amount")

    def test_filter_by_category_with_no_transactions(self):
        """
        Test filtering by a category that exists but has no recorded transactions.

        This test covers:
        1. Adding transactions to some categories
        2. Filtering by a category that exists but has no transactions
        3. Verifying that an empty list is returned
        """
        tracker = InvestmentTracker()

        # Add transactions to some categories
        tracker.record_transaction(50.75, "food", "Dinner")
        tracker.record_transaction(30.00, "transport", "Bus fare")

        # Filter by 'utilities' category, which exists but has no transactions
        utilities_expenses = tracker.filter_by_category("utilities")

        # Check if the result is an empty list
        assert utilities_expenses == []