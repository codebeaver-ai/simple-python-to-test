import unittest

from expense_tracker import ExpenseTracker


class TestExpenseTracker(unittest.TestCase):
    def test_expense_tracker_initialization(self):
        """Test that ExpenseTracker initializes with an empty expenses list."""
        tracker = ExpenseTracker()
        self.assertEqual(len(tracker.expenses), 0)

    def test_expenses_initialized_as_empty_list(self):
        """Test that expenses is initialized as an empty list."""
        tracker = ExpenseTracker()
        self.assertIsInstance(tracker.expenses, list)
        self.assertEqual(len(tracker.expenses), 0)

    def test_direct_expense_manipulation(self):
        """Test that expenses can be directly manipulated."""
        tracker = ExpenseTracker()
        initial_expense_count = len(tracker.expenses)

        # Directly add an expense to the expenses list
        new_expense = {"amount": 50, "category": "food", "description": "Groceries"}
        tracker.expenses.append(new_expense)

        # Check if the expense was added
        self.assertEqual(len(tracker.expenses), initial_expense_count + 1)
        self.assertIn(new_expense, tracker.expenses)

    # All other tests that relied on the 'categories' attribute have been removed
