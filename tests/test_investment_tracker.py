import pytest

from datetime import datetime
from investment_tracker import InvestmentTracker

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

    def test_register_new_category_with_spaces(self):
        tracker = InvestmentTracker()

        # Test registering a new category with leading/trailing spaces
        assert tracker.register_new_category("  savings  ") == True
        assert "savings" in tracker.categories

        # Attempt to register the same category again, but with different spacing
        assert tracker.register_new_category("savings  ") == False
        assert tracker.register_new_category("  savings") == False

        # Verify that only one version of the category exists
        assert len([cat for cat in tracker.categories if "savings" in cat]) == 1

        # Verify that the category can be used in other methods
        tracker.record_transaction(100, "  savings  ", "Test savings")
        assert tracker.compute_category_sum("savings") == 100
        assert len(tracker.filter_by_category("savings")) == 1

    def test_record_transaction_with_new_category(self):
        tracker = InvestmentTracker()

        # Register a new category
        assert tracker.register_new_category("investments") == True

        # Record a transaction with the new category
        assert tracker.record_transaction(1000.00, "investments", "Stock purchase") == True

        # Verify that the transaction was recorded correctly
        investments = tracker.filter_by_category("investments")
        assert len(investments) == 1
        assert investments[0]["amount"] == 1000.00
        assert investments[0]["description"] == "Stock purchase"

        # Verify the category sum
        assert tracker.compute_category_sum("investments") == 1000.00

        # Try to record a transaction with an unregistered category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(500.00, "savings", "Unregistered category")

        # Verify that the total spending includes only the valid transaction
        assert tracker.calculate_overall_spending() == 1000.00

    def test_floating_point_precision(self):
        tracker = InvestmentTracker()

        # Record transactions with floating-point amounts
        tracker.record_transaction(10.01, "food", "Snack")
        tracker.record_transaction(10.02, "food", "Another snack")
        tracker.record_transaction(10.03, "food", "Yet another snack")

        # Calculate the expected total (avoiding floating-point arithmetic)
        expected_total = 30.06  # 10.01 + 10.02 + 10.03

        # Check if the calculated total matches the expected total
        assert abs(tracker.calculate_overall_spending() - expected_total) < 1e-8

        # Check category sum
        food_sum = tracker.compute_category_sum("food")
        assert abs(food_sum - expected_total) < 1e-8

        # Filter and check individual transactions
        food_expenses = tracker.filter_by_category("food")
        assert len(food_expenses) == 3
        assert abs(food_expenses[0]["amount"] - 10.01) < 1e-8
        assert abs(food_expenses[1]["amount"] - 10.02) < 1e-8
        assert abs(food_expenses[2]["amount"] - 10.03) < 1e-8

    def test_record_transaction_empty_description(self):
        tracker = InvestmentTracker()

        # Test recording a transaction with an empty description
        assert tracker.record_transaction(50.00, "food", "") == True

        # Verify that the transaction was recorded
        food_expenses = tracker.filter_by_category("food")
        assert len(food_expenses) == 1
        assert food_expenses[0]["amount"] == 50.00
        assert food_expenses[0]["description"] == ""

        # Verify the category sum
        assert tracker.compute_category_sum("food") == 50.00

        # Verify the total spending
        assert tracker.calculate_overall_spending() == 50.00