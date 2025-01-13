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

    def test_record_transaction(self):
        tracker = InvestmentTracker()

        # Test successful transaction recording
        self.assertTrue(tracker.record_transaction(50.00, "food", "Dinner"))
        self.assertEqual(len(tracker.expenses), 1)
        self.assertEqual(tracker.expenses[0]["amount"], 50.00)
        self.assertEqual(tracker.expenses[0]["category"], "food")
        self.assertEqual(tracker.expenses[0]["description"], "Dinner")

        # Test invalid amount (negative number)
        with self.assertRaises(ValueError):
            tracker.record_transaction(-10, "food", "Invalid expense")

        # Test invalid category
        with self.assertRaises(ValueError):
            tracker.record_transaction(30.00, "invalid_category", "Invalid category")

        # Verify that the invalid transactions were not added
        self.assertEqual(len(tracker.expenses), 1)

    def test_calculate_overall_spending(self):
        tracker = InvestmentTracker()

        # Add multiple transactions
        tracker.record_transaction(50.00, "food", "Dinner")
        tracker.record_transaction(30.00, "transport", "Bus ticket")
        tracker.record_transaction(100.00, "utilities", "Electricity bill")

        # Calculate total spending
        total_spending = tracker.calculate_overall_spending()

        # Verify the total is correct
        self.assertEqual(total_spending, 180.00)

    def test_filter_and_sum_by_category(self):
        tracker = InvestmentTracker()

        # Add multiple transactions
        tracker.record_transaction(50.00, "food", "Dinner")
        tracker.record_transaction(30.00, "food", "Lunch")
        tracker.record_transaction(100.00, "utilities", "Electricity bill")
        tracker.record_transaction(20.00, "transport", "Bus ticket")

        # Test filter_by_category
        food_expenses = tracker.filter_by_category("food")
        self.assertEqual(len(food_expenses), 2)
        self.assertEqual(food_expenses[0]["amount"], 50.00)
        self.assertEqual(food_expenses[1]["amount"], 30.00)

        # Test compute_category_sum
        food_sum = tracker.compute_category_sum("food")
        self.assertEqual(food_sum, 80.00)

        # Test invalid category for filter_by_category
        with self.assertRaises(ValueError):
            tracker.filter_by_category("invalid_category")

        # Test invalid category for compute_category_sum
        with self.assertRaises(ValueError):
            tracker.compute_category_sum("invalid_category")

def test_category_case_insensitivity(self):
    tracker = InvestmentTracker()

    # Record a transaction with mixed case category
    tracker.record_transaction(75.50, "FoOd", "Dinner at restaurant")

    # Filter by category with different case
    food_expenses = tracker.filter_by_category("fOoD")
    self.assertEqual(len(food_expenses), 1)
    self.assertEqual(food_expenses[0]["amount"], 75.50)
    self.assertEqual(food_expenses[0]["description"], "Dinner at restaurant")

    # Compute category sum with different case
    food_sum = tracker.compute_category_sum("FOOD")
    self.assertEqual(food_sum, 75.50)

    # Try to register a category with different case
    self.assertFalse(tracker.register_new_category("FoOd"))
    self.assertFalse(tracker.register_new_category("FOOD"))

    def test_floating_point_amounts(self):
        tracker = InvestmentTracker()

        # Record transactions with floating-point amounts
        tracker.record_transaction(10.99, "food", "Lunch")
        tracker.record_transaction(5.50, "food", "Coffee")
        tracker.record_transaction(20.75, "transport", "Taxi")

        # Test overall spending calculation
        total_spending = tracker.calculate_overall_spending()
        self.assertAlmostEqual(total_spending, 37.24, places=2)

        # Test category sum calculation
        food_sum = tracker.compute_category_sum("food")
        self.assertAlmostEqual(food_sum, 16.49, places=2)

        # Test filtering by category with floating-point amounts
        food_expenses = tracker.filter_by_category("food")
        self.assertEqual(len(food_expenses), 2)
        self.assertAlmostEqual(food_expenses[0]["amount"], 10.99, places=2)
        self.assertAlmostEqual(food_expenses[1]["amount"], 5.50, places=2)

    def test_record_transaction_with_zero_amount(self):
        tracker = InvestmentTracker()

        # Attempt to record a transaction with zero amount
        with self.assertRaises(ValueError) as context:
            tracker.record_transaction(0, "food", "Invalid zero amount")

        # Verify the error message
        self.assertEqual(str(context.exception), "Amount must be a positive number")

        # Verify that no transaction was added
        self.assertEqual(len(tracker.expenses), 0)

        # Verify that a valid transaction can still be added after the error
        self.assertTrue(tracker.record_transaction(10, "food", "Valid amount"))
        self.assertEqual(len(tracker.expenses), 1)

    def test_record_transaction_with_non_numeric_amount(self):
        tracker = InvestmentTracker()

        # Attempt to record a transaction with a non-numeric amount
        with self.assertRaises(ValueError) as context:
            tracker.record_transaction("not a number", "food", "Invalid amount")

        # Verify the error message
        self.assertEqual(str(context.exception), "Amount must be a positive number")

        # Verify that no transaction was added
        self.assertEqual(len(tracker.expenses), 0)

        # Verify that a valid transaction can still be added after the error
        self.assertTrue(tracker.record_transaction(15.50, "food", "Valid amount"))
        self.assertEqual(len(tracker.expenses), 1)

    def test_empty_category_operations(self):
        tracker = InvestmentTracker()

        # Add a transaction for one category
        tracker.record_transaction(50.00, "food", "Dinner")

        # Test filtering an empty category
        empty_category = tracker.filter_by_category("transport")
        self.assertEqual(len(empty_category), 0, "Expected empty list for category with no transactions")

        # Test computing sum for an empty category
        empty_sum = tracker.compute_category_sum("transport")
        self.assertEqual(empty_sum, 0, "Expected zero sum for category with no transactions")

        # Test filtering a non-existent category (should raise ValueError)
        with self.assertRaises(ValueError):
            tracker.filter_by_category("non_existent")

        # Test computing sum for a non-existent category (should raise ValueError)
        with self.assertRaises(ValueError):
            tracker.compute_category_sum("non_existent")

def test_register_substring_category(self):
    tracker = InvestmentTracker()

    # Attempt to register a category that's a substring of an existing category
    self.assertTrue(tracker.register_new_category("foo"), "Should be able to register 'foo' as a new category")
    self.assertIn("foo", tracker.categories, "'foo' should be in the categories set")

    # Verify that the original "food" category still exists
    self.assertIn("food", tracker.categories, "'food' should still be in the categories set")

    # Try to use the new category in a transaction
    self.assertTrue(tracker.record_transaction(25.00, "foo", "Test transaction"), "Should be able to record a transaction with the new 'foo' category")

    # Verify that the transaction was recorded correctly
    foo_expenses = tracker.filter_by_category("foo")
    self.assertEqual(len(foo_expenses), 1, "Should have one transaction in the 'foo' category")
    self.assertEqual(foo_expenses[0]["amount"], 25.00, "Transaction amount should be 25.00")
    self.assertEqual(foo_expenses[0]["description"], "Test transaction", "Transaction description should match")