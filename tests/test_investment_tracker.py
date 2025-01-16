import unittest

from datetime import datetime
from investment_tracker import InvestmentTracker

class TestInvestmentTracker(unittest.TestCase):
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
        """
        Test that a new category can be registered successfully and that
        attempting to register an existing category returns False.
        """
        tracker = InvestmentTracker()

        # Test registering a new category
        self.assertTrue(tracker.register_new_category("savings"))
        self.assertIn("savings", tracker.categories)

        # Test registering an existing category
        self.assertFalse(tracker.register_new_category("food"))

        # Test registering with invalid input
        with self.assertRaises(ValueError):
            tracker.register_new_category("")
        with self.assertRaises(ValueError):
            tracker.register_new_category(123)