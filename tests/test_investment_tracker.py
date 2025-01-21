import pytest

from datetime import datetime
from investment_tracker import InvestmentTracker

# TODO: add more tests

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
        """
        Test the register_new_category method of InvestmentTracker.

        This test verifies that:
        1. A new category can be successfully added.
        2. Adding an existing category returns False.
        3. The new category is actually added to the categories set.
        """
        tracker = InvestmentTracker()

        # Test adding a new category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test adding an existing category
        assert tracker.register_new_category("food") == False

        # Test adding a new category with mixed case
        assert tracker.register_new_category("Investments") == True
        assert "investments" in tracker.categories

    def test_calculate_overall_spending(self):
        """
        Test the calculate_overall_spending method of InvestmentTracker.

        This test verifies that:
        1. The method correctly calculates the total of all recorded expenses.
        2. The method works with multiple transactions across different categories.
        """
        tracker = InvestmentTracker()

        # Record multiple transactions
        tracker.record_transaction(50.00, "food", "Dinner")
        tracker.record_transaction(30.00, "transport", "Bus fare")
        tracker.record_transaction(100.00, "utilities", "Internet bill")
        tracker.record_transaction(20.50, "entertainment", "Movie ticket")

        # Calculate the expected total
        expected_total = 50.00 + 30.00 + 100.00 + 20.50

        # Verify the calculated total matches the expected total
        assert tracker.calculate_overall_spending() == expected_total

    def test_filter_by_category(self):
        """
        Test the filter_by_category method of InvestmentTracker.

        This test verifies that:
        1. The method correctly filters transactions by category.
        2. The filtered results contain the correct number of transactions.
        3. The filtered transactions have the correct amounts and descriptions.
        """
        tracker = InvestmentTracker()

        # Record multiple transactions in different categories
        tracker.record_transaction(50.00, "food", "Dinner")
        tracker.record_transaction(30.00, "transport", "Bus fare")
        tracker.record_transaction(25.00, "food", "Lunch")
        tracker.record_transaction(100.00, "utilities", "Internet bill")
        tracker.record_transaction(20.50, "food", "Snacks")

        # Filter transactions for the "food" category
        food_transactions = tracker.filter_by_category("food")

        # Verify the number of filtered transactions
        assert len(food_transactions) == 3

        # Verify the amounts and descriptions of the filtered transactions
        expected_transactions = [
            {"amount": 50.00, "category": "food", "description": "Dinner"},
            {"amount": 25.00, "category": "food", "description": "Lunch"},
            {"amount": 20.50, "category": "food", "description": "Snacks"}
        ]

        for expected, actual in zip(expected_transactions, food_transactions):
            assert expected["amount"] == actual["amount"]
            assert expected["category"] == actual["category"]
            assert expected["description"] == actual["description"]

    def test_compute_category_sum(self):
        """
        Test the compute_category_sum method of InvestmentTracker.

        This test verifies that:
        1. The method correctly calculates the sum of expenses for a specific category.
        2. The method works with multiple transactions in the same category.
        3. The method returns the correct sum when there are transactions in other categories.
        """
        tracker = InvestmentTracker()

        # Record multiple transactions in different categories
        tracker.record_transaction(50.00, "food", "Dinner")
        tracker.record_transaction(30.00, "transport", "Bus fare")
        tracker.record_transaction(25.00, "food", "Lunch")
        tracker.record_transaction(100.00, "utilities", "Internet bill")
        tracker.record_transaction(20.50, "food", "Snacks")

        # Compute the sum for the "food" category
        food_sum = tracker.compute_category_sum("food")

        # Verify the computed sum matches the expected total
        expected_food_sum = 50.00 + 25.00 + 20.50
        assert food_sum == expected_food_sum

        # Verify sum for a category with a single transaction
        transport_sum = tracker.compute_category_sum("transport")
        assert transport_sum == 30.00

        # Verify sum for a category with no transactions
        entertainment_sum = tracker.compute_category_sum("entertainment")
        assert entertainment_sum == 0

    def test_record_transaction_validation(self):
        """
        Test the input validation of the record_transaction method.

        This test verifies that:
        1. The method raises a ValueError when given a negative amount.
        2. The method raises a ValueError when given an invalid category.
        """
        tracker = InvestmentTracker()

        # Test invalid amount (negative number)
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(-50, "food", "Invalid expense")

        # Test invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(50, "invalid_category", "Invalid category expense")

    def test_register_new_category_validation(self):
        """
        Test the input validation of the register_new_category method.

        This test verifies that:
        1. The method raises a ValueError when given an empty string.
        2. The method raises a ValueError when given a non-string input.
        """
        tracker = InvestmentTracker()

        # Test empty string input
        with pytest.raises(ValueError, match="Category must be a non-empty string"):
            tracker.register_new_category("")

        # Test whitespace-only string input
        with pytest.raises(ValueError, match="Category must be a non-empty string"):
            tracker.register_new_category("   ")

        # Test non-string input
        with pytest.raises(ValueError, match="Category must be a non-empty string"):
            tracker.register_new_category(123)

    def test_invalid_category_operations(self):
        """
        Test operations with invalid categories.

        This test verifies that:
        1. Attempting to filter by an invalid category raises a ValueError.
        2. Attempting to compute the sum for an invalid category raises a ValueError.
        3. The error messages are correct and informative.
        """
        tracker = InvestmentTracker()

        # Test filtering by invalid category
        with pytest.raises(ValueError) as excinfo:
            tracker.filter_by_category("invalid_category")
        assert "Category must be one of:" in str(excinfo.value)

        # Test computing sum for invalid category
        with pytest.raises(ValueError) as excinfo:
            tracker.compute_category_sum("nonexistent_category")
        assert "Category must be one of:" in str(excinfo.value)

        # Verify that the error message includes all valid categories
        for category in tracker.categories:
            assert category in str(excinfo.value)

    def test_multiple_categories_and_transactions(self):
        """
        Test recording multiple transactions across different categories and verifying totals.

        This test verifies that:
        1. Transactions can be recorded in multiple categories.
        2. The overall spending is calculated correctly across all categories.
        3. Category-specific sums are calculated correctly.
        4. The number of transactions in each category is accurate.
        """
        tracker = InvestmentTracker()

        # Record transactions in multiple categories
        tracker.record_transaction(50.00, "food", "Groceries")
        tracker.record_transaction(30.00, "transport", "Gas")
        tracker.record_transaction(100.00, "utilities", "Electricity")
        tracker.record_transaction(25.50, "food", "Restaurant")
        tracker.record_transaction(15.00, "entertainment", "Movie")
        tracker.record_transaction(40.00, "transport", "Train ticket")

        # Verify overall spending
        assert tracker.calculate_overall_spending() == 260.50

        # Verify category-specific sums
        assert tracker.compute_category_sum("food") == 75.50
        assert tracker.compute_category_sum("transport") == 70.00
        assert tracker.compute_category_sum("utilities") == 100.00
        assert tracker.compute_category_sum("entertainment") == 15.00
        assert tracker.compute_category_sum("other") == 0.00  # Category with no transactions

        # Verify number of transactions in each category
        assert len(tracker.filter_by_category("food")) == 2
        assert len(tracker.filter_by_category("transport")) == 2
        assert len(tracker.filter_by_category("utilities")) == 1
        assert len(tracker.filter_by_category("entertainment")) == 1
        assert len(tracker.filter_by_category("other")) == 0

    def test_multiple_categories_and_transactions(self):
        """
        Test recording multiple transactions across different categories and verifying totals.

        This test verifies that:
        1. Transactions can be recorded in multiple categories.
        2. The overall spending is calculated correctly across all categories.
        3. Category-specific sums are calculated correctly.
        4. The number of transactions in each category is accurate.
        """
        tracker = InvestmentTracker()

        # Record transactions in multiple categories
        tracker.record_transaction(50.00, "food", "Groceries")
        tracker.record_transaction(30.00, "transport", "Gas")
        tracker.record_transaction(100.00, "utilities", "Electricity")
        tracker.record_transaction(25.50, "food", "Restaurant")
        tracker.record_transaction(15.00, "entertainment", "Movie")
        tracker.record_transaction(40.00, "transport", "Train ticket")

        # Verify overall spending
        assert tracker.calculate_overall_spending() == 260.50

        # Verify category-specific sums
        assert tracker.compute_category_sum("food") == 75.50
        assert tracker.compute_category_sum("transport") == 70.00
        assert tracker.compute_category_sum("utilities") == 100.00
        assert tracker.compute_category_sum("entertainment") == 15.00
        assert tracker.compute_category_sum("other") == 0.00  # Category with no transactions

        # Verify number of transactions in each category
        assert len(tracker.filter_by_category("food")) == 2
        assert len(tracker.filter_by_category("transport")) == 2
        assert len(tracker.filter_by_category("utilities")) == 1
        assert len(tracker.filter_by_category("entertainment")) == 1
        assert len(tracker.filter_by_category("other")) == 0