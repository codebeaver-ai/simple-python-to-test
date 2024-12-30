import pytest
from datetime import datetime
from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_calculate_overall_spending(self):
        tracker = InvestmentTracker()

        # Add some sample transactions
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Gas")
        tracker.record_transaction(200, "utilities", "Electricity bill")

        # Calculate and assert the total spending
        total_spending = tracker.calculate_overall_spending()
        assert total_spending == 350, f"Expected total spending to be 350, but got {total_spending}"

    def test_filter_by_category(self):
        tracker = InvestmentTracker()

        # Add some sample transactions
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Gas")
        tracker.record_transaction(200, "food", "Restaurant")
        tracker.record_transaction(150, "utilities", "Electricity bill")

        # Filter expenses by category
        food_expenses = tracker.filter_by_category("food")

        # Assert the number of food expenses
        assert len(food_expenses) == 2, f"Expected 2 food expenses, but got {len(food_expenses)}"

        # Assert the contents of food expenses
        assert food_expenses[0]["amount"] == 100 and food_expenses[0]["description"] == "Groceries"
        assert food_expenses[1]["amount"] == 200 and food_expenses[1]["description"] == "Restaurant"

        # Test for an invalid category
        with pytest.raises(ValueError):
            tracker.filter_by_category("invalid_category")

    def test_compute_category_sum(self):
        tracker = InvestmentTracker()

        # Add sample transactions
        tracker.record_transaction(100, "food", "Groceries")
        tracker.record_transaction(50, "transport", "Gas")
        tracker.record_transaction(200, "food", "Restaurant")
        tracker.record_transaction(150, "utilities", "Electricity bill")

        # Compute sum for food category
        food_sum = tracker.compute_category_sum("food")
        assert food_sum == 300, f"Expected food sum to be 300, but got {food_sum}"

        # Compute sum for transport category
        transport_sum = tracker.compute_category_sum("transport")
        assert transport_sum == 50, f"Expected transport sum to be 50, but got {transport_sum}"

        # Test for an invalid category
        with pytest.raises(ValueError):
            tracker.compute_category_sum("invalid_category")

    def test_register_new_category(self):
        tracker = InvestmentTracker()

        # Test successful registration of a new category
        assert tracker.register_new_category("groceries") == True
        assert "groceries" in tracker.categories

        # Test unsuccessful registration with an empty string
        with pytest.raises(ValueError):
            tracker.register_new_category("")

        # Test unsuccessful registration with a non-string input
        with pytest.raises(ValueError):
            tracker.register_new_category(123)

        # Test registering an existing category (should return False)
        assert tracker.register_new_category("food") == False

        # Test case-insensitivity and stripping of whitespace
        assert tracker.register_new_category(" NEWCATEGORY ") == True
        assert "newcategory" in tracker.categories

    def test_calculate_overall_spending(self):
        tracker = InvestmentTracker()

        # Add some sample transactions
        tracker.record_transaction(100.50, "food", "Groceries")
        tracker.record_transaction(50.25, "transport", "Gas")
        tracker.record_transaction(200.75, "utilities", "Electricity bill")

        # Calculate the total spending
        total_spending = tracker.calculate_overall_spending()

        # Assert the total spending (sum of all transactions)
        expected_total = 100.50 + 50.25 + 200.75
        assert total_spending == expected_total, f"Expected total spending to be {expected_total}, but got {total_spending}"