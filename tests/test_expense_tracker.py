import unittest

from expense_tracker import ExpenseTracker

class TestExpenseTracker(unittest.TestCase):
    def test_add_category(self):
        tracker = ExpenseTracker()

        # Test adding a new category
        self.assertTrue(tracker.add_category("groceries"))
        self.assertIn("groceries", tracker.categories)

        # Test adding an existing category (should return False)
        self.assertFalse(tracker.add_category("groceries"))

        # Test adding a category with spaces and uppercase (should be normalized)
        self.assertTrue(tracker.add_category(" HoUsE Supplies "))
        self.assertIn("house supplies", tracker.categories)

        # Test adding an invalid category (empty string)
        with self.assertRaises(ValueError):
            tracker.add_category("")

        # Test adding an invalid category (non-string)
        with self.assertRaises(ValueError):
            tracker.add_category(123)