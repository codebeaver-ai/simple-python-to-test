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
        self.assertEqual(len(tracker.expenses), 0)  # Ensure expenses are still empty

    def test_direct_expense_manipulation(self):
        tracker = ExpenseTracker()
        initial_expense_count = len(tracker.expenses)
        initial_category_count = len(tracker.categories)

        # Directly add an expense to the expenses list
        new_expense = {"amount": 50, "category": "food", "description": "Groceries"}
        tracker.expenses.append(new_expense)

        # Check if the expense was added
        self.assertEqual(len(tracker.expenses), initial_expense_count + 1)
        self.assertIn(new_expense, tracker.expenses)

        # Ensure categories weren't affected
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
        self.assertEqual(len(tracker.expenses), 0)  # Ensure expenses are still empty

    def test_clear_all_categories(self):
        tracker = ExpenseTracker()
        initial_expense_count = len(tracker.expenses)

        # Clear all categories
        tracker.categories.clear()

        # Check if categories are empty
        self.assertEqual(len(tracker.categories), 0)

        # Ensure expenses weren't affected
        self.assertEqual(len(tracker.expenses), initial_expense_count)

    def test_modify_existing_category(self):
        tracker = ExpenseTracker()
        initial_category_count = len(tracker.categories)
        old_category = "entertainment"
        new_category = "entertainment_and_leisure"

        # Remove the old category and add the new one
        tracker.categories.remove(old_category)
        tracker.categories.add(new_category)

        # Check if the modification was successful
        self.assertEqual(len(tracker.categories), initial_category_count)
        self.assertNotIn(old_category, tracker.categories)
        self.assertIn(new_category, tracker.categories)

        # Ensure expenses weren't affected
        self.assertEqual(len(tracker.expenses), 0)

    def test_add_expense(self):
        """
        Test the add_expense method of ExpenseTracker.

        This test checks if:
        1. A valid expense is added correctly.
        2. An exception is raised for an invalid amount.
        3. An exception is raised for an invalid category.
        """
        tracker = ExpenseTracker()

        # Test adding a valid expense
        self.assertTrue(tracker.add_expense(50.0, "food", "Groceries"))
        self.assertEqual(len(tracker.expenses), 1)
        self.assertEqual(tracker.expenses[0]["amount"], 50.0)
        self.assertEqual(tracker.expenses[0]["category"], "food")
        self.assertEqual(tracker.expenses[0]["description"], "Groceries")

        # Test adding an expense with invalid amount
        with self.assertRaises(ValueError):
            tracker.add_expense(-10, "food", "Invalid amount")

        # Test adding an expense with invalid category
        with self.assertRaises(ValueError):
            tracker.add_expense(30, "invalid_category", "Invalid category")

    def test_get_total_expenses(self):
        """
        Test the get_total_expenses method of ExpenseTracker.

        This test checks if:
        1. The method correctly calculates the total of all added expenses.
        2. The total is accurate after adding multiple expenses.
        3. The method returns 0 when no expenses have been added.
        """
        tracker = ExpenseTracker()

        # Test with no expenses
        self.assertEqual(tracker.get_total_expenses(), 0)

        # Add multiple expenses
        tracker.add_expense(50.0, "food", "Groceries")
        tracker.add_expense(30.0, "transport", "Gas")
        tracker.add_expense(100.0, "utilities", "Electricity")

        # Calculate expected total
        expected_total = 50.0 + 30.0 + 100.0

        # Test the total expenses
        self.assertEqual(tracker.get_total_expenses(), expected_total)

        # Add one more expense
        tracker.add_expense(25.5, "entertainment", "Movie")
        expected_total += 25.5

        # Test the updated total expenses
        self.assertEqual(tracker.get_total_expenses(), expected_total)

    def test_get_expenses_by_category(self):
        """
        Test the get_expenses_by_category method of ExpenseTracker.

        This test checks if:
        1. The method correctly returns all expenses for a valid category.
        2. The method raises a ValueError for an invalid category.
        3. The returned expenses match the expected ones for the valid category.
        """
        tracker = ExpenseTracker()

        # Add expenses to multiple categories
        tracker.add_expense(50.0, "food", "Groceries")
        tracker.add_expense(30.0, "food", "Restaurant")
        tracker.add_expense(100.0, "utilities", "Electricity")
        tracker.add_expense(25.5, "entertainment", "Movie")

        # Test getting expenses for a valid category
        food_expenses = tracker.get_expenses_by_category("food")
        self.assertEqual(len(food_expenses), 2)
        self.assertEqual(food_expenses[0]["amount"], 50.0)
        self.assertEqual(food_expenses[0]["description"], "Groceries")
        self.assertEqual(food_expenses[1]["amount"], 30.0)
        self.assertEqual(food_expenses[1]["description"], "Restaurant")

        # Test getting expenses for an invalid category
        with self.assertRaises(ValueError):
            tracker.get_expenses_by_category("invalid_category")

        # Verify that the returned expenses match the expected ones
        utilities_expenses = tracker.get_expenses_by_category("utilities")
        self.assertEqual(len(utilities_expenses), 1)
        self.assertEqual(utilities_expenses[0]["amount"], 100.0)
        self.assertEqual(utilities_expenses[0]["description"], "Electricity")

    def test_get_category_total(self):
        """
        Test the get_category_total method of ExpenseTracker.

        This test checks if:
        1. The method correctly calculates the total expenses for a valid category.
        2. The method returns 0 for a category with no expenses.
        3. The method raises a ValueError for an invalid category.
        """
        tracker = ExpenseTracker()

        # Add expenses to multiple categories
        tracker.add_expense(50.0, "food", "Groceries")
        tracker.add_expense(30.0, "food", "Restaurant")
        tracker.add_expense(100.0, "utilities", "Electricity")
        tracker.add_expense(25.5, "entertainment", "Movie")

        # Test getting total for a category with multiple expenses
        self.assertAlmostEqual(tracker.get_category_total("food"), 80.0, places=2)

        # Test getting total for a category with one expense
        self.assertAlmostEqual(tracker.get_category_total("utilities"), 100.0, places=2)

        # Test getting total for a category with no expenses
        self.assertAlmostEqual(tracker.get_category_total("transport"), 0.0, places=2)

        # Test getting total for an invalid category
        with self.assertRaises(ValueError):
            tracker.get_category_total("invalid_category")

    # ... (other test methods)

    def test_get_category_total(self):
        """
        Test the get_category_total method of ExpenseTracker.

        This test checks if:
        1. The method correctly calculates the total expenses for a valid category.
        2. The method returns 0 for a category with no expenses.
        3. The method raises a ValueError for an invalid category.
        """
        tracker = ExpenseTracker()

        # Add expenses to multiple categories
        tracker.add_expense(50.0, "food", "Groceries")
        tracker.add_expense(30.0, "food", "Restaurant")
        tracker.add_expense(100.0, "utilities", "Electricity")
        tracker.add_expense(25.5, "entertainment", "Movie")

        # Test getting total for a category with multiple expenses
        self.assertAlmostEqual(tracker.get_category_total("food"), 80.0, places=2)

        # Test getting total for a category with one expense
        self.assertAlmostEqual(tracker.get_category_total("utilities"), 100.0, places=2)

        # Test getting total for a category with no expenses
        self.assertAlmostEqual(tracker.get_category_total("transport"), 0.0, places=2)

        # Test getting total for an invalid category
        with self.assertRaises(ValueError):
            tracker.get_category_total("invalid_category")

    # ... (other test methods)

    def test_get_category_total(self):
        """
        Test the get_category_total method of ExpenseTracker.

        This test checks if:
        1. The method correctly calculates the total expenses for a valid category.
        2. The method returns 0 for a category with no expenses.
        3. The method raises a ValueError for an invalid category.
        4. The method handles case-insensitivity for category names.
        """
        tracker = ExpenseTracker()

        # Add expenses to multiple categories
        tracker.add_expense(50.0, "food", "Groceries")
        tracker.add_expense(30.0, "Food", "Restaurant")  # Testing case-insensitivity
        tracker.add_expense(100.0, "utilities", "Electricity")
        tracker.add_expense(25.5, "entertainment", "Movie")

        # Test getting total for a category with multiple expenses
        self.assertAlmostEqual(tracker.get_category_total("food"), 80.0, places=2)

        # Test getting total for a category with one expense
        self.assertAlmostEqual(tracker.get_category_total("utilities"), 100.0, places=2)

        # Test getting total for a category with no expenses
        self.assertAlmostEqual(tracker.get_category_total("transport"), 0.0, places=2)

        # Test getting total for an invalid category
        with self.assertRaises(ValueError):
            tracker.get_category_total("invalid_category")

        # Test case-insensitivity
        self.assertAlmostEqual(tracker.get_category_total("FOOD"), 80.0, places=2)

    # ... (other test methods)

    def test_get_category_total(self):
        """
        Test the get_category_total method of ExpenseTracker.

        This test checks if:
        1. The method correctly calculates the total expenses for a valid category.
        2. The method returns 0 for a category with no expenses.
        3. The method raises a ValueError for an invalid category.
        4. The method handles case-insensitivity for category names.
        5. The method works correctly with floating-point amounts.
        """
        tracker = ExpenseTracker()

        # Add expenses to multiple categories
        tracker.add_expense(50.0, "food", "Groceries")
        tracker.add_expense(30.25, "Food", "Restaurant")  # Testing case-insensitivity
        tracker.add_expense(100.0, "utilities", "Electricity")
        tracker.add_expense(25.5, "entertainment", "Movie")

        # Test getting total for a category with multiple expenses
        self.assertAlmostEqual(tracker.get_category_total("food"), 80.25, places=2)

        # Test getting total for a category with one expense
        self.assertAlmostEqual(tracker.get_category_total("utilities"), 100.0, places=2)

        # Test getting total for a category with no expenses
        self.assertAlmostEqual(tracker.get_category_total("transport"), 0.0, places=2)

        # Test getting total for an invalid category
        with self.assertRaises(ValueError):
            tracker.get_category_total("invalid_category")

        # Test case-insensitivity
        self.assertAlmostEqual(tracker.get_category_total("FOOD"), 80.25, places=2)

        # Test with floating-point amounts
        tracker.add_expense(10.99, "food", "Snacks")
        self.assertAlmostEqual(tracker.get_category_total("food"), 91.24, places=2)

    # ... (other test methods)

    def test_get_category_total(self):
        """
        Test the get_category_total method of ExpenseTracker.

        This test checks if:
        1. The method correctly calculates the total expenses for a valid category.
        2. The method returns 0 for a category with no expenses.
        3. The method raises a ValueError for an invalid category.
        4. The method handles case-insensitivity for category names.
        5. The method works correctly with floating-point amounts.
        """
        tracker = ExpenseTracker()

        # Add expenses to multiple categories
        tracker.add_expense(50.0, "food", "Groceries")
        tracker.add_expense(30.25, "Food", "Restaurant")  # Testing case-insensitivity
        tracker.add_expense(100.0, "utilities", "Electricity")
        tracker.add_expense(25.5, "entertainment", "Movie")

        # Test getting total for a category with multiple expenses
        self.assertAlmostEqual(tracker.get_category_total("food"), 80.25, places=2)

        # Test getting total for a category with one expense
        self.assertAlmostEqual(tracker.get_category_total("utilities"), 100.0, places=2)

        # Test getting total for a category with no expenses
        self.assertAlmostEqual(tracker.get_category_total("transport"), 0.0, places=2)

        # Test getting total for an invalid category
        with self.assertRaises(ValueError):
            tracker.get_category_total("invalid_category")

        # Test case-insensitivity
        self.assertAlmostEqual(tracker.get_category_total("FOOD"), 80.25, places=2)

        # Test with floating-point amounts
        tracker.add_expense(10.99, "food", "Snacks")
        self.assertAlmostEqual(tracker.get_category_total("food"), 91.24, places=2)

    # ... (other test methods)

    def test_get_category_total(self):
        """
        Test the get_category_total method of ExpenseTracker.

        This test checks if:
        1. The method correctly calculates the total expenses for a valid category.
        2. The method returns 0 for a category with no expenses.
        3. The method raises a ValueError for an invalid category.
        4. The method handles case-insensitivity for category names.
        5. The method works correctly with floating-point amounts.
        """
        tracker = ExpenseTracker()

        # Add expenses to multiple categories
        tracker.add_expense(50.0, "food", "Groceries")
        tracker.add_expense(30.25, "Food", "Restaurant")  # Testing case-insensitivity
        tracker.add_expense(100.0, "utilities", "Electricity")
        tracker.add_expense(25.5, "entertainment", "Movie")

        # Test getting total for a category with multiple expenses
        self.assertAlmostEqual(tracker.get_category_total("food"), 80.25, places=2)

        # Test getting total for a category with one expense
        self.assertAlmostEqual(tracker.get_category_total("utilities"), 100.0, places=2)

        # Test getting total for a category with no expenses
        self.assertAlmostEqual(tracker.get_category_total("transport"), 0.0, places=2)

        # Test getting total for an invalid category
        with self.assertRaises(ValueError):
            tracker.get_category_total("invalid_category")

        # Test case-insensitivity
        self.assertAlmostEqual(tracker.get_category_total("FOOD"), 80.25, places=2)

        # Test with floating-point amounts
        tracker.add_expense(10.99, "food", "Snacks")
        self.assertAlmostEqual(tracker.get_category_total("food"), 91.24, places=2)