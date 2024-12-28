import pytest
from datetime import datetime
from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

class TestInvestmentTracker:
    def test_calculate_overall_spending(self):
        tracker = InvestmentTracker()

        # Add some transactions
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Gas")
        tracker.record_transaction(200, "utilities", "Electricity bill")

        # Calculate total spending
        total_spending = tracker.calculate_overall_spending()

        # Assert that the total is correct
        assert total_spending == 350, f"Expected total spending to be 350, but got {total_spending}"

class TestInvestmentTracker:
    def test_filter_by_category(self):
        tracker = InvestmentTracker()

        # Add some transactions
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Gas")
        tracker.record_transaction(200, "food", "Restaurant")

        # Filter by food category
        food_expenses = tracker.filter_by_category("food")

        # Assert that we got the correct expenses
        assert len(food_expenses) == 2
        assert food_expenses[0]["amount"] == 100
        assert food_expenses[0]["description"] == "Groceries"
        assert food_expenses[1]["amount"] == 200
        assert food_expenses[1]["description"] == "Restaurant"

        # Test filtering by a category with no expenses
        entertainment_expenses = tracker.filter_by_category("entertainment")
        assert len(entertainment_expenses) == 0

        # Test error case with invalid category
        with pytest.raises(ValueError):
            tracker.filter_by_category("invalid_category")

class TestInvestmentTracker:
    def test_register_new_category(self):
        tracker = InvestmentTracker()

        # Test successful category registration
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test registering an existing category (should return False)
        assert tracker.register_new_category("food") == False

        # Test registering an invalid category (should raise ValueError)
        with pytest.raises(ValueError):
            tracker.register_new_category("")

        with pytest.raises(ValueError):
            tracker.register_new_category(123)

        # Test case insensitivity and stripping
        assert tracker.register_new_category("  InVeStMeNtS  ") == True
        assert "investments" in tracker.categories