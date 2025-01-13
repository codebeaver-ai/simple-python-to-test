import unittest

from expense_tracker import ExpenseTracker

class TestExpenseTracker(unittest.TestCase):
    def test_add_category(self):
        tracker = ExpenseTracker()

        # Test adding a new category
        self.assertTrue(tracker.add_category("groceries"))
        self.assertIn("groceries", tracker.categories)

        # Test adding an existing category (should return False)
        self.assertFalse(tracker.add_category("groceries"))

        # Test adding a category with spaces and uppercase (should be normalized)
        self.assertTrue(tracker.add_category(" HoUsE Supplies "))
        self.assertIn("house supplies", tracker.categories)

        # Test adding an invalid category (empty string)
        with self.assertRaises(ValueError):
            tracker.add_category("")

        # Test adding an invalid category (non-string)
        with self.assertRaises(ValueError):
            tracker.add_category(123)

    def test_get_category_total(self):
        tracker = ExpenseTracker()

        # Add expenses in different categories
        tracker.add_expense(50.00, "food", "Groceries")
        tracker.add_expense(30.00, "food", "Restaurant")
        tracker.add_expense(100.00, "utilities", "Electricity")
        tracker.add_expense(20.00, "food", "Snacks")

        # Test getting total for a specific category
        self.assertEqual(tracker.get_category_total("food"), 100.00)
        self.assertEqual(tracker.get_category_total("utilities"), 100.00)
        self.assertEqual(tracker.get_category_total("transport"), 0.00)

        # Test error case for invalid category
        with self.assertRaises(ValueError):
            tracker.get_category_total("invalid_category")

    def test_get_expenses_by_category(self):
        tracker = ExpenseTracker()

        # Add expenses in different categories
        tracker.add_expense(50.00, "food", "Groceries")
        tracker.add_expense(30.00, "food", "Restaurant")
        tracker.add_expense(100.00, "utilities", "Electricity")
        tracker.add_expense(20.00, "transport", "Bus ticket")

        # Test getting expenses for a specific category
        food_expenses = tracker.get_expenses_by_category("food")
        self.assertEqual(len(food_expenses), 2)
        self.assertEqual(food_expenses[0]["amount"], 50.00)
        self.assertEqual(food_expenses[1]["amount"], 30.00)

        # Test getting expenses for a category with no expenses
        entertainment_expenses = tracker.get_expenses_by_category("entertainment")
        self.assertEqual(len(entertainment_expenses), 0)

        # Test error case for invalid category
        with self.assertRaises(ValueError):
            tracker.get_expenses_by_category("invalid_category")

    def test_get_total_expenses(self):
        tracker = ExpenseTracker()

        # Add expenses in different categories
        tracker.add_expense(50.00, "food", "Groceries")
        tracker.add_expense(30.00, "transport", "Bus ticket")
        tracker.add_expense(100.00, "utilities", "Electricity")
        tracker.add_expense(20.00, "entertainment", "Movie ticket")

        # Calculate expected total
        expected_total = 50.00 + 30.00 + 100.00 + 20.00

        # Get total expenses
        total_expenses = tracker.get_total_expenses()

        # Assert that the total matches the expected value
        self.assertEqual(total_expenses, expected_total)

        # Add another expense and check if the total updates correctly
        tracker.add_expense(15.00, "food", "Snacks")
        expected_total += 15.00

        total_expenses = tracker.get_total_expenses()
        self.assertEqual(total_expenses, expected_total)

    def test_add_expense(self):
        tracker = ExpenseTracker()

        # Test adding a valid expense
        self.assertTrue(tracker.add_expense(50.00, "food", "Groceries"))
        self.assertEqual(len(tracker.expenses), 1)
        self.assertEqual(tracker.expenses[0]["amount"], 50.00)
        self.assertEqual(tracker.expenses[0]["category"], "food")
        self.assertEqual(tracker.expenses[0]["description"], "Groceries")

        # Test adding an expense with an invalid amount (negative number)
        with self.assertRaises(ValueError):
            tracker.add_expense(-10.00, "transport", "Bus ticket")

        # Test adding an expense with an invalid amount (zero)
        with self.assertRaises(ValueError):
            tracker.add_expense(0, "utilities", "Water bill")

        # Test adding an expense with an invalid category
        with self.assertRaises(ValueError):
            tracker.add_expense(30.00, "invalid_category", "Random expense")

        # Verify that only the valid expense was added
        self.assertEqual(len(tracker.expenses), 1)

    def test_add_multiple_categories(self):
        tracker = ExpenseTracker()

        # Add multiple new categories
        self.assertTrue(tracker.add_category("groceries"))
        self.assertTrue(tracker.add_category("rent"))
        self.assertTrue(tracker.add_category("healthcare"))

        # Verify that all new categories were added
        self.assertIn("groceries", tracker.categories)
        self.assertIn("rent", tracker.categories)
        self.assertIn("healthcare", tracker.categories)

        # Try adding an existing category (should return False)
        self.assertFalse(tracker.add_category("groceries"))

        # Verify that the number of categories is correct (5 default + 3 new)
        self.assertEqual(len(tracker.categories), 8)

        # Try adding a category with different casing (should be considered duplicate)
        self.assertFalse(tracker.add_category("Groceries"))

        # Verify that the number of categories hasn't changed
        self.assertEqual(len(tracker.categories), 8)

    def test_get_expenses_for_empty_category(self):
        tracker = ExpenseTracker()

        # Add an expense to a different category
        tracker.add_expense(50.00, "food", "Groceries")

        # Try to get expenses for a category that exists but has no expenses
        transport_expenses = tracker.get_expenses_by_category("transport")

        # Assert that the result is an empty list
        self.assertEqual(len(transport_expenses), 0)
        self.assertIsInstance(transport_expenses, list)

        # Add an expense to the previously empty category
        tracker.add_expense(20.00, "transport", "Bus ticket")

        # Get expenses for the category again
        updated_transport_expenses = tracker.get_expenses_by_category("transport")

        # Assert that the result now contains one expense
        self.assertEqual(len(updated_transport_expenses), 1)
        self.assertEqual(updated_transport_expenses[0]["amount"], 20.00)
        self.assertEqual(updated_transport_expenses[0]["description"], "Bus ticket")

    def test_get_category_total_for_custom_category(self):
        tracker = ExpenseTracker()

        # Add a new custom category
        new_category = "subscriptions"
        self.assertTrue(tracker.add_category(new_category))

        # Verify that the total for this category is initially zero
        self.assertEqual(tracker.get_category_total(new_category), 0.00)

        # Add an expense to the new category
        expense_amount = 15.99
        tracker.add_expense(expense_amount, new_category, "Monthly streaming service")

        # Verify that we can get the correct total for the new category
        self.assertEqual(tracker.get_category_total(new_category), expense_amount)

        # Verify that the total expenses have increased accordingly
        self.assertEqual(tracker.get_total_expenses(), expense_amount)

    def test_add_expense_with_non_numeric_amount(self):
        tracker = ExpenseTracker()

        # Test adding an expense with a string amount
        with self.assertRaises(ValueError):
            tracker.add_expense("fifty", "food", "Groceries")

        # Test adding an expense with a boolean amount
        with self.assertRaises(ValueError):
            tracker.add_expense(True, "transport", "Bus ticket")

        # Test adding an expense with None as amount
        with self.assertRaises(ValueError):
            tracker.add_expense(None, "utilities", "Electricity bill")

        # Verify that no expenses were added
        self.assertEqual(len(tracker.expenses), 0)

        # Add a valid expense to ensure the tracker still works correctly
        self.assertTrue(tracker.add_expense(50.00, "food", "Groceries"))
        self.assertEqual(len(tracker.expenses), 1)

    def test_add_expense_with_mixed_case_category(self):
        tracker = ExpenseTracker()

        # Add an expense with a mixed case category
        self.assertTrue(tracker.add_expense(75.50, "FoOd", "Dinner at restaurant"))

        # Verify that the expense was added correctly
        self.assertEqual(len(tracker.expenses), 1)
        self.assertEqual(tracker.expenses[0]["amount"], 75.50)
        self.assertEqual(tracker.expenses[0]["category"], "food")  # Should be lowercase
        self.assertEqual(tracker.expenses[0]["description"], "Dinner at restaurant")

        # Verify that we can retrieve this expense using lowercase category
        food_expenses = tracker.get_expenses_by_category("food")
        self.assertEqual(len(food_expenses), 1)
        self.assertEqual(food_expenses[0]["amount"], 75.50)

        # Verify that the total for the food category is correct
        self.assertEqual(tracker.get_category_total("food"), 75.50)

        # Try to add another expense with a different mixed case for the same category
        self.assertTrue(tracker.add_expense(30.25, "FOOd", "Groceries"))

        # Verify that both expenses are in the same category
        food_expenses = tracker.get_expenses_by_category("food")
        self.assertEqual(len(food_expenses), 2)
        self.assertEqual(tracker.get_category_total("food"), 105.75)