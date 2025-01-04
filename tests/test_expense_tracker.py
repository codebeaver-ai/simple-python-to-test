import unittest

from expense_tracker import ExpenseTracker

class TestExpenseTracker(unittest.TestCase):
    def test_expense_tracker_initialization(self):
        tracker = ExpenseTracker()
        expected_categories = {"food", "transport", "utilities", "entertainment", "other"}
        self.assertEqual(tracker.categories, expected_categories, "Categories should be initialized correctly")
        self.assertEqual(len(tracker.expenses), 0, "Expenses list should be empty upon initialization")