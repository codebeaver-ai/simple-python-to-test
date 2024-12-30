import pytest
from datetime import datetime
from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

class TestInvestmentTracker:
    def test_calculate_overall_spending(self):
        tracker = InvestmentTracker()

        # Add some sample expenses
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Bus fare")
        tracker.record_transaction(200, "utilities", "Electricity bill")

        # Calculate the total spending
        total_spending = tracker.calculate_overall_spending()

        # Assert that the total spending is correct
        assert total_spending == 350, f"Expected total spending to be 350, but got {total_spending}"

class TestInvestmentTracker:
    def test_filter_by_category(self):
        tracker = InvestmentTracker()

        # Add sample expenses
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Bus fare")
        tracker.record_transaction(75, "food", "Restaurant")

        # Filter expenses by category
        food_expenses = tracker.filter_by_category("food")

        # Assert that the filtered expenses are correct
        assert len(food_expenses) == 2, f"Expected 2 food expenses, but got {len(food_expenses)}"
        assert food_expenses[0]["amount"] == 100 and food_expenses[0]["description"] == "Groceries"
        assert food_expenses[1]["amount"] == 75 and food_expenses[1]["description"] == "Restaurant"

        # Test with a category that has no expenses
        entertainment_expenses = tracker.filter_by_category("entertainment")
        assert len(entertainment_expenses) == 0, "Expected no entertainment expenses"

        # Test with an invalid category
        with pytest.raises(ValueError):
            tracker.filter_by_category("invalid_category")

class TestInvestmentTracker:
    def test_compute_category_sum(self):
        tracker = InvestmentTracker()

        # Add sample expenses
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Bus fare")
        tracker.record_transaction(75, "food", "Restaurant")
        tracker.record_transaction(200, "utilities", "Electricity bill")

        # Compute sum for food category
        food_sum = tracker.compute_category_sum("food")

        # Assert that the sum is correct
        assert food_sum == 175, f"Expected food sum to be 175, but got {food_sum}"

        # Compute sum for a category with no expenses
        entertainment_sum = tracker.compute_category_sum("entertainment")
        assert entertainment_sum == 0, f"Expected entertainment sum to be 0, but got {entertainment_sum}"

        # Test with an invalid category
        with pytest.raises(ValueError):
            tracker.compute_category_sum("invalid_category")

class TestInvestmentTracker:
    def test_register_new_category(self):
        tracker = InvestmentTracker()

        # Test successful registration
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test registering existing category
        assert tracker.register_new_category("savings") == False

        # Test registering with different case
        assert tracker.register_new_category("INVESTMENTS") == True
        assert "investments" in tracker.categories

        # Test registering empty string
        with pytest.raises(ValueError):
            tracker.register_new_category("")

        # Test registering whitespace
        with pytest.raises(ValueError):
            tracker.register_new_category("   ")

        # Test registering non-string
        with pytest.raises(ValueError):
            tracker.register_new_category(123)

class TestInvestmentTracker:
    def test_calculate_overall_spending(self):
        tracker = InvestmentTracker()

        # Add some sample expenses
        tracker.record_transaction(100.50, "food", "Groceries")
        tracker.record_transaction(50.25, "transport", "Gas")
        tracker.record_transaction(200.00, "utilities", "Electricity")

        # Calculate the total spending
        total_spending = tracker.calculate_overall_spending()

        # Assert that the total spending is correct (rounded to 2 decimal places)
        expected_total = round(100.50 + 50.25 + 200.00, 2)
        assert total_spending == expected_total, f"Expected total spending to be {expected_total}, but got {total_spending}"