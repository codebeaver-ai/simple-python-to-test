import unittest

from investment_tracker import InvestmentTracker

class TestInvestmentTracker(unittest.TestCase):
    def test_register_new_category(self):
        tracker = InvestmentTracker()

        # Test registering a new category
        self.assertTrue(tracker.register_new_category("savings"))
        self.assertIn("savings", tracker.categories)

        # Test registering an existing category
        self.assertFalse(tracker.register_new_category("food"))

        # Test registering an invalid category (empty string)
        with self.assertRaises(ValueError):
            tracker.register_new_category("")

        # Test registering an invalid category (non-string)
        with self.assertRaises(ValueError):
            tracker.register_new_category(123)