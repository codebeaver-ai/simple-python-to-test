import unittest
from expense_tracker import ExpenseTracker

class TestExpenseTracker(unittest.TestCase):
    def test_add_new_category_and_expense(self):
        tracker = ExpenseTracker()

        # Add a new category
        new_category = "healthcare"
        self.assertTrue(tracker.add_category(new_category))

        # Add an expense with the new category
        amount = 100.50
        description = "Doctor's appointment"
        self.assertTrue(tracker.add_expense(amount, new_category, description))

        # Check if the expense is correctly added
        expenses = tracker.get_expenses_by_category(new_category)
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]['amount'], amount)
        self.assertEqual(expenses[0]['category'], new_category)
        self.assertEqual(expenses[0]['description'], description)

        # Check the total for the new category
        self.assertEqual(tracker.get_category_total(new_category), amount)

if __name__ == '__main__':
    unittest.main()

    def test_add_expense_invalid_category(self):
        tracker = ExpenseTracker()

        # Attempt to add an expense with an invalid category
        with self.assertRaises(ValueError) as context:
            tracker.add_expense(50.00, "invalid_category", "Test expense")

        # Check if the error message is correct
        self.assertIn("Category must be one of:", str(context.exception))

        # Verify that no expense was added
        self.assertEqual(tracker.get_total_expenses(), 0)

        # Verify that the invalid category was not added to the categories set
        self.assertNotIn("invalid_category", tracker.categories)

    def test_get_total_expenses(self):
        tracker = ExpenseTracker()

        # Add multiple expenses
        tracker.add_expense(50.00, "food", "Groceries")
        tracker.add_expense(30.00, "transport", "Gas")
        tracker.add_expense(100.00, "utilities", "Electricity")

        # Check if the total is correct
        self.assertEqual(tracker.get_total_expenses(), 180.00)

        # Add another expense
        tracker.add_expense(25.50, "entertainment", "Movie tickets")

        # Check if the total is updated correctly
        self.assertEqual(tracker.get_total_expenses(), 205.50)

        # Add an expense with decimals
        tracker.add_expense(10.75, "food", "Snacks")

        # Check if the total is still accurate with decimals
        self.assertEqual(tracker.get_total_expenses(), 216.25)

    def test_add_category_invalid_input(self):
        tracker = ExpenseTracker()

        # Test adding an empty string as a category
        with self.assertRaises(ValueError) as context:
            tracker.add_category("")
        self.assertEqual(str(context.exception), "Category must be a non-empty string")

        # Test adding a whitespace-only string as a category
        with self.assertRaises(ValueError) as context:
            tracker.add_category("   ")
        self.assertEqual(str(context.exception), "Category must be a non-empty string")

        # Test adding a non-string (integer) as a category
        with self.assertRaises(ValueError) as context:
            tracker.add_category(123)
        self.assertEqual(str(context.exception), "Category must be a non-empty string")

        # Verify that no new categories were added
        original_categories = set(["food", "transport", "utilities", "entertainment", "other"])
        self.assertEqual(tracker.categories, original_categories)

        # Test adding a valid category
        self.assertTrue(tracker.add_category("healthcare"))
        self.assertIn("healthcare", tracker.categories)

        # Test adding an existing category (should return False)
        self.assertFalse(tracker.add_category("healthcare"))
        self.assertEqual(len(tracker.categories), len(original_categories) + 1)

    def test_get_expenses_by_category_invalid_category(self):
        tracker = ExpenseTracker()

        # Add some sample expenses
        tracker.add_expense(50.00, "food", "Groceries")
        tracker.add_expense(30.00, "transport", "Gas")

        # Attempt to get expenses for an invalid category
        with self.assertRaises(ValueError) as context:
            tracker.get_expenses_by_category("invalid_category")

        # Check if the error message contains the list of valid categories
        error_message = str(context.exception)
        self.assertIn("Category must be one of:", error_message)
        for category in tracker.categories:
            self.assertIn(category, error_message)

