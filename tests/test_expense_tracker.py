import unittest

from expense_tracker import ExpenseTracker

class TestExpenseTracker(unittest.TestCase):
    def test_expense_tracker_initialization(self):
        tracker = ExpenseTracker()
        expected_categories = {"food", "transport", "utilities", "entertainment", "other"}
        self.assertEqual(tracker.categories, expected_categories)
        self.assertEqual(len(tracker.expenses), 0)

    def test_expenses_initialized_as_empty_list(self):
        tracker = ExpenseTracker()
        self.assertIsInstance(tracker.expenses, list)
        self.assertEqual(len(tracker.expenses), 0)

    def test_categories_is_set_with_default_categories(self):
        tracker = ExpenseTracker()
        self.assertIsInstance(tracker.categories, set)
        expected_categories = {"food", "transport", "utilities", "entertainment", "other"}
        self.assertEqual(tracker.categories, expected_categories)
        for category in expected_categories:
            self.assertIn(category, tracker.categories)

    def test_add_new_category(self):
        tracker = ExpenseTracker()
        initial_category_count = len(tracker.categories)
        new_category = "healthcare"
        tracker.categories.add(new_category)
        self.assertEqual(len(tracker.categories), initial_category_count + 1)
        self.assertIn(new_category, tracker.categories)

    def test_expenses_remain_empty_after_adding_category(self):
        tracker = ExpenseTracker()
        initial_expense_count = len(tracker.expenses)
        new_category = "healthcare"
        tracker.categories.add(new_category)
        self.assertEqual(len(tracker.expenses), initial_expense_count)
        self.assertEqual(len(tracker.expenses), 0)

    def test_remove_category(self):
        tracker = ExpenseTracker()
        initial_category_count = len(tracker.categories)
        category_to_remove = "entertainment"

        tracker.categories.remove(category_to_remove)

        self.assertEqual(len(tracker.categories), initial_category_count - 1)
        self.assertNotIn(category_to_remove, tracker.categories)
        self.assertEqual(len(tracker.expenses), 0)

    def test_direct_expense_manipulation(self):
        tracker = ExpenseTracker()
        initial_expense_count = len(tracker.expenses)
        initial_category_count = len(tracker.categories)

        new_expense = {"amount": 50, "category": "food", "description": "Groceries"}
        tracker.expenses.append(new_expense)

        self.assertEqual(len(tracker.expenses), initial_expense_count + 1)
        self.assertIn(new_expense, tracker.expenses)

        self.assertEqual(len(tracker.categories), initial_category_count)
        self.assertNotIn("Groceries", tracker.categories)

    def test_add_multiple_categories(self):
        tracker = ExpenseTracker()
        initial_category_count = len(tracker.categories)
        new_categories = {"healthcare", "education", "savings"}

        tracker.categories.update(new_categories)

        self.assertEqual(len(tracker.categories), initial_category_count + len(new_categories))
        for category in new_categories:
            self.assertIn(category, tracker.categories)
        self.assertEqual(len(tracker.expenses), 0)

    def test_clear_all_categories(self):
        tracker = ExpenseTracker()
        initial_expense_count = len(tracker.expenses)

        tracker.categories.clear()

        self.assertEqual(len(tracker.categories), 0)
        self.assertEqual(len(tracker.expenses), initial_expense_count)

    def test_modify_existing_category(self):
        tracker = ExpenseTracker()
        initial_category_count = len(tracker.categories)
        old_category = "entertainment"
        new_category = "entertainment_and_leisure"

        tracker.categories.remove(old_category)
        tracker.categories.add(new_category)

        self.assertEqual(len(tracker.categories), initial_category_count)
        self.assertNotIn(old_category, tracker.categories)
        self.assertIn(new_category, tracker.categories)
        self.assertEqual(len(tracker.expenses), 0)

    def test_add_expense(self):
        tracker = ExpenseTracker()

        self.assertTrue(tracker.add_expense(50.0, "food", "Groceries"))
        self.assertEqual(len(tracker.expenses), 1)
        self.assertEqual(tracker.get_total_expenses(), 50.0)

        self.assertTrue(tracker.add_expense(30.0, "transport", "Bus ticket"))
        self.assertEqual(len(tracker.expenses), 2)
        self.assertEqual(tracker.get_total_expenses(), 80.0)

        self.assertEqual(tracker.expenses[0], {"amount": 50.0, "category": "food", "description": "Groceries"})
        self.assertEqual(tracker.expenses[1], {"amount": 30.0, "category": "transport", "description": "Bus ticket"})

    def test_add_category(self):
        tracker = ExpenseTracker()
        initial_category_count = len(tracker.categories)

        self.assertTrue(tracker.add_category("healthcare"))
        self.assertEqual(len(tracker.categories), initial_category_count + 1)
        self.assertIn("healthcare", tracker.categories)

        self.assertFalse(tracker.add_category("healthcare"))
        self.assertEqual(len(tracker.categories), initial_category_count + 1)

        with self.assertRaises(ValueError):
            tracker.add_category("")

        with self.assertRaises(ValueError):
            tracker.add_category(123)

        self.assertEqual(len(tracker.categories), initial_category_count + 1)

    def test_get_expenses_by_category(self):
        tracker = ExpenseTracker()

        tracker.add_expense(50.0, "food", "Groceries")
        tracker.add_expense(30.0, "transport", "Bus ticket")
        tracker.add_expense(25.0, "food", "Restaurant")

        food_expenses = tracker.get_expenses_by_category("food")
        self.assertEqual(len(food_expenses), 2)
        self.assertEqual(food_expenses[0]["amount"], 50.0)
        self.assertEqual(food_expenses[1]["amount"], 25.0)

        entertainment_expenses = tracker.get_expenses_by_category("entertainment")
        self.assertEqual(len(entertainment_expenses), 0)

        with self.assertRaises(ValueError):
            tracker.get_expenses_by_category("invalid_category")

    def test_get_category_total(self):
        tracker = ExpenseTracker()

        tracker.add_expense(50.0, "food", "Groceries")
        tracker.add_expense(30.0, "transport", "Bus ticket")
        tracker.add_expense(25.0, "food", "Restaurant")
        tracker.add_expense(100.0, "utilities", "Electricity bill")

        self.assertEqual(tracker.get_category_total("food"), 75.0)
        self.assertEqual(tracker.get_category_total("transport"), 30.0)
        self.assertEqual(tracker.get_category_total("entertainment"), 0.0)

        with self.assertRaises(ValueError):
            tracker.get_category_total("invalid_category")

    def test_add_expense_with_invalid_amount(self):
        tracker = ExpenseTracker()

        with self.assertRaises(ValueError):
            tracker.add_expense(0, "food", "Invalid expense")

        with self.assertRaises(ValueError):
            tracker.add_expense(-50, "transport", "Invalid expense")

        self.assertEqual(len(tracker.expenses), 0)
        self.assertEqual(tracker.get_total_expenses(), 0)

    def test_add_expense_case_insensitive_category(self):
        """
        Test that adding an expense with a category name in uppercase
        is successful and the category is stored in lowercase.
        """
        tracker = ExpenseTracker()

        # Add an expense

    def test_add_expense_case_insensitive_category(self):
        """
        Test that adding an expense with a category name in uppercase
        is successful and the category is stored in lowercase.
        """
        tracker = ExpenseTracker()

        # Add an expense with an uppercase category
        self.assertTrue(tracker.add_expense(75.0, "FOOD", "Dinner"))

        # Check if the expense was added successfully
        self.assertEqual(len(tracker.expenses), 1)

        # Verify that the category was stored in lowercase
        added_expense = tracker.expenses[0]
        self.assertEqual(added_expense["category"], "food")

        # Ensure the other details were stored correctly
        self.assertEqual(added_expense["amount"], 75.0)
        self.assertEqual(added_expense["description"], "Dinner")

        # Verify that we can retrieve this expense using the lowercase category
        food_expenses = tracker.get_expenses_by_category("food")
        self.assertEqual(len(food_expenses), 1)
        self.assertEqual(food_expenses[0], added_expense)

    def test_get_total_expenses_with_no_expenses(self):
        """
        Test that get_total_expenses returns 0 when no expenses have been added.
        This ensures the method handles an empty expense list correctly.
        """
        tracker = ExpenseTracker()

        # Verify that the total expenses is 0 when no expenses have been added
        self.assertEqual(tracker.get_total_expenses(), 0)

        # Add an expense and verify the total changes
        tracker.add_expense(50.0, "food", "Groceries")
        self.assertEqual(tracker.get_total_expenses(), 50.0)

        # Remove all expenses and check if the total returns to 0
        tracker.expenses.clear()
        self.assertEqual(tracker.get_total_expenses(), 0)