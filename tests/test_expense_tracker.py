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
        self.assertTrue(tracker.add_category("groceries"))
        self.assertIn("groceries", tracker.categories)

        # Test adding an existing category
        self.assertFalse(tracker.add_category("groceries"))

        # Test adding an invalid category (empty string)
        with self.assertRaises(ValueError):
            tracker.add_category("")

    def test_get_category_total(self):
        """
        Test the get_category_total method of ExpenseTracker.

        This test covers:
        1. Adding expenses to different categories
        2. Getting the total for a specific category
        3. Attempting to get the total for a non-existent category
        """
        tracker = ExpenseTracker()

        # Add expenses to different categories
        tracker.add_expense(50.00, "food", "Groceries")
        tracker.add_expense(30.00, "food", "Restaurant")
        tracker.add_expense(100.00, "transport", "Gas")

        # Test getting total for a specific category
        self.assertEqual(tracker.get_category_total("food"), 80.00)
        self.assertEqual(tracker.get_category_total("transport"), 100.00)
        self.assertEqual(tracker.get_category_total("utilities"), 0.00)

        # Test getting total for a non-existent category
        with self.assertRaises(ValueError):
            tracker.get_category_total("invalid_category")

    def test_get_expenses_by_category(self):
        """
        Test the get_expenses_by_category method of ExpenseTracker.

        This test covers:
        1. Adding expenses to different categories
        2. Retrieving expenses for a specific category
        3. Verifying the contents of the returned expenses
        4. Attempting to get expenses for a non-existent category
        """
        tracker = ExpenseTracker()

        # Add expenses to different categories
        tracker.add_expense(50.00, "food", "Groceries")
        tracker.add_expense(30.00, "food", "Restaurant")
        tracker.add_expense(100.00, "transport", "Gas")
        tracker.add_expense(20.00, "food", "Snacks")

        # Test retrieving expenses for a specific category
        food_expenses = tracker.get_expenses_by_category("food")
        self.assertEqual(len(food_expenses), 3)

        # Verify the contents of the returned expenses
        expected_food_expenses = [
            {"amount": 50.00, "category": "food", "description": "Groceries"},
            {"amount": 30.00, "category": "food", "description": "Restaurant"},
            {"amount": 20.00, "category": "food", "description": "Snacks"}
        ]
        self.assertEqual(food_expenses, expected_food_expenses)

        # Test retrieving expenses for a category with no expenses
        utilities_expenses = tracker.get_expenses_by_category("utilities")
        self.assertEqual(len(utilities_expenses), 0)

        # Test attempting to get expenses for a non-existent category
        with self.assertRaises(ValueError):
            tracker.get_expenses_by_category("invalid_category")

    def test_get_total_expenses(self):
        """
        Test the get_total_expenses method of ExpenseTracker.

        This test covers:
        1. Adding multiple expenses across different categories
        2. Calculating the total expenses
        3. Verifying the total when no expenses have been added
        """
        tracker = ExpenseTracker()

        # Test total expenses when no expenses have been added
        self.assertEqual(tracker.get_total_expenses(), 0.00)

        # Add multiple expenses across different categories
        tracker.add_expense(50.00, "food", "Groceries")
        tracker.add_expense(30.00, "transport", "Bus fare")
        tracker.add_expense(100.00, "utilities", "Electricity bill")
        tracker.add_expense(20.00, "entertainment", "Movie ticket")

        # Calculate expected total
        expected_total = 50.00 + 30.00 + 100.00 + 20.00

        # Test total expenses
        self.assertEqual(tracker.get_total_expenses(), expected_total)
