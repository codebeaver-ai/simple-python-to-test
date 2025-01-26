import pytest

from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    """Test class for InvestmentTracker"""

    def test_record_transaction(self):
        """
        Test that a transaction can be recorded successfully.
        This test creates an InvestmentTracker instance and records a valid transaction.
        """
        tracker = InvestmentTracker()
        result = tracker.record_transaction(100, "food", "Grocery shopping")
        assert result == True
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0]["amount"] == 100
        assert tracker.expenses[0]["category"] == "food"
        assert tracker.expenses[0]["description"] == "Grocery shopping"

    def test_calculate_overall_spending(self):
        """
        Test that the overall spending is calculated correctly.
        This test creates an InvestmentTracker instance, records multiple transactions,
        and verifies that the calculated overall spending is correct.
        """
        tracker = InvestmentTracker()
        tracker.record_transaction(100, "food", "Grocery shopping")
        tracker.record_transaction(50, "transport", "Bus ticket")
        tracker.record_transaction(200, "utilities", "Electricity bill")

        total_spending = tracker.calculate_overall_spending()
        assert total_spending == 350, f"Expected overall spending to be 350, but got {total_spending}"

    def test_filter_by_category(self):
        """
        Test that expenses can be correctly filtered by category.
        This test creates an InvestmentTracker instance, records multiple transactions
        across different categories, and verifies that filtering by a specific category
        returns the correct expenses.
        """
        tracker = InvestmentTracker()
        tracker.record_transaction(100, "food", "Grocery shopping")
        tracker.record_transaction(50, "transport", "Bus ticket")
        tracker.record_transaction(200, "food", "Restaurant dinner")
        tracker.record_transaction(150, "utilities", "Electricity bill")

        food_expenses = tracker.filter_by_category("food")
        assert len(food_expenses) == 2, f"Expected 2 food expenses, but got {len(food_expenses)}"
        assert food_expenses[0]["amount"] == 100
        assert food_expenses[0]["description"] == "Grocery shopping"
        assert food_expenses[1]["amount"] == 200
        assert food_expenses[1]["description"] == "Restaurant dinner"

        transport_expenses = tracker.filter_by_category("transport")
        assert len(transport_expenses) == 1, f"Expected 1 transport expense, but got {len(transport_expenses)}"
        assert transport_expenses[0]["amount"] == 50
        assert transport_expenses[0]["description"] == "Bus ticket"

    def test_compute_category_sum(self):
        """
        Test that the sum of expenses for a specific category is calculated correctly.
        This test creates an InvestmentTracker instance, records multiple transactions
        across different categories, and verifies that the sum for a specific category
        is calculated accurately.
        """
        tracker = InvestmentTracker()
        tracker.record_transaction(100, "food", "Grocery shopping")
        tracker.record_transaction(50, "transport", "Bus ticket")
        tracker.record_transaction(200, "food", "Restaurant dinner")
        tracker.record_transaction(150, "utilities", "Electricity bill")

        food_sum = tracker.compute_category_sum("food")
        assert food_sum == 300, f"Expected food expenses sum to be 300, but got {food_sum}"

        transport_sum = tracker.compute_category_sum("transport")
        assert transport_sum == 50, f"Expected transport expenses sum to be 50, but got {transport_sum}"

        utilities_sum = tracker.compute_category_sum("utilities")
        assert utilities_sum == 150, f"Expected utilities expenses sum to be 150, but got {utilities_sum}"

        # Test for a category with no expenses
        entertainment_sum = tracker.compute_category_sum("entertainment")
        assert entertainment_sum == 0, f"Expected entertainment expenses sum to be 0, but got {entertainment_sum}"

    def test_register_new_category(self):
        """
        Test that new categories can be registered and that invalid or duplicate
        categories are handled correctly.
        This test creates an InvestmentTracker instance, registers a new valid category,
        attempts to register a duplicate category, and tries to register an invalid category.
        """
        tracker = InvestmentTracker()

        # Test registering a new valid category
        result = tracker.register_new_category("savings")
        assert result == True, "Expected True when registering a new category"
        assert "savings" in tracker.categories, "New category should be in the categories set"

        # Test registering a duplicate category
        result = tracker.register_new_category("savings")
        assert result == False, "Expected False when registering a duplicate category"

        # Test registering an invalid category (empty string)
        with pytest.raises(ValueError):
            tracker.register_new_category("")

        # Test registering a category with leading/trailing spaces
        result = tracker.register_new_category("  investments  ")
        assert result == True, "Expected True when registering a new category with spaces"
        assert "investments" in tracker.categories, "New category should be in the categories set without spaces"

    def test_record_transaction_invalid_amount(self):
        """
        Test that an exception is raised when trying to record a transaction with an invalid amount.
        This test creates an InvestmentTracker instance and attempts to record transactions with
        invalid amounts (zero, negative, and non-numeric), verifying that ValueError is raised in each case.
        """
        tracker = InvestmentTracker()

        # Test with zero amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(0, "food", "Invalid transaction")

        # Test with negative amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(-50, "transport", "Invalid transaction")

        # Test with non-numeric amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction("not a number", "utilities", "Invalid transaction")

        # Verify that no transactions were recorded
        assert len(tracker.expenses) == 0, "No transactions should be recorded with invalid amounts"

    def test_filter_by_invalid_category(self):
        """
        Test that attempting to filter expenses by an invalid category raises a ValueError.
        This test creates an InvestmentTracker instance, records a valid transaction,
        and then tries to filter by an invalid category, expecting a ValueError to be raised.
        """
        tracker = InvestmentTracker()
        tracker.record_transaction(100, "food", "Grocery shopping")

        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.filter_by_category("invalid_category")

        # Ensure the valid transaction is still present
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0]["category"] == "food"

    def test_record_transaction_case_insensitive_category(self):
        """
        Test that record_transaction handles case-insensitive category input correctly.
        This test creates an InvestmentTracker instance and records a transaction with
        a category name in mixed case, verifying that it's stored in lowercase.
        """
        tracker = InvestmentTracker()
        result = tracker.record_transaction(75.50, "FoOd", "Dinner at restaurant")

        assert result == True
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0]["amount"] == 75.50
        assert tracker.expenses[0]["category"] == "food"  # Should be stored in lowercase
        assert tracker.expenses[0]["description"] == "Dinner at restaurant"

        # Verify that we can filter by the category regardless of case
        food_expenses = tracker.filter_by_category("FoOd")
        assert len(food_expenses) == 1
        assert food_expenses[0]["amount"] == 75.50

    def test_record_transaction_invalid_category(self):
        """
        Test that attempting to record a transaction with an invalid category raises a ValueError.
        This test creates an InvestmentTracker instance and tries to record a transaction
        with a category that doesn't exist in the predefined categories list.
        """
        tracker = InvestmentTracker()

        # Attempt to record a transaction with an invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(100, "invalid_category", "Invalid transaction")

        # Verify that no transaction was recorded
        assert len(tracker.expenses) == 0, "No transaction should be recorded with an invalid category"

        # Verify that a valid transaction can still be recorded after the failed attempt
        result = tracker.record_transaction(100, "food", "Valid transaction")
        assert result == True
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0]["category"] == "food"
        assert tracker.expenses[0]["description"] == "Valid transaction"

    def test_compute_category_sum_invalid_category(self):
        """
        Test that attempting to compute the sum for an invalid category raises a ValueError.
        This test creates an InvestmentTracker instance and tries to compute the sum
        for a category that doesn't exist in the predefined categories list.
        """
        tracker = InvestmentTracker()

        # Record a valid transaction to ensure the tracker is working
        tracker.record_transaction(100, "food", "Grocery shopping")

        # Attempt to compute sum for an invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.compute_category_sum("invalid_category")

        # Verify that we can still compute sum for a valid category
        food_sum = tracker.compute_category_sum("food")
        assert food_sum == 100, f"Expected food sum to be 100, but got {food_sum}"

    def test_register_new_category_non_string_input(self):
        """
        Test that attempting to register a new category with a non-string input raises a ValueError.
        This test creates an InvestmentTracker instance and tries to register new categories
        with various non-string inputs, expecting a ValueError to be raised in each case.
        """
        tracker = InvestmentTracker()

        # Test with integer input
        with pytest.raises(ValueError, match="Category must be a non-empty string"):
            tracker.register_new_category(123)

        # Test with float input
        with pytest.raises(ValueError, match="Category must be a non-empty string"):
            tracker.register_new_category(45.67)

        # Test with list input
        with pytest.raises(ValueError, match="Category must be a non-empty string"):
            tracker.register_new_category(["invalid", "category"])

        # Test with dictionary input
        with pytest.raises(ValueError, match="Category must be a non-empty string"):
            tracker.register_new_category({"category": "invalid"})

        # Verify that no new categories were added
        original_categories = set(["food", "transport", "utilities", "entertainment", "health", "other"])
        assert tracker.categories == original_categories, "No new categories should be added with invalid inputs"