import unittest

from expense_tracker import ExpenseTracker

class TestExpenseTracker(unittest.TestCase):
    def test_add_category(self):
        """
        Test the add_category method of ExpenseTracker.

        This test covers:
        1. Adding a new valid category
        2. Attempting to add an existing category
        3. Attempting to add an invalid category (empty string)
        """
        tracker = ExpenseTracker()

        # Test adding a new valid category
        self.assertTrue(tracker.add_category("savings"))
        self.assertIn("savings", tracker.categories)

        # Test adding an existing category
        self.assertFalse(tracker.add_category("food"))

        # Test adding an invalid category (empty string)
        with self.assertRaises(ValueError):
            tracker.add_category("")