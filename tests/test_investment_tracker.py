from datetime import datetime

from investment_tracker import InvestmentTracker

import pytest

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

class TestInvestmentTracker:
    def test_register_new_category(self):
        tracker = InvestmentTracker()

        # Test registering a new category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test registering an existing category
        assert tracker.register_new_category("savings") == False

        # Test that the total number of categories has increased by 1
        assert len(tracker.categories) == 6  # 5 default categories + 1 new

class TestInvestmentTracker:
    def test_calculate_overall_spending(self):
        tracker = InvestmentTracker()

        # Add some transactions
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Bus ticket")
        tracker.record_transaction(200, "utilities", "Electricity bill")

        # Calculate total spending
        total_spending = tracker.calculate_overall_spending()

        # Assert that the total is correct
        assert total_spending == 350, f"Expected total spending to be 350, but got {total_spending}"

class TestInvestmentTracker:
    def test_filter_by_category(self):
        tracker = InvestmentTracker()

        # Add transactions in different categories
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Bus ticket")
        tracker.record_transaction(200, "food", "Restaurant")
        tracker.record_transaction(150, "utilities", "Electricity bill")

        # Filter by 'food' category
        food_expenses = tracker.filter_by_category("food")

        # Check if all returned expenses are in the 'food' category
        assert len(food_expenses) == 2
        assert all(expense['category'] == 'food' for expense in food_expenses)
        assert sum(expense['amount'] for expense in food_expenses) == 300

        # Test with an invalid category
        with pytest.raises(ValueError):
            tracker.filter_by_category("invalid_category")

class TestInvestmentTracker:
    def test_compute_category_sum(self):
        tracker = InvestmentTracker()

        # Add transactions in different categories
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Bus ticket")
        tracker.record_transaction(200, "food", "Restaurant")
        tracker.record_transaction(150, "utilities", "Electricity bill")

        # Compute sum for 'food' category
        food_sum = tracker.compute_category_sum("food")

        # Check if the sum is correct
        assert food_sum == 300, f"Expected food sum to be 300, but got {food_sum}"

        # Compute sum for 'transport' category
        transport_sum = tracker.compute_category_sum("transport")

        # Check if the sum is correct
        assert transport_sum == 50, f"Expected transport sum to be 50, but got {transport_sum}"

        # Test with an invalid category
        with pytest.raises(ValueError):
            tracker.compute_category_sum("invalid_category")