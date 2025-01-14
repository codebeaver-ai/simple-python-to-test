import pytest

from datetime import datetime
from investment_tracker import InvestmentTracker
from math import isclose

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
        tracker = InvestmentTracker()

        # Test registering a new category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test registering an existing category
        assert tracker.register_new_category("savings") == False

        # Test registering with invalid input
        with pytest.raises(ValueError):
            tracker.register_new_category("")

        with pytest.raises(ValueError):
            tracker.register_new_category(123)

    def test_calculate_overall_spending(self):
        tracker = InvestmentTracker()

        # Add some sample expenses
        tracker.record_transaction(50.00, "food", "Dinner")
        tracker.record_transaction(30.00, "transport", "Bus fare")
        tracker.record_transaction(100.00, "utilities", "Internet bill")

        # Calculate the expected total
        expected_total = 50.00 + 30.00 + 100.00

        # Check if the calculated total matches the expected total
        assert tracker.calculate_overall_spending() == expected_total

    def test_filter_by_category(self):
        tracker = InvestmentTracker()

        # Add sample transactions
        tracker.record_transaction(50.00, "food", "Groceries")
        tracker.record_transaction(30.00, "food", "Restaurant")
        tracker.record_transaction(100.00, "utilities", "Electricity")
        tracker.record_transaction(20.00, "food", "Snacks")

        # Filter by 'food' category
        food_expenses = tracker.filter_by_category("food")

        # Check if the correct number of expenses are returned
        assert len(food_expenses) == 3

        # Check if all returned expenses are in the 'food' category
        for expense in food_expenses:
            assert expense["category"] == "food"

        # Check if the amounts and descriptions match the expected values
        expected_food_expenses = [
            {"amount": 50.00, "category": "food", "description": "Groceries"},
            {"amount": 30.00, "category": "food", "description": "Restaurant"},
            {"amount": 20.00, "category": "food", "description": "Snacks"}
        ]
        assert food_expenses == expected_food_expenses

        # Test with a category that has no expenses
        empty_category = tracker.filter_by_category("entertainment")
        assert len(empty_category) == 0

        # Test with an invalid category
        with pytest.raises(ValueError):
            tracker.filter_by_category("invalid_category")

    def test_compute_category_sum(self):
        tracker = InvestmentTracker()

        # Add sample transactions across different categories
        tracker.record_transaction(50.00, "food", "Groceries")
        tracker.record_transaction(30.00, "food", "Restaurant")
        tracker.record_transaction(100.00, "utilities", "Electricity")
        tracker.record_transaction(20.00, "food", "Snacks")
        tracker.record_transaction(40.00, "transport", "Gas")

        # Test the sum for the 'food' category
        assert tracker.compute_category_sum("food") == 100.00

        # Test the sum for the 'utilities' category
        assert tracker.compute_category_sum("utilities") == 100.00

        # Test the sum for the 'transport' category
        assert tracker.compute_category_sum("transport") == 40.00

        # Test the sum for a category with no expenses
        assert tracker.compute_category_sum("entertainment") == 0.00

        # Test with an invalid category
        with pytest.raises(ValueError):
            tracker.compute_category_sum("invalid_category")

    def test_record_transaction_invalid_inputs(self):
        tracker = InvestmentTracker()

        # Test with invalid amount (negative number)
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(-50, "food", "Negative amount")

        # Test with invalid amount (zero)
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(0, "food", "Zero amount")

        # Test with invalid amount (non-numeric)
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction("not a number", "food", "Non-numeric amount")

        # Test with invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(50, "invalid_category", "Invalid category")

        # Verify that no transactions were added
        assert len(tracker.expenses) == 0

    def test_category_case_insensitivity(self):
        tracker = InvestmentTracker()

        # Record transactions with different cases for the same category
        tracker.record_transaction(50.00, "FOOD", "Uppercase category")
        tracker.record_transaction(30.00, "Food", "Capitalized category")
        tracker.record_transaction(20.00, "food", "Lowercase category")

        # Filter by 'food' category
        food_expenses = tracker.filter_by_category("food")

        # Check if all transactions are correctly categorized
        assert len(food_expenses) == 3

        # Check if the total amount for 'food' category is correct
        assert tracker.compute_category_sum("food") == 100.00

        # Ensure that filtering with different cases works
        assert len(tracker.filter_by_category("FOOD")) == 3
        assert len(tracker.filter_by_category("Food")) == 3

        # Check if the descriptions are correct and in the right order
        descriptions = [expense["description"] for expense in food_expenses]
        assert descriptions == ["Uppercase category", "Capitalized category", "Lowercase category"]

    def test_register_new_category_with_whitespace(self):
        tracker = InvestmentTracker()

        # Test registering a new category with leading/trailing whitespace
        assert tracker.register_new_category("  Savings  ") == True
        assert "savings" in tracker.categories  # Should be lowercase and stripped

        # Verify that the category was added only once
        assert len([cat for cat in tracker.categories if "savings" in cat]) == 1

        # Test that adding the same category without whitespace fails
        assert tracker.register_new_category("savings") == False

        # Test that adding the same category with different whitespace fails
        assert tracker.register_new_category(" SAVINGS ") == False

        # Verify that the total number of categories is correct
        original_category_count = 5  # food, transport, utilities, entertainment, other
        assert len(tracker.categories) == original_category_count + 1

    def test_record_transaction_with_new_category(self):
        tracker = InvestmentTracker()

        # Register a new category
        new_category = "investments"
        assert tracker.register_new_category(new_category) == True

        # Attempt to record a transaction with the new category
        amount = 1000.00
        description = "Stock purchase"
        assert tracker.record_transaction(amount, new_category, description) == True

        # Verify that the transaction was recorded correctly
        investments = tracker.filter_by_category(new_category)
        assert len(investments) == 1
        assert investments[0]["amount"] == amount
        assert investments[0]["category"] == new_category.lower()
        assert investments[0]["description"] == description

        # Verify that the category sum is correct
        assert tracker.compute_category_sum(new_category) == amount

        # Attempt to record a transaction with an invalid new category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(500, "invalid_category", "This should fail")

    def test_floating_point_precision(self):
        tracker = InvestmentTracker()

        # Add many small transactions
        for _ in range(1000):
            tracker.record_transaction(0.01, "food", "Penny candy")

        # The total should be exactly 10.00
        expected_total = 10.00
        actual_total = tracker.calculate_overall_spending()

        # Use isclose to compare floating-point numbers with a small tolerance
        assert isclose(actual_total, expected_total, rel_tol=1e-9, abs_tol=1e-9), \
            f"Expected {expected_total}, but got {actual_total}"

        # Verify that adding a larger transaction still maintains precision
        tracker.record_transaction(1000.00, "other", "Large purchase")
        new_expected_total = 1010.00
        new_actual_total = tracker.calculate_overall_spending()

        assert isclose(new_actual_total, new_expected_total, rel_tol=1e-9, abs_tol=1e-9), \
            f"Expected {new_expected_total}, but got {new_actual_total}"

    def test_record_transaction_with_many_decimal_places(self):
        tracker = InvestmentTracker()

        # Attempt to record a transaction with many decimal places
        amount = 10.123456789
        category = "food"
        description = "Precise meal"

        assert tracker.record_transaction(amount, category, description) == True

        # Verify that the transaction was recorded correctly
        expenses = tracker.filter_by_category(category)
        assert len(expenses) == 1
        recorded_expense = expenses[0]

        # Check if the recorded amount is close to the original amount
        assert isclose(recorded_expense["amount"], amount, rel_tol=1e-9, abs_tol=1e-9), \
            f"Expected {amount}, but got {recorded_expense['amount']}"

        assert recorded_expense["category"] == category
        assert recorded_expense["description"] == description

        # Verify that the category sum is correct
        category_sum = tracker.compute_category_sum(category)
        assert isclose(category_sum, amount, rel_tol=1e-9, abs_tol=1e-9), \
            f"Expected category sum {amount}, but got {category_sum}"

        # Verify that the overall spending is correct
        overall_spending = tracker.calculate_overall_spending()
        assert isclose(overall_spending, amount, rel_tol=1e-9, abs_tol=1e-9), \
            f"Expected overall spending {amount}, but got {overall_spending}"