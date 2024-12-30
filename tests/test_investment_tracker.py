import pytest
from datetime import datetime
from investment_tracker import InvestmentTracker

import math

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
        tracker = InvestmentTracker()

        # Test successful category registration
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test registering an existing category
        assert tracker.register_new_category("food") == False

        # Test registering an invalid category
        with pytest.raises(ValueError):
            tracker.register_new_category("")

        with pytest.raises(ValueError):
            tracker.register_new_category(123)

    def test_compute_category_sum(self):
        tracker = InvestmentTracker()

        # Add some transactions
        tracker.record_transaction(50.00, "food", "Grocery shopping")
        tracker.record_transaction(30.00, "food", "Restaurant dinner")
        tracker.record_transaction(100.00, "transport", "Train ticket")

        # Test compute_category_sum for food category
        assert tracker.compute_category_sum("food") == 80.00

        # Test compute_category_sum for transport category
        assert tracker.compute_category_sum("transport") == 100.00

        # Test compute_category_sum for a category with no transactions
        assert tracker.compute_category_sum("utilities") == 0.00

        # Test compute_category_sum with invalid category
        with pytest.raises(ValueError):
            tracker.compute_category_sum("invalid_category")

    def test_filter_by_category(self):
        tracker = InvestmentTracker()

        # Add some transactions
        tracker.record_transaction(50.00, "food", "Grocery shopping")
        tracker.record_transaction(30.00, "food", "Restaurant dinner")
        tracker.record_transaction(100.00, "transport", "Train ticket")
        tracker.record_transaction(20.00, "entertainment", "Movie ticket")

        # Test filtering by food category
        food_expenses = tracker.filter_by_category("food")
        assert len(food_expenses) == 2
        assert food_expenses[0]["amount"] == 50.00
        assert food_expenses[1]["amount"] == 30.00

        # Test filtering by transport category
        transport_expenses = tracker.filter_by_category("transport")
        assert len(transport_expenses) == 1
        assert transport_expenses[0]["amount"] == 100.00

        # Test filtering by a category with no transactions
        utilities_expenses = tracker.filter_by_category("utilities")
        assert len(utilities_expenses) == 0

        # Test filtering with invalid category
        with pytest.raises(ValueError):
            tracker.filter_by_category("invalid_category")

    # ... (existing test methods)

    def test_calculate_overall_spending(self):
        tracker = InvestmentTracker()

        # Add transactions across different categories
        tracker.record_transaction(50.00, "food", "Grocery shopping")
        tracker.record_transaction(30.00, "transport", "Bus ticket")
        tracker.record_transaction(100.00, "utilities", "Electricity bill")
        tracker.record_transaction(20.00, "entertainment", "Movie ticket")

        # Calculate the expected total
        expected_total = 50.00 + 30.00 + 100.00 + 20.00

        # Test the calculate_overall_spending method
        assert tracker.calculate_overall_spending() == expected_total

        # Add one more transaction and test again
        tracker.record_transaction(15.00, "food", "Snacks")
        assert tracker.calculate_overall_spending() == expected_total + 15.00

    def test_record_transaction_invalid_inputs(self):
        tracker = InvestmentTracker()

        # Test with negative amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(-50, "food", "Invalid transaction")

        # Test with zero amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(0, "food", "Invalid transaction")

        # Test with invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(50, "invalid_category", "Invalid transaction")

    def test_category_case_insensitivity(self):
        tracker = InvestmentTracker()

        # Record transactions with differently cased category names
        tracker.record_transaction(50.00, "Food", "Lunch")
        tracker.record_transaction(30.00, "food", "Dinner")
        tracker.record_transaction(20.00, "FOOD", "Snacks")

        # Verify that all transactions are counted in the same category
        food_expenses = tracker.filter_by_category("food")
        assert len(food_expenses) == 3

        # Verify the total amount for the category
        assert tracker.compute_category_sum("food") == 100.00

        # Verify that querying with different cases returns the same result
        assert len(tracker.filter_by_category("Food")) == 3
        assert len(tracker.filter_by_category("FOOD")) == 3
        assert tracker.compute_category_sum("Food") == 100.00
        assert tracker.compute_category_sum("FOOD") == 100.00

    def test_register_new_category_case_insensitive(self):
        tracker = InvestmentTracker()

        # Register a new category
        assert tracker.register_new_category("Savings") == True
        assert "savings" in tracker.categories

        # Attempt to register the same category with different capitalization
        assert tracker.register_new_category("SAVINGS") == False
        assert tracker.register_new_category("savings") == False

        # Verify that only one version of the category exists
        assert len([cat for cat in tracker.categories if cat.lower() == "savings"]) == 1

        # Verify that the original capitalization is preserved
        assert "Savings" not in tracker.categories
        assert "SAVINGS" not in tracker.categories
        assert "savings" in tracker.categories

    def test_record_transaction_with_many_decimals(self):
        tracker = InvestmentTracker()

        # Test with a float amount having many decimal places
        amount = 50.123456789
        category = "food"
        description = "Precise grocery shopping"

        assert tracker.record_transaction(amount, category, description) == True

        # Verify that the transaction was recorded correctly
        expenses = tracker.filter_by_category(category)
        assert len(expenses) == 1

        recorded_expense = expenses[0]
        assert math.isclose(recorded_expense['amount'], amount, rel_tol=1e-9)
        assert recorded_expense['category'] == category
        assert recorded_expense['description'] == description

        # Verify that the total spending is correct
        total_spending = tracker.calculate_overall_spending()
        assert math.isclose(total_spending, amount, rel_tol=1e-9)

    def test_record_transaction_non_numeric_amount(self):
        tracker = InvestmentTracker()

        # Attempt to record a transaction with a non-numeric amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction("fifty", "food", "Invalid transaction")

        # Verify that no transaction was recorded
        assert tracker.calculate_overall_spending() == 0
        assert len(tracker.filter_by_category("food")) == 0

    def test_record_transaction_empty_description(self):
        tracker = InvestmentTracker()

        # Test with an empty description
        amount = 50.00
        category = "food"
        description = ""

        # The current implementation doesn't explicitly check for empty descriptions,
        # so this should succeed. If the requirements change to disallow empty descriptions,
        # this test would need to be updated accordingly.
        assert tracker.record_transaction(amount, category, description) == True

        # Verify that the transaction was recorded correctly
        expenses = tracker.filter_by_category(category)
        assert len(expenses) == 1

        recorded_expense = expenses[0]
        assert recorded_expense['amount'] == amount
        assert recorded_expense['category'] == category
        assert recorded_expense['description'] == description

        # Verify that the total spending is correct
        total_spending = tracker.calculate_overall_spending()
        assert total_spending == amount