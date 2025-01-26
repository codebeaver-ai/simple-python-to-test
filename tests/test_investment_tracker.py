import pytest

from datetime import datetime
from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
        """
        Test the register_new_category method:
        - Registering a new category should succeed
        - The new category should be in the categories set
        - Registering the same category again should fail
        """
        tracker = InvestmentTracker()

        # Register a new category
        result = tracker.register_new_category("savings")
        assert result == True
        assert "savings" in tracker.categories

        # Try to register the same category again
        result = tracker.register_new_category("savings")
        assert result == False

    def test_calculate_overall_spending(self):
        """
        Test the calculate_overall_spending method:
        - Add multiple transactions
        - Verify that the overall spending is calculated correctly
        """
        tracker = InvestmentTracker()

        # Add multiple transactions
        tracker.record_transaction(100, "food", "Grocery shopping")
        tracker.record_transaction(50, "transport", "Bus ticket")
        tracker.record_transaction(200, "utilities", "Electricity bill")

        # Calculate overall spending
        total_spending = tracker.calculate_overall_spending()

        # Verify the result
        assert total_spending == 350, f"Expected total spending to be 350, but got {total_spending}"

    def test_filter_by_category(self):
        """
        Test the filter_by_category method:
        - Add multiple transactions with different categories
        - Filter expenses by a specific category
        - Verify that only expenses from the specified category are returned
        """
        tracker = InvestmentTracker()

        # Add transactions with different categories
        tracker.record_transaction(100, "food", "Grocery shopping")
        tracker.record_transaction(50, "transport", "Bus ticket")
        tracker.record_transaction(200, "food", "Restaurant dinner")
        tracker.record_transaction(150, "utilities", "Electricity bill")

        # Filter expenses by the 'food' category
        food_expenses = tracker.filter_by_category("food")

        # Verify the result
        assert len(food_expenses) == 2, f"Expected 2 food expenses, but got {len(food_expenses)}"
        assert all(expense['category'] == 'food' for expense in food_expenses), "All filtered expenses should be in the 'food' category"
        assert sum(expense['amount'] for expense in food_expenses) == 300, "Total amount for food expenses should be 300"

    def test_compute_category_sum(self):
        """
        Test the compute_category_sum method:
        - Add multiple transactions with different categories
        - Calculate the sum for a specific category
        - Verify that the calculated sum is correct
        - Test with a category that has no transactions
        """
        tracker = InvestmentTracker()

        # Add transactions with different categories
        tracker.record_transaction(100, "food", "Grocery shopping")
        tracker.record_transaction(50, "transport", "Bus ticket")
        tracker.record_transaction(200, "food", "Restaurant dinner")
        tracker.record_transaction(150, "utilities", "Electricity bill")

        # Calculate sum for the 'food' category
        food_sum = tracker.compute_category_sum("food")

        # Verify the result
        assert food_sum == 300, f"Expected food expenses sum to be 300, but got {food_sum}"

        # Calculate sum for a category with no transactions
        entertainment_sum = tracker.compute_category_sum("entertainment")

        # Verify the result
        assert entertainment_sum == 0, f"Expected entertainment expenses sum to be 0, but got {entertainment_sum}"

    def test_record_transaction_invalid_category(self):
        """
        Test that attempting to record a transaction with an invalid category raises a ValueError:
        - Create an InvestmentTracker instance
        - Attempt to record a transaction with an invalid category
        - Verify that a ValueError is raised with the correct error message
        """
        tracker = InvestmentTracker()

        with pytest.raises(ValueError) as excinfo:
            tracker.record_transaction(100, "invalid_category", "Test transaction")

        expected_error_message = f"Category must be one of: {', '.join(tracker.categories)}"
        assert str(excinfo.value) == expected_error_message

    def test_record_transaction_invalid_amount(self):
        """
        Test that attempting to record a transaction with an invalid amount (non-positive number) raises a ValueError:
        - Create an InvestmentTracker instance
        - Attempt to record a transaction with a zero amount
        - Verify that a ValueError is raised with the correct error message
        - Attempt to record a transaction with a negative amount
        - Verify that a ValueError is raised with the correct error message
        """
        tracker = InvestmentTracker()

        # Test with zero amount
        with pytest.raises(ValueError) as excinfo:
            tracker.record_transaction(0, "food", "Test transaction")
        assert str(excinfo.value) == "Amount must be a positive number"

        # Test with negative amount
        with pytest.raises(ValueError) as excinfo:
            tracker.record_transaction(-50, "food", "Test transaction")
        assert str(excinfo.value) == "Amount must be a positive number"

    def test_register_new_category_invalid_input(self):
        """
        Test that attempting to register a new category with invalid input raises a ValueError:
        - Create an InvestmentTracker instance
        - Attempt to register a new category with an empty string
        - Verify that a ValueError is raised with the correct error message
        - Attempt to register a new category with a non-string input
        - Verify that a ValueError is raised with the correct error message
        """
        tracker = InvestmentTracker()

        # Test with empty string
        with pytest.raises(ValueError) as excinfo:
            tracker.register_new_category("")
        assert str(excinfo.value) == "Category must be a non-empty string"

        # Test with non-string input
        with pytest.raises(ValueError) as excinfo:
            tracker.register_new_category(123)
        assert str(excinfo.value) == "Category must be a non-empty string"

    def test_filter_by_category_case_insensitive(self):
        """
        Test that the filter_by_category method is case-insensitive:
        - Create an InvestmentTracker instance
        - Add transactions with different cases for the same category
        - Filter expenses using different cases of the category
        - Verify that all expenses for the category are returned regardless of case
        """
        tracker = InvestmentTracker()

        # Add transactions with different cases for the 'food' category
        tracker.record_transaction(100, "Food", "Grocery shopping")
        tracker.record_transaction(50, "food", "Snacks")
        tracker.record_transaction(200, "FOOD", "Restaurant dinner")

        # Filter expenses using different cases
        food_expenses_lower = tracker.filter_by_category("food")
        food_expenses_upper = tracker.filter_by_category("FOOD")
        food_expenses_title = tracker.filter_by_category("Food")

        # Verify that all methods return the same results
        assert len(food_expenses_lower) == 3
        assert len(food_expenses_upper) == 3
        assert len(food_expenses_title) == 3

        # Verify that the total amount is correct
        total_food_expenses = sum(expense['amount'] for expense in food_expenses_lower)
        assert total_food_expenses == 350, f"Expected total food expenses to be 350, but got {total_food_expenses}"

        # Verify that all returned expenses have the 'food' category (case-insensitive)
        for expense in food_expenses_lower + food_expenses_upper + food_expenses_title:
            assert expense['category'].lower() == 'food'

    def test_non_existent_category(self):
        """
        Test that attempting to filter or compute sum for a non-existent category raises a ValueError:
        - Create an InvestmentTracker instance
        - Attempt to filter expenses by a non-existent category
        - Verify that a ValueError is raised with the correct error message
        - Attempt to compute the sum for a non-existent category
        - Verify that a ValueError is raised with the correct error message
        """
        tracker = InvestmentTracker()

        non_existent_category = "non_existent"
        expected_error_message = f"Category must be one of: {', '.join(tracker.categories)}"

        # Test filter_by_category with non-existent category
        with pytest.raises(ValueError) as excinfo:
            tracker.filter_by_category(non_existent_category)
        assert str(excinfo.value) == expected_error_message

        # Test compute_category_sum with non-existent category
        with pytest.raises(ValueError) as excinfo:
            tracker.compute_category_sum(non_existent_category)
        assert str(excinfo.value) == expected_error_message

    def test_register_existing_category_different_case(self):
        """
        Test that attempting to register an existing category with different capitalization:
        - Returns False, indicating the category already exists
        - Does not add a duplicate category to the categories set
        """
        tracker = InvestmentTracker()

        # Register a new category
        result = tracker.register_new_category("Savings")
        assert result == True
        assert "savings" in tracker.categories

        # Try to register the same category with different capitalization
        result = tracker.register_new_category("sAviNgs")
        assert result == False, "Registering an existing category with different case should return False"

        # Check that only one version of the category exists in the set
        assert len([cat for cat in tracker.categories if cat.lower() == 'savings']) == 1
        assert "savings" in tracker.categories
        assert "Savings" not in tracker.categories
        assert "sAviNgs" not in tracker.categories