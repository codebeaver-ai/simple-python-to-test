import pytest

from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    def test_register_new_category(self):
        """
        Test the register_new_category method of InvestmentTracker.

        This test covers:
        1. Successfully adding a new category
        2. Attempting to add an existing category (should return False)
        3. Attempting to add an invalid category (should raise ValueError)
        """
        tracker = InvestmentTracker()

        # Test adding a new category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test adding an existing category
        assert tracker.register_new_category("food") == False

        # Test adding an invalid category
        with pytest.raises(ValueError):
            tracker.register_new_category("")

        with pytest.raises(ValueError):
            tracker.register_new_category(123)

    def test_record_transaction(self):
        """
        Test the record_transaction method of InvestmentTracker.

        This test covers:
        1. Successfully recording a valid transaction
        2. Attempting to record a transaction with an invalid amount (should raise ValueError)
        3. Attempting to record a transaction with an invalid category (should raise ValueError)
        """
        tracker = InvestmentTracker()

        # Test recording a valid transaction
        assert tracker.record_transaction(50.00, "food", "Grocery shopping") == True
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0] == {"amount": 50.00, "category": "food", "description": "Grocery shopping"}

        # Test recording a transaction with an invalid amount
        with pytest.raises(ValueError):
            tracker.record_transaction(-10, "food", "Invalid amount")

        # Test recording a transaction with an invalid category
        with pytest.raises(ValueError):
            tracker.record_transaction(30.00, "invalid_category", "Invalid category")

        # Ensure no additional transactions were added after the invalid attempts
        assert len(tracker.expenses) == 1

    def test_calculate_overall_spending(self):
        """
        Test the calculate_overall_spending method of InvestmentTracker.

        This test covers:
        1. Adding multiple transactions across different categories
        2. Calculating the total spending across all categories
        3. Verifying that the calculated total is correct
        """
        tracker = InvestmentTracker()

        # Add multiple transactions
        tracker.record_transaction(50.00, "food", "Grocery shopping")
        tracker.record_transaction(30.00, "transport", "Bus fare")
        tracker.record_transaction(100.00, "utilities", "Electricity bill")
        tracker.record_transaction(20.00, "entertainment", "Movie ticket")

        # Calculate overall spending
        total_spending = tracker.calculate_overall_spending()

        # Assert that the total is correct (50 + 30 + 100 + 20 = 200)
        assert total_spending == 200.00

    def test_filter_and_sum_by_category(self):
        """
        Test the filter_by_category and compute_category_sum methods of InvestmentTracker.

        This test covers:
        1. Adding multiple transactions across different categories
        2. Filtering expenses by a specific category
        3. Computing the sum of expenses for a specific category
        4. Verifying that the filtered list and computed sum are correct
        5. Checking that an invalid category raises a ValueError
        """
        tracker = InvestmentTracker()

        # Add multiple transactions
        tracker.record_transaction(50.00, "food", "Grocery shopping")
        tracker.record_transaction(30.00, "food", "Restaurant dinner")
        tracker.record_transaction(100.00, "utilities", "Electricity bill")
        tracker.record_transaction(20.00, "food", "Snacks")

        # Filter expenses by category
        food_expenses = tracker.filter_by_category("food")

        # Assert that the filtered list is correct
        assert len(food_expenses) == 3
        assert sum(expense['amount'] for expense in food_expenses) == 100.00

        # Compute sum for food category
        food_sum = tracker.compute_category_sum("food")

        # Assert that the computed sum is correct
        assert food_sum == 100.00

        # Test with invalid category
        with pytest.raises(ValueError):
            tracker.filter_by_category("invalid_category")

        with pytest.raises(ValueError):
            tracker.compute_category_sum("invalid_category")

    def test_multiple_transactions(self):
        """
        Test recording and calculating multiple transactions across different categories.

        This test covers:
        1. Recording multiple transactions across different categories
        2. Verifying that all transactions are correctly stored
        3. Checking that the overall spending is calculated correctly
        4. Ensuring that transactions with the same category are handled properly
        """
        tracker = InvestmentTracker()

        # Record multiple transactions
        transactions = [
            (50.00, "food", "Grocery shopping"),
            (30.00, "transport", "Bus fare"),
            (100.00, "utilities", "Electricity bill"),
            (20.00, "food", "Restaurant"),
            (15.00, "entertainment", "Movie ticket"),
            (5.00, "food", "Snacks"),
        ]

        for amount, category, description in transactions:
            assert tracker.record_transaction(amount, category, description) == True

        # Verify that all transactions are stored
        assert len(tracker.expenses) == len(transactions)

        # Check that the overall spending is calculated correctly
        expected_total = sum(amount for amount, _, _ in transactions)
        assert tracker.calculate_overall_spending() == expected_total

        # Verify that transactions for the same category are handled correctly
        food_expenses = tracker.filter_by_category("food")
        assert len(food_expenses) == 3
        assert tracker.compute_category_sum("food") == 75.00

        # Check that each category has the correct number of transactions
        category_counts = {
            "food": 3,
            "transport": 1,
            "utilities": 1,
            "entertainment": 1,
        }
        for category, count in category_counts.items():
            assert len(tracker.filter_by_category(category)) == count

    def test_record_transaction_non_numeric_amount(self):
        """
        Test that attempting to record a transaction with a non-numeric amount raises a ValueError.

        This test covers:
        1. Attempting to record a transaction with a string amount
        2. Verifying that a ValueError is raised
        3. Ensuring that no transaction is added to the expenses list
        """
        tracker = InvestmentTracker()

        # Attempt to record a transaction with a string amount
        with pytest.raises(ValueError):
            tracker.record_transaction("fifty", "food", "Invalid amount")

        # Ensure no transaction was added
        assert len(tracker.expenses) == 0

    def test_register_existing_category_different_case(self):
        """
        Test registering a category that already exists but with different case.

        This test covers:
        1. Attempting to register a category that already exists in a different case
        2. Verifying that the method returns False (category not added)
        3. Ensuring that the original category remains in the set and no duplicate is added
        """
        tracker = InvestmentTracker()

        # The 'food' category is already in the default set
        assert "food" in tracker.categories

        # Attempt to register 'FOOD' (uppercase version of existing category)
        result = tracker.register_new_category("FOOD")

        # The method should return False as the category already exists
        assert result == False

        # Verify that only the original 'food' category exists in the set
        assert "food" in tracker.categories
        assert "FOOD" not in tracker.categories

        # Ensure no duplicate category was added
        assert len([cat for cat in tracker.categories if cat.lower() == 'food']) == 1

    def test_record_transaction_with_numeric_amount(self):
        """
        Test recording a transaction with a valid numeric amount.

        This test covers:
        1. Attempting to record a transaction with a valid numeric amount
        2. Verifying that the transaction is successfully recorded
        3. Ensuring that the amount is correctly stored as a float
        """
        tracker = InvestmentTracker()

        # Attempt to record a transaction with a numeric amount
        result = tracker.record_transaction(50.00, "food", "Grocery shopping")

        # The method should return True as the transaction should be recorded successfully
        assert result == True

        # Verify that the transaction was added to the expenses list
        assert len(tracker.expenses) == 1

        # Check that the amount is correctly stored as a float
        recorded_transaction = tracker.expenses[0]
        assert isinstance(recorded_transaction['amount'], float)
        assert recorded_transaction['amount'] == 50.00
        assert recorded_transaction['category'] == "food"
        assert recorded_transaction['description'] == "Grocery shopping"

    def test_record_transaction_with_float_amount(self):
        """
        Test recording a transaction with a valid float amount.

        This test covers:
        1. Attempting to record a transaction with a valid float amount
        2. Verifying that the transaction is successfully recorded
        3. Ensuring that the amount is correctly stored as a float
        """
        tracker = InvestmentTracker()

        # Attempt to record a transaction with a float amount
        result = tracker.record_transaction(50.00, "food", "Grocery shopping")

        # The method should return True as the transaction should be recorded successfully
        assert result == True

        # Verify that the transaction was added to the expenses list
        assert len(tracker.expenses) == 1

        # Check that the amount is correctly stored as a float
        recorded_transaction = tracker.expenses[0]
        assert isinstance(recorded_transaction['amount'], float)
        assert recorded_transaction['amount'] == 50.00
        assert recorded_transaction['category'] == "food"
        assert recorded_transaction['description'] == "Grocery shopping"

    def test_record_transaction_with_float_amount(self):
        """
        Test recording a transaction with a valid float amount.

        This test covers:
        1. Attempting to record a transaction with a valid float amount
        2. Verifying that the transaction is successfully recorded
        3. Ensuring that the amount is correctly stored as a float
        """
        tracker = InvestmentTracker()

        # Attempt to record a transaction with a float amount
        result = tracker.record_transaction(50.00, "food", "Grocery shopping")

        # The method should return True as the transaction should be recorded successfully
        assert result == True

        # Verify that the transaction was added to the expenses list
        assert len(tracker.expenses) == 1

        # Check that the amount is correctly stored as a float
        recorded_transaction = tracker.expenses[0]
        assert isinstance(recorded_transaction['amount'], float)
        assert recorded_transaction['amount'] == 50.00
        assert recorded_transaction['category'] == "food"
        assert recorded_transaction['description'] == "Grocery shopping"