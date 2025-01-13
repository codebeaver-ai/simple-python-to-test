import pytest

from datetime import datetime
from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_calculate_overall_spending(self):
        tracker = InvestmentTracker()
        tracker.record_transaction(50.00, "food", "Dinner")
        tracker.record_transaction(30.00, "transport", "Bus ticket")
        tracker.record_transaction(100.00, "utilities", "Internet bill")

        total_spending = tracker.calculate_overall_spending()

        assert total_spending == 180.00, f"Expected total spending to be 180.00, but got {total_spending}"

    def test_register_new_category(self):
        tracker = InvestmentTracker()

        # Test registering a new category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test registering an existing category
        assert tracker.register_new_category("savings") == False

        # Test registering an invalid category
        with pytest.raises(ValueError):
            tracker.register_new_category("")

    def test_filter_by_category(self):
        tracker = InvestmentTracker()

        # Add transactions across different categories
        tracker.record_transaction(50.00, "food", "Dinner")
        tracker.record_transaction(30.00, "transport", "Bus ticket")
        tracker.record_transaction(100.00, "utilities", "Internet bill")
        tracker.record_transaction(25.00, "food", "Lunch")

        # Filter expenses by the "food" category
        food_expenses = tracker.filter_by_category("food")

        # Assert that all returned expenses are in the "food" category
        assert all(expense["category"] == "food" for expense in food_expenses), "Not all expenses are in the 'food' category"

        # Assert that the correct number of expenses are returned
        assert len(food_expenses) == 2, f"Expected 2 food expenses, but got {len(food_expenses)}"

        # Assert that the amounts are correct
        food_amounts = [expense["amount"] for expense in food_expenses]
        assert sorted(food_amounts) == [25.00, 50.00], f"Expected food amounts [25.00, 50.00], but got {sorted(food_amounts)}"

    def test_compute_category_sum(self):
        tracker = InvestmentTracker()

        # Add transactions across different categories
        tracker.record_transaction(50.00, "food", "Dinner")
        tracker.record_transaction(30.00, "transport", "Bus ticket")
        tracker.record_transaction(100.00, "utilities", "Internet bill")
        tracker.record_transaction(25.00, "food", "Lunch")
        tracker.record_transaction(15.00, "food", "Snacks")

        # Test sum for 'food' category
        food_sum = tracker.compute_category_sum("food")
        assert food_sum == 90.00, f"Expected food sum to be 90.00, but got {food_sum}"

        # Test sum for 'transport' category
        transport_sum = tracker.compute_category_sum("transport")
        assert transport_sum == 30.00, f"Expected transport sum to be 30.00, but got {transport_sum}"

        # Test sum for a category with no transactions
        entertainment_sum = tracker.compute_category_sum("entertainment")
        assert entertainment_sum == 0.00, f"Expected entertainment sum to be 0.00, but got {entertainment_sum}"

        # Test with invalid category
        with pytest.raises(ValueError):
            tracker.compute_category_sum("invalid_category")

    def test_record_transaction_invalid_inputs(self):
        tracker = InvestmentTracker()

        # Test with negative amount
        with pytest.raises(ValueError, match="Amount must be a positive number"):
            tracker.record_transaction(-50, "food", "Invalid transaction")

        # Test with invalid category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.record_transaction(50, "invalid_category", "Invalid category")

    def test_filter_by_nonexistent_category(self):
        tracker = InvestmentTracker()

        # Add a sample transaction
        tracker.record_transaction(50.00, "food", "Dinner")

        # Attempt to filter by a non-existent category
        with pytest.raises(ValueError, match="Category must be one of:"):
            tracker.filter_by_category("nonexistent_category")

    def test_record_transaction_with_float_amount(self):
        tracker = InvestmentTracker()

        # Test with a floating-point amount
        assert tracker.record_transaction(25.75, "food", "Lunch") == True

        # Verify that the transaction was recorded correctly
        expenses = tracker.filter_by_category("food")
        assert len(expenses) == 1, "Expected one food expense"
        assert expenses[0]["amount"] == 25.75, f"Expected amount 25.75, but got {expenses[0]['amount']}"
        assert expenses[0]["description"] == "Lunch", f"Expected description 'Lunch', but got {expenses[0]['description']}"

        # Verify that the overall spending is correct
        total_spending = tracker.calculate_overall_spending()
        assert total_spending == 25.75, f"Expected total spending to be 25.75, but got {total_spending}"

    def test_register_existing_default_category(self):
        tracker = InvestmentTracker()

        # Store the initial number of categories
        initial_category_count = len(tracker.categories)

        # Attempt to register an existing default category
        result = tracker.register_new_category("food")

        # Assert that the method returns False
        assert result == False, "Expected register_new_category to return False for existing category"

        # Assert that the number of categories hasn't changed
        assert len(tracker.categories) == initial_category_count, "Expected number of categories to remain unchanged"

        # Assert that "food" is still in the categories set
        assert "food" in tracker.categories, "Expected 'food' to still be in the categories set"

    def test_category_case_insensitivity(self):
        tracker = InvestmentTracker()

        # Record a transaction with uppercase category
        tracker.record_transaction(75.50, "FOOD", "Dinner at restaurant")

        # Filter expenses using lowercase category
        food_expenses = tracker.filter_by_category("food")

        # Assert that the transaction was retrieved
        assert len(food_expenses) == 1, "Expected one food expense"
        assert food_expenses[0]["amount"] == 75.50, f"Expected amount 75.50, but got {food_expenses[0]['amount']}"
        assert food_expenses[0]["description"] == "Dinner at restaurant", f"Expected description 'Dinner at restaurant', but got {food_expenses[0]['description']}"
        assert food_expenses[0]["category"] == "food", f"Expected category 'food', but got {food_expenses[0]['category']}"

        # Verify that filtering with uppercase category also works
        upper_food_expenses = tracker.filter_by_category("FOOD")
        assert len(upper_food_expenses) == 1, "Expected one food expense when filtering with uppercase category"
        assert upper_food_expenses == food_expenses, "Expenses should be the same regardless of category case"

    def test_record_transaction_with_whitespace_category(self):
        tracker = InvestmentTracker()

        # Record a transaction with whitespace in the category
        result = tracker.record_transaction(100.00, "  food  ", "Grocery shopping")

        # Assert that the transaction was recorded successfully
        assert result == True, "Expected record_transaction to return True"

        # Retrieve all food expenses
        food_expenses = tracker.filter_by_category("food")

        # Assert that exactly one expense was recorded
        assert len(food_expenses) == 1, f"Expected one food expense, but got {len(food_expenses)}"

        # Assert that the category was normalized (trimmed)
        assert food_expenses[0]["category"] == "food", f"Expected category 'food', but got '{food_expenses[0]['category']}'"

        # Assert that other details of the transaction are correct
        assert food_expenses[0]["amount"] == 100.00, f"Expected amount 100.00, but got {food_expenses[0]['amount']}"
        assert food_expenses[0]["description"] == "Grocery shopping", f"Expected description 'Grocery shopping', but got '{food_expenses[0]['description']}'"