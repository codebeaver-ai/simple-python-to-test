import pytest
from datetime import datetime
from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

class TestInvestmentTracker:
    def test_calculate_overall_spending(self):
        tracker = InvestmentTracker()

        # Add some sample transactions
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Gas")
        tracker.record_transaction(200, "utilities", "Electricity bill")

        # Calculate the overall spending
        total_spending = tracker.calculate_overall_spending()

        # Assert that the total spending is correct
        assert total_spending == 350, f"Expected total spending to be 350, but got {total_spending}"

class TestInvestmentTracker:
    def test_filter_by_category(self):
        tracker = InvestmentTracker()

        # Add sample expenses
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Bus ticket")
        tracker.record_transaction(200, "food", "Restaurant dinner")
        tracker.record_transaction(75, "entertainment", "Movie tickets")

        # Test filtering by 'food' category
        food_expenses = tracker.filter_by_category("food")
        assert len(food_expenses) == 2
        assert all(expense["category"] == "food" for expense in food_expenses)
        assert sum(expense["amount"] for expense in food_expenses) == 300

        # Test filtering by 'transport' category
        transport_expenses = tracker.filter_by_category("transport")
        assert len(transport_expenses) == 1
        assert transport_expenses[0]["amount"] == 50
        assert transport_expenses[0]["description"] == "Bus ticket"

        # Test filtering by non-existent category
        with pytest.raises(ValueError):
            tracker.filter_by_category("invalid_category")

class TestInvestmentTracker:
    def test_compute_category_sum(self):
        tracker = InvestmentTracker()

        # Add sample expenses
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Bus ticket")
        tracker.record_transaction(200, "food", "Restaurant dinner")
        tracker.record_transaction(75, "entertainment", "Movie tickets")

        # Test sum for 'food' category
        food_sum = tracker.compute_category_sum("food")
        assert food_sum == 300, f"Expected food sum to be 300, but got {food_sum}"

        # Test sum for 'transport' category
        transport_sum = tracker.compute_category_sum("transport")
        assert transport_sum == 50, f"Expected transport sum to be 50, but got {transport_sum}"

        # Test sum for category with no expenses
        utilities_sum = tracker.compute_category_sum("utilities")
        assert utilities_sum == 0, f"Expected utilities sum to be 0, but got {utilities_sum}"

        # Test invalid category
        with pytest.raises(ValueError):
            tracker.compute_category_sum("invalid_category")