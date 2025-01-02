import pytest

from datetime import datetime
from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    # ... existing tests ...

    def test_register_new_category(self):
        tracker = InvestmentTracker()

        # Test adding a new category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test adding an existing category (should return False)
        assert tracker.register_new_category("savings") == False

        # Test adding a category with spaces and uppercase (should be normalized)
        assert tracker.register_new_category("  New Category  ") == True
        assert "new category" in tracker.categories

    # ... existing tests ...

    def test_compute_category_sum(self):
        tracker = InvestmentTracker()

        # Add expenses in different categories
        tracker.record_transaction(50.00, "food", "Groceries")
        tracker.record_transaction(30.00, "food", "Restaurant")
        tracker.record_transaction(100.00, "utilities", "Electricity")
        tracker.record_transaction(20.00, "transport", "Bus ticket")

        # Compute sum for the "food" category
        food_sum = tracker.compute_category_sum("food")

        # Assert that the sum matches the expected total
        assert food_sum == 80.00, f"Expected food sum to be 80.00, but got {food_sum}"

        # Test for a category with no expenses
        entertainment_sum = tracker.compute_category_sum("entertainment")
        assert entertainment_sum == 0, f"Expected entertainment sum to be 0, but got {entertainment_sum}"

def test_filter_by_category_invalid_category(self):
    tracker = InvestmentTracker()

    # Add some sample transactions
    tracker.record_transaction(50.00, "food", "Groceries")
    tracker.record_transaction(30.00, "transport", "Bus ticket")

    # Test filtering with an invalid category
    with pytest.raises(ValueError) as excinfo:
        tracker.filter_by_category("invalid_category")

    # Check if the error message is as expected
    assert str(excinfo.value).startswith("Category must be one of:")

    # Ensure that valid categories still work
    food_expenses = tracker.filter_by_category("food")
    assert len(food_expenses) == 1
    assert food_expenses[0]["amount"] == 50.00
    assert food_expenses[0]["description"] == "Groceries"

    # ... existing tests ...

    def test_calculate_overall_spending(self):
        tracker = InvestmentTracker()

        # Add expenses in different categories
        tracker.record_transaction(50.00, "food", "Groceries")
        tracker.record_transaction(30.00, "transport", "Bus ticket")
        tracker.record_transaction(100.00, "utilities", "Electricity")
        tracker.record_transaction(20.00, "entertainment", "Movie")

        # Calculate overall spending
        total_spending = tracker.calculate_overall_spending()

        # Assert that the total matches the sum of all transactions
        expected_total = 50.00 + 30.00 + 100.00 + 20.00
        assert total_spending == expected_total, f"Expected total spending to be {expected_total}, but got {total_spending}"

    # ... existing tests ...

    def test_record_transaction_invalid_amount(self):
        tracker = InvestmentTracker()

        # Test with a negative amount
        with pytest.raises(ValueError) as excinfo:
            tracker.record_transaction(-50.00, "food", "Invalid expense")
        assert str(excinfo.value) == "Amount must be a positive number"

        # Test with a non-numeric amount
        with pytest.raises(ValueError) as excinfo:
            tracker.record_transaction("not a number", "food", "Invalid expense")
        assert str(excinfo.value) == "Amount must be a positive number"

    # ... existing tests ...

    def test_record_transaction_invalid_category(self):
        tracker = InvestmentTracker()

        # Attempt to record a transaction with an invalid category
        with pytest.raises(ValueError) as excinfo:
            tracker.record_transaction(50.00, "invalid_category", "Test expense")

        # Check if the error message is as expected
        assert str(excinfo.value).startswith("Category must be one of:")

        # Verify that no transaction was added
        assert len(tracker.expenses) == 0

        # Verify that a valid category still works
        assert tracker.record_transaction(50.00, "food", "Valid expense") == True
        assert len(tracker.expenses) == 1

    # ... existing tests ...

    def test_register_new_category_invalid_input(self):
        tracker = InvestmentTracker()

        # Test with empty string
        with pytest.raises(ValueError) as excinfo:
            tracker.register_new_category("")
        assert str(excinfo.value) == "Category must be a non-empty string"

        # Test with None
        with pytest.raises(ValueError) as excinfo:
            tracker.register_new_category(None)
        assert str(excinfo.value) == "Category must be a non-empty string"

        # Test with non-string type (integer)
        with pytest.raises(ValueError) as excinfo:
            tracker.register_new_category(123)
        assert str(excinfo.value) == "Category must be a non-empty string"

        # Verify that the categories set remains unchanged
        assert tracker.categories == set(["food", "transport", "utilities", "entertainment", "other"])

    # ... existing tests ...

    def test_filter_by_category(self):
        tracker = InvestmentTracker()

        # Add expenses in different categories
        tracker.record_transaction(50.00, "food", "Groceries")
        tracker.record_transaction(30.00, "transport", "Bus ticket")
        tracker.record_transaction(100.00, "food", "Restaurant")
        tracker.record_transaction(20.00, "entertainment", "Movie")

        # Filter expenses for the "food" category
        food_expenses = tracker.filter_by_category("food")

        # Assert that only food expenses are returned
        assert len(food_expenses) == 2, f"Expected 2 food expenses, but got {len(food_expenses)}"

        # Check if the returned expenses have the correct amounts and descriptions
        assert any(expense["amount"] == 50.00 and expense["description"] == "Groceries" for expense in food_expenses)
        assert any(expense["amount"] == 100.00 and expense["description"] == "Restaurant" for expense in food_expenses)

        # Verify that expenses from other categories are not included
        assert all(expense["category"] == "food" for expense in food_expenses)

    def test_compute_category_sum_invalid_category(self):
        tracker = InvestmentTracker()

        # Add some sample transactions
        tracker.record_transaction(50.00, "food", "Groceries")
        tracker.record_transaction(30.00, "transport", "Bus ticket")

        # Test computing sum for an invalid category
        with pytest.raises(ValueError) as excinfo:
            tracker.compute_category_sum("invalid_category")

        # Check if the error message is as expected
        assert str(excinfo.value).startswith("Category must be one of:")

        # Ensure that valid categories still work
        food_sum = tracker.compute_category_sum("food")
        assert food_sum == 50.00, f"Expected food sum to be 50.00, but got {food_sum}"

    def test_record_transaction_with_integer_amount(self):
        tracker = InvestmentTracker()

        # Test recording a transaction with an integer amount
        assert tracker.record_transaction(100, "food", "Dinner") == True

        # Verify that the transaction was recorded correctly
        assert len(tracker.expenses) == 1
        recorded_expense = tracker.expenses[0]
        assert recorded_expense["amount"] == 100
        assert recorded_expense["category"] == "food"
        assert recorded_expense["description"] == "Dinner"

        # Verify that the overall spending is calculated correctly
        assert tracker.calculate_overall_spending() == 100

        # Verify that filtering by category works with this transaction
        food_expenses = tracker.filter_by_category("food")
        assert len(food_expenses) == 1
        assert food_expenses[0] == recorded_expense