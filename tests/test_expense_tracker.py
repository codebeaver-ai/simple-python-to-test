from expense_tracker import ExpenseTracker

import unittest

class TestExpenseTracker(unittest.TestCase):
    def test_add_category(self):
        tracker = ExpenseTracker()

        # Test adding a new category
        self.assertTrue(tracker.add_category("groceries"))
        self.assertIn("groceries", tracker.categories)

        # Test adding an existing category (should return False)
        self.assertFalse(tracker.add_category("groceries"))

        # Test adding an invalid category (empty string)
        with self.assertRaises(ValueError):
            tracker.add_category("")

        # Test adding an invalid category (non-string)
        with self.assertRaises(ValueError):
            tracker.add_category(123)

if __name__ == '__main__':
    unittest.main()

def test_add_expense(self):
    tracker = ExpenseTracker()

    # Test adding a valid expense
    self.assertTrue(tracker.add_expense(50.00, "food", "Dinner"))
    self.assertEqual(len(tracker.expenses), 1)
    self.assertEqual(tracker.expenses[0]["amount"], 50.00)
    self.assertEqual(tracker.expenses[0]["category"], "food")
    self.assertEqual(tracker.expenses[0]["description"], "Dinner")

    # Test adding an expense with invalid amount (negative number)
    with self.assertRaises(ValueError):
        tracker.add_expense(-10.00, "food", "Invalid expense")

    # Test adding an expense with invalid category
    with self.assertRaises(ValueError):
        tracker.add_expense(30.00, "invalid_category", "Invalid category expense")

    # Verify that only the valid expense was added
    self.assertEqual(len(tracker.expenses), 1)

def test_get_total_expenses(self):
    tracker = ExpenseTracker()

    # Add multiple expenses
    tracker.add_expense(50.00, "food", "Dinner")
    tracker.add_expense(30.00, "transport", "Bus ticket")
    tracker.add_expense(100.00, "utilities", "Electricity bill")

    # Calculate expected total
    expected_total = 50.00 + 30.00 + 100.00

    # Get the actual total from the tracker
    actual_total = tracker.get_total_expenses()

    # Assert that the actual total matches the expected total
    self.assertEqual(actual_total, expected_total)

    # Add another expense and check again
    tracker.add_expense(25.50, "entertainment", "Movie ticket")
    expected_total += 25.50

    actual_total = tracker.get_total_expenses()
    self.assertEqual(actual_total, expected_total)

def test_get_expenses_by_category(self):
    tracker = ExpenseTracker()

    # Add expenses to different categories
    tracker.add_expense(50.00, "food", "Dinner")
    tracker.add_expense(30.00, "transport", "Bus ticket")
    tracker.add_expense(20.00, "food", "Lunch")
    tracker.add_expense(100.00, "utilities", "Electricity bill")

    # Test retrieving expenses for a valid category
    food_expenses = tracker.get_expenses_by_category("food")
    self.assertEqual(len(food_expenses), 2)
    self.assertEqual(food_expenses[0]["amount"], 50.00)
    self.assertEqual(food_expenses[1]["amount"], 20.00)

    # Test retrieving expenses for a category with no expenses
    entertainment_expenses = tracker.get_expenses_by_category("entertainment")
    self.assertEqual(len(entertainment_expenses), 0)

    # Test error handling for invalid category
    with self.assertRaises(ValueError):
        tracker.get_expenses_by_category("invalid_category")

def test_get_category_total(self):
    tracker = ExpenseTracker()

    # Add expenses to different categories
    tracker.add_expense(50.00, "food", "Dinner")
    tracker.add_expense(30.00, "transport", "Bus ticket")
    tracker.add_expense(20.00, "food", "Lunch")
    tracker.add_expense(100.00, "utilities", "Electricity bill")

    # Test category with multiple expenses
    self.assertEqual(tracker.get_category_total("food"), 70.00)

    # Test category with single expense
    self.assertEqual(tracker.get_category_total("transport"), 30.00)

    # Test category with no expenses
    self.assertEqual(tracker.get_category_total("entertainment"), 0.00)

    # Test error handling for invalid category
    with self.assertRaises(ValueError):
        tracker.get_category_total("invalid_category")

class TestExpenseTracker(unittest.TestCase):
    def test_case_insensitive_categories(self):
        tracker = ExpenseTracker()

        # Test adding expenses with different case for categories
        tracker.add_expense(50.00, "FOOD", "Dinner")
        tracker.add_expense(30.00, "Transport", "Bus ticket")
        tracker.add_expense(20.00, "food", "Lunch")

        # Test get_expenses_by_category with different case
        food_expenses = tracker.get_expenses_by_category("FoOd")
        self.assertEqual(len(food_expenses), 2)
        self.assertEqual(food_expenses[0]["amount"], 50.00)
        self.assertEqual(food_expenses[1]["amount"], 20.00)

        # Test get_category_total with different case
        self.assertEqual(tracker.get_category_total("TRANSPORT"), 30.00)

        # Test adding a new category with different case
        self.assertFalse(tracker.add_category("FOOD"))  # Should return False as 'food' already exists
        self.assertTrue(tracker.add_category("Groceries"))
        self.assertIn("groceries", tracker.categories)  # Should be stored in lowercase

class TestExpenseTracker(unittest.TestCase):
    def test_add_expense_with_zero_amount(self):
        tracker = ExpenseTracker()

        # Attempt to add an expense with zero amount
        with self.assertRaises(ValueError):
            tracker.add_expense(0, "food", "Invalid zero amount")

        # Verify that no expense was added
        self.assertEqual(len(tracker.expenses), 0)

        # Verify that a valid expense can still be added after the failed attempt
        tracker.add_expense(10, "food", "Valid expense")
        self.assertEqual(len(tracker.expenses), 1)
        self.assertEqual(tracker.expenses[0]["amount"], 10)

class TestExpenseTracker(unittest.TestCase):
    def test_expense_with_high_precision_amount(self):
        tracker = ExpenseTracker()

        # Add an expense with a high-precision amount
        precise_amount = 10.123456
        tracker.add_expense(precise_amount, "food", "Precise expense")

        # Verify that the expense was added correctly
        self.assertEqual(len(tracker.expenses), 1)
        self.assertEqual(tracker.expenses[0]["amount"], precise_amount)

        # Check if get_total_expenses maintains precision
        self.assertEqual(tracker.get_total_expenses(), precise_amount)

        # Check if get_category_total maintains precision
        self.assertEqual(tracker.get_category_total("food"), precise_amount)

        # Add another expense and check total
        tracker.add_expense(20.987654, "food", "Another precise expense")
        expected_total = 10.123456 + 20.987654

        # Verify total expenses
        self.assertAlmostEqual(tracker.get_total_expenses(), expected_total, places=6)

        # Verify category total
        self.assertAlmostEqual(tracker.get_category_total("food"), expected_total, places=6)

class TestExpenseTracker(unittest.TestCase):
    def test_expense_with_large_amount(self):
        tracker = ExpenseTracker()

        # Add an expense with a very large amount
        large_amount = 1_000_000_000_000  # 1 trillion
        tracker.add_expense(large_amount, "other", "Very large expense")

        # Verify that the expense was added correctly
        self.assertEqual(len(tracker.expenses), 1)
        self.assertEqual(tracker.expenses[0]["amount"], large_amount)
        self.assertEqual(tracker.expenses[0]["category"], "other")
        self.assertEqual(tracker.expenses[0]["description"], "Very large expense")

        # Check if get_total_expenses returns the correct large amount
        self.assertEqual(tracker.get_total_expenses(), large_amount)

        # Check if get_category_total returns the correct large amount
        self.assertEqual(tracker.get_category_total("other"), large_amount)

class TestExpenseTracker(unittest.TestCase):
    def test_add_expense_with_non_numeric_amount(self):
        tracker = ExpenseTracker()

        # Attempt to add an expense with a non-numeric amount
        with self.assertRaises(ValueError):
            tracker.add_expense("not a number", "food", "Invalid amount")

        # Verify that no expense was added
        self.assertEqual(len(tracker.expenses), 0)

        # Verify that a valid expense can still be added after the failed attempt
        tracker.add_expense(15.50, "food", "Valid expense")
        self.assertEqual(len(tracker.expenses), 1)
        self.assertEqual(tracker.expenses[0]["amount"], 15.50)
        self.assertEqual(tracker.expenses[0]["category"], "food")
        self.assertEqual(tracker.expenses[0]["description"], "Valid expense")