if __name__ == '__main__':
    unittest.main()

    def test_get_category_total(self):
        tracker = ExpenseTracker()

        # Add expenses to different categories
        tracker.add_expense(50.00, "food", "Groceries")
        tracker.add_expense(30.00, "food", "Restaurant")
        tracker.add_expense(100.00, "utilities", "Electricity")
        tracker.add_expense(20.00, "food", "Snacks")

        # Test valid category total
        self.assertEqual(tracker.get_category_total("food"), 100.00)
        self.assertEqual(tracker.get_category_total("utilities"), 100.00)
        self.assertEqual(tracker.get_category_total("transport"), 0.00)  # Category exists but no expenses

        # Test case insensitivity
        self.assertEqual(tracker.get_category_total("FOOD"), 100.00)

        # Test invalid category
        with self.assertRaises(ValueError) as context:
            tracker.get_category_total("invalid_category")
        self.assertIn("Category must be one of:", str(context.exception))

if __name__ == '__main__':
    unittest.main()

    def test_add_expense_negative_amount(self):
        tracker = ExpenseTracker()

        # Attempt to add an expense with a negative amount
        with self.assertRaises(ValueError) as context:
            tracker.add_expense(-50.00, "food", "Negative expense")

        # Check if the error message is correct
        self.assertEqual(str(context.exception), "Amount must be a positive number")

        # Verify that no expense was added
        self.assertEqual(tracker.get_total_expenses(), 0)

        # Verify that adding a valid expense still works
        self.assertTrue(tracker.add_expense(50.00, "food", "Valid expense"))
        self.assertEqual(tracker.get_total_expenses(), 50.00)

if __name__ == '__main__':
    unittest.main()

    def test_add_expense_zero_amount(self):
        tracker = ExpenseTracker()

        # Attempt to add an expense with a zero amount
        with self.assertRaises(ValueError) as context:
            tracker.add_expense(0.00, "food", "Zero expense")

        # Check if the error message is correct
        self.assertEqual(str(context.exception), "Amount must be a positive number")

        # Verify that no expense was added
        self.assertEqual(tracker.get_total_expenses(), 0)

        # Verify that adding a valid expense still works
        self.assertTrue(tracker.add_expense(50.00, "food", "Valid expense"))
        self.assertEqual(tracker.get_total_expenses(), 50.00)

if __name__ == '__main__':
    unittest.main()

    def test_add_expense_case_insensitive_category(self):
        tracker = ExpenseTracker()

        # Add an expense with a category in uppercase
        self.assertTrue(tracker.add_expense(50.00, "FOOD", "Groceries"))

        # Add another expense with the same category in lowercase
        self.assertTrue(tracker.add_expense(30.00, "food", "Restaurant"))

        # Verify that both expenses are added to the same category
        food_expenses = tracker.get_expenses_by_category("food")
        self.assertEqual(len(food_expenses), 2)

        # Verify that the total for the category is correct
        self.assertEqual(tracker.get_category_total("food"), 80.00)

        # Verify that querying with uppercase also works
        upper_food_expenses = tracker.get_expenses_by_category("FOOD")
        self.assertEqual(len(upper_food_expenses), 2)
        self.assertEqual(tracker.get_category_total("FOOD"), 80.00)

if __name__ == '__main__':
    unittest.main()

    def test_add_expense_non_numeric_amount(self):
        tracker = ExpenseTracker()

        # Attempt to add an expense with a non-numeric amount
        with self.assertRaises(ValueError) as context:
            tracker.add_expense("fifty", "food", "Invalid amount expense")

        # Check if the error message is correct
        self.assertEqual(str(context.exception), "Amount must be a positive number")

        # Verify that no expense was added
        self.assertEqual(tracker.get_total_expenses(), 0)

        # Verify that adding a valid expense still works
        self.assertTrue(tracker.add_expense(50.00, "food", "Valid expense"))
        self.assertEqual(tracker.get_total_expenses(), 50.00)

if __name__ == '__main__':
    unittest.main()