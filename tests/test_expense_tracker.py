import pytest
from expense_tracker import ExpenseTracker

class TestExpenseTracker:
    def test_add_category(self):
        tracker = ExpenseTracker()

        # Test adding a new valid category
        assert tracker.add_category("groceries") == True
        assert "groceries" in tracker.categories

        # Test adding an existing category (should return False)
        assert tracker.add_category("groceries") == False

        # Test adding an invalid category (empty string)
        with pytest.raises(ValueError):
            tracker.add_category("")

        # Test adding an invalid category (non-string)
        with pytest.raises(ValueError):
            tracker.add_category(123)

        # Test adding a category with leading/trailing spaces
        assert tracker.add_category("  hobbies  ") == True
        assert "hobbies" in tracker.categories

class TestExpenseTracker:
    def test_get_total_expenses(self):
        tracker = ExpenseTracker()

        # Add some expenses
        tracker.add_expense(50.0, "food", "Groceries")
        tracker.add_expense(30.0, "transport", "Bus fare")
        tracker.add_expense(100.0, "utilities", "Electricity bill")

        # Check if the total expenses are calculated correctly
        assert tracker.get_total_expenses() == 180.0

        # Add another expense and check again
        tracker.add_expense(20.0, "entertainment", "Movie ticket")
        assert tracker.get_total_expenses() == 200.0

class TestExpenseTracker:
    def test_get_expenses_by_category(self):
        tracker = ExpenseTracker()

        # Add some expenses
        tracker.add_expense(50.0, "food", "Groceries")
        tracker.add_expense(30.0, "transport", "Bus fare")
        tracker.add_expense(20.0, "food", "Restaurant")
        tracker.add_expense(100.0, "utilities", "Electricity bill")

        # Test getting expenses for the "food" category
        food_expenses = tracker.get_expenses_by_category("food")
        assert len(food_expenses) == 2
        assert food_expenses[0]["amount"] == 50.0
        assert food_expenses[0]["description"] == "Groceries"
        assert food_expenses[1]["amount"] == 20.0
        assert food_expenses[1]["description"] == "Restaurant"

        # Test getting expenses for the "transport" category
        transport_expenses = tracker.get_expenses_by_category("transport")
        assert len(transport_expenses) == 1
        assert transport_expenses[0]["amount"] == 30.0
        assert transport_expenses[0]["description"] == "Bus fare"

        # Test getting expenses for a category with no expenses
        entertainment_expenses = tracker.get_expenses_by_category("entertainment")
        assert len(entertainment_expenses) == 0

        # Test error case for invalid category
        with pytest.raises(ValueError):
            tracker.get_expenses_by_category("invalid_category")

class TestExpenseTracker:
    def test_get_category_total(self):
        tracker = ExpenseTracker()

        # Add some expenses
        tracker.add_expense(50.0, "food", "Groceries")
        tracker.add_expense(30.0, "transport", "Bus fare")
        tracker.add_expense(20.0, "food", "Restaurant")
        tracker.add_expense(100.0, "utilities", "Electricity bill")

        # Test getting total for a category with multiple expenses
        assert tracker.get_category_total("food") == 70.0

        # Test getting total for a category with one expense
        assert tracker.get_category_total("transport") == 30.0

        # Test getting total for a category with no expenses
        assert tracker.get_category_total("entertainment") == 0.0

        # Test error case for invalid category
        with pytest.raises(ValueError):
            tracker.get_category_total("invalid_category")

class TestExpenseTracker:
    def test_add_expense(self):
        tracker = ExpenseTracker()

        # Test adding a valid expense
        assert tracker.add_expense(50.0, "food", "Groceries") == True
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0] == {"amount": 50.0, "category": "food", "description": "Groceries"}

        # Test adding an expense with invalid amount (negative)
        with pytest.raises(ValueError):
            tracker.add_expense(-10.0, "transport", "Bus fare")

        # Test adding an expense with invalid amount (zero)
        with pytest.raises(ValueError):
            tracker.add_expense(0, "utilities", "Water bill")

        # Test adding an expense with invalid category
        with pytest.raises(ValueError):
            tracker.add_expense(30.0, "invalid_category", "Something")

        # Test adding an expense with uppercase category (should be converted to lowercase)
        assert tracker.add_expense(25.0, "ENTERTAINMENT", "Movie") == True
        assert tracker.expenses[-1]["category"] == "entertainment"

        # Verify the total number of expenses after all operations
        assert len(tracker.expenses) == 2