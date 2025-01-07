import pytest

from datetime import datetime
from decimal import Decimal
from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
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

    def test_calculate_overall_spending(self):
        tracker = InvestmentTracker()

        # Add multiple transactions
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Gas")
        tracker.record_transaction(200, "utilities", "Electricity bill")
        tracker.record_transaction(75, "entertainment", "Movie tickets")

        # Calculate total spending
        total_spending = tracker.calculate_overall_spending()

        # Assert that the total is correct
        assert total_spending == 425, f"Expected total spending to be 425, but got {total_spending}"

    def test_filter_by_category(self):
        tracker = InvestmentTracker()

        # Add multiple transactions in different categories
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Gas")
        tracker.record_transaction(200, "food", "Restaurant")
        tracker.record_transaction(75, "entertainment", "Movie tickets")

        # Filter expenses by the "food" category
        food_expenses = tracker.filter_by_category("food")

        # Assert that the filtered list contains only food expenses
        assert len(food_expenses) == 2, f"Expected 2 food expenses, but got {len(food_expenses)}"
        assert all(expense['category'] == 'food' for expense in food_expenses), "All filtered expenses should be in the 'food' category"

        # Check the amounts of the food expenses
        food_amounts = [expense['amount'] for expense in food_expenses]
        assert 100 in food_amounts and 200 in food_amounts, "Food expenses should include 100 and 200"

        # Test filtering for a category with no expenses
        utilities_expenses = tracker.filter_by_category("utilities")
        assert len(utilities_expenses) == 0, "Expected no utilities expenses"

        # Test filtering with an invalid category
        with pytest.raises(ValueError):
            tracker.filter_by_category("invalid_category")

    def test_compute_category_sum(self):
        tracker = InvestmentTracker()

        # Add multiple transactions in different categories
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Gas")
        tracker.record_transaction(200, "food", "Restaurant")
        tracker.record_transaction(75, "entertainment", "Movie tickets")
        tracker.record_transaction(30, "food", "Snacks")

        # Compute sum for the "food" category
        food_sum = tracker.compute_category_sum("food")

        # Assert that the sum is correct
        assert food_sum == 330, f"Expected food sum to be 330, but got {food_sum}"

        # Compute sum for a category with no expenses
        utilities_sum = tracker.compute_category_sum("utilities")
        assert utilities_sum == 0, f"Expected utilities sum to be 0, but got {utilities_sum}"

        # Test with an invalid category
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

        # Ensure no transactions were recorded
        assert len(tracker.expenses) == 0, "No transactions should be recorded with invalid amounts"

    def test_record_transaction_invalid_category(self):
        tracker = InvestmentTracker()

        # Test with an invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(100, "invalid_category", "Invalid transaction")

        # Ensure no transaction was recorded
        assert len(tracker.expenses) == 0, "No transaction should be recorded with an invalid category"

        # Test with a valid amount but invalid category type
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(100, 123, "Invalid transaction")

        # Ensure still no transaction was recorded
        assert len(tracker.expenses) == 0, "No transaction should be recorded with an invalid category type"

        # Test with a valid category to ensure the method still works correctly
        assert tracker.record_transaction(100, "food", "Valid transaction") == True
        assert len(tracker.expenses) == 1, "One transaction should be recorded with a valid category"

    def test_category_case_insensitivity(self):
        tracker = InvestmentTracker()

        # Record transactions with different cases for categories
        tracker.record_transaction(100, "FOOD", "Uppercase category")
        tracker.record_transaction(75, "Food", "Capitalized category")
        tracker.record_transaction(50, "food", "Lowercase category")

        # Filter expenses using different cases
        uppercase_filter = tracker.filter_by_category("FOOD")
        capitalized_filter = tracker.filter_by_category("Food")
        lowercase_filter = tracker.filter_by_category("food")

        # Verify that all filters return the same results
        assert len(uppercase_filter) == 3, "Should return all 3 food transactions"
        assert len(capitalized_filter) == 3, "Should return all 3 food transactions"
        assert len(lowercase_filter) == 3, "Should return all 3 food transactions"

        # Verify that the total amount is correct
        total_food_expenses = tracker.compute_category_sum("FoOd")  # Mixed case
        assert total_food_expenses == 225, "Total food expenses should be 225"

        # Verify that filtering works for other categories too
        tracker.record_transaction(30, "TRANSPORT", "Uppercase transport")
        transport_expenses = tracker.filter_by_category("transport")
        assert len(transport_expenses) == 1, "Should return 1 transport transaction"
        assert transport_expenses[0]["amount"] == 30, "Transport amount should be 30"

def test_register_new_category_case_insensitivity(self):
    tracker = InvestmentTracker()

    # Register a new category in lowercase
    assert tracker.register_new_category("savings") == True
    assert "savings" in tracker.categories

    # Try to register the same category with different capitalization
    assert tracker.register_new_category("Savings") == False
    assert tracker.register_new_category("SAVINGS") == False

    # Check that only one version of the category exists
    assert len([cat for cat in tracker.categories if cat.lower() == "savings"]) == 1

    # Verify that the category can still be used for transactions regardless of case
    assert tracker.record_transaction(100, "Savings", "Deposit") == True
    assert tracker.record_transaction(50, "SAVINGS", "Another deposit") == True

    # Check that these transactions are correctly categorized
    savings_transactions = tracker.filter_by_category("savings")
    assert len(savings_transactions) == 2
    assert sum(transaction["amount"] for transaction in savings_transactions) == 150

def test_empty_category_operations(self):
    tracker = InvestmentTracker()

    # Add transactions to some categories, but not all
    tracker.record_transaction(100, "food", "Groceries")
    tracker.record_transaction(50, "transport", "Gas")

    # Try to filter expenses for a category with no transactions
    utilities_expenses = tracker.filter_by_category("utilities")
    assert len(utilities_expenses) == 0, "Expected an empty list for utilities expenses"

    # Try to compute sum for a category with no transactions
    utilities_sum = tracker.compute_category_sum("utilities")
    assert utilities_sum == 0, "Expected zero sum for utilities expenses"

    # Verify that these operations don't raise exceptions
    try:
        tracker.filter_by_category("entertainment")
        tracker.compute_category_sum("entertainment")
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")

    # Verify that the total spending is still correct
    total_spending = tracker.calculate_overall_spending()
    assert total_spending == 150, f"Expected total spending to be 150, but got {total_spending}"

    def test_floating_point_transactions(self):
        tracker = InvestmentTracker()

        # Record transactions with floating-point amounts
        tracker.record_transaction(10.50, "food", "Sandwich")
        tracker.record_transaction(3.75, "food", "Coffee")
        tracker.record_transaction(25.99, "entertainment", "Movie ticket")

        # Test overall spending
        total_spending = tracker.calculate_overall_spending()
        expected_total = Decimal('40.24')  # 10.50 + 3.75 + 25.99
        assert Decimal(str(total_spending)).quantize(Decimal('0.01')) == expected_total, \
            f"Expected total spending to be {expected_total}, but got {total_spending}"

        # Test category sum
        food_sum = tracker.compute_category_sum("food")
        expected_food_sum = Decimal('14.25')  # 10.50 + 3.75
        assert Decimal(str(food_sum)).quantize(Decimal('0.01')) == expected_food_sum, \
            f"Expected food sum to be {expected_food_sum}, but got {food_sum}"

        # Test filtering by category
        food_expenses = tracker.filter_by_category("food")
        assert len(food_expenses) == 2, "Expected 2 food expenses"
        food_amounts = [Decimal(str(expense['amount'])) for expense in food_expenses]
        assert Decimal('10.50') in food_amounts and Decimal('3.75') in food_amounts, \
            "Food expenses should include 10.50 and 3.75"