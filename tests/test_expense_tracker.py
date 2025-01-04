import unittest

from expense_tracker import ExpenseTracker

class TestExpenseTracker(unittest.TestCase):
    def test_add_category(self):
        tracker = ExpenseTracker()
        initial_category_count = len(tracker.categories)

        # Test adding a new category
        result = tracker.add_category("savings")
        self.assertTrue(result)
        self.assertEqual(len(tracker.categories), initial_category_count + 1)
        self.assertIn("savings", tracker.categories)

        # Test adding an existing category
        result = tracker.add_category("food")
        self.assertFalse(result)
        self.assertEqual(len(tracker.categories), initial_category_count + 1)

        # Test adding an invalid category (empty string)
        with self.assertRaises(ValueError):
            tracker.add_category("")

        # Test adding an invalid category (non-string)
        with self.assertRaises(ValueError):
            tracker.add_category(123)