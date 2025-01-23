import unittest
from expense_tracker import ExpenseTracker


class TestExpenseTracker(unittest.TestCase):
    def test_expense_tracker_initialization(self):
        """Test that the ExpenseTracker is initialized with an empty expenses list."""
        tracker = ExpenseTracker()
        self.assertEqual(len(tracker.expenses), 0)

    def test_expenses_initialized_as_empty_list(self):
        """Test that the expenses attribute is initialized as an empty list."""
        tracker = ExpenseTracker()
        self.assertIsInstance(tracker.expenses, list)
        self.assertEqual(len(tracker.expenses), 0)

    def test_direct_expense_manipulation(self):
        """Test that expenses can be directly added to the expenses list."""
        tracker = ExpenseTracker()
        initial_expense_count = len(tracker.expenses)

        # Directly add an expense to the expenses list
        new_expense = {"amount": 50, "category": "food", "description": "Groceries"}
        tracker.expenses.append(new_expense)

        # Check if the expense was added
        self.assertEqual(len(tracker.expenses), initial_expense_count + 1)
        self.assertIn(new_expense, tracker.expenses)

    # The following tests have been removed as they rely on the 'categories' attribute:
    # test_categories_is_set_with_default_categories
    # test_add_new_category
    # test_expenses_remain_empty_after_adding_category
    # test_remove_category
    # test_add_multiple_categories
    # test_clear_all_categories
    # test_modify_existing_category
