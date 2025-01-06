import unittest

from investment_tracker import InvestmentTracker

class TestInvestmentTracker(unittest.TestCase):
    def test_register_new_category(self):
        tracker = InvestmentTracker()
        initial_category_count = len(tracker.categories)

        # Test registering a new category
        result = tracker.register_new_category("savings")
        self.assertTrue(result)
        self.assertEqual(len(tracker.categories), initial_category_count + 1)
        self.assertIn("savings", tracker.categories)

        # Test registering an existing category
        result = tracker.register_new_category("food")
        self.assertFalse(result)
        self.assertEqual(len(tracker.categories), initial_category_count + 1)

        # Test registering an invalid category
        with self.assertRaises(ValueError):
            tracker.register_new_category("")