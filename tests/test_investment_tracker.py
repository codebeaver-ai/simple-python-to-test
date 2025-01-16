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

    def test_calculate_overall_spending(self):
        """
        Test that calculate_overall_spending correctly sums up all expenses
        across different categories.
        """
        tracker = InvestmentTracker()

        # Add multiple transactions
        tracker.record_transaction(50.00, "food", "Dinner")
        tracker.record_transaction(30.00, "transport", "Bus fare")
        tracker.record_transaction(100.00, "utilities", "Electricity bill")
        tracker.record_transaction(20.50, "entertainment", "Movie ticket")

        # Calculate total spending
        total_spending = tracker.calculate_overall_spending()

        # Assert the total is correct (50 + 30 + 100 + 20.50 = 200.50)
        self.assertAlmostEqual(total_spending, 200.50, places=2)
