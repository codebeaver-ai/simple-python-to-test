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
        tracker.record_transaction(100.50, "food", "Grocery shopping")
        tracker.record_transaction(50.00, "transport", "Gas")
        tracker.record_transaction(200.00, "utilities", "Electricity bill")

        # Calculate the overall spending
        total_spending = tracker.calculate_overall_spending()

        # Assert that the total spending is correct (100.50 + 50.00 + 200.00 = 350.50)
        assert total_spending == pytest.approx(350.50)

class TestInvestmentTracker:
    def test_filter_by_category(self):
        tracker = InvestmentTracker()

        # Add some sample transactions
        tracker.record_transaction(100.50, "food", "Grocery shopping")
        tracker.record_transaction(50.00, "transport", "Gas")
        tracker.record_transaction(200.00, "utilities", "Electricity bill")
        tracker.record_transaction(75.25, "food", "Restaurant dinner")

        # Test filtering by 'food' category
        food_expenses = tracker.filter_by_category("food")
        assert len(food_expenses) == 2
        assert food_expenses[0]["amount"] == 100.50
        assert food_expenses[1]["amount"] == 75.25

        # Test filtering by 'transport' category
        transport_expenses = tracker.filter_by_category("transport")
        assert len(transport_expenses) == 1
        assert transport_expenses[0]["amount"] == 50.00

        # Test filtering by non-existent category
        with pytest.raises(ValueError):
            tracker.filter_by_category("invalid_category")

class TestInvestmentTracker:
    def test_register_new_category(self):
        tracker = InvestmentTracker()

        # Test registering a new valid category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test registering an existing category (should return False)
        assert tracker.register_new_category("food") == False

        # Test registering an invalid category (empty string)
        with pytest.raises(ValueError):
            tracker.register_new_category("")

        # Test registering an invalid category (non-string)
        with pytest.raises(ValueError):
            tracker.register_new_category(123)