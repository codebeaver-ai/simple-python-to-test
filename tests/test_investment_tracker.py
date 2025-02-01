import pytest

from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    """Test suite for the InvestmentTracker class.

    This test ensures that a transaction is correctly recorded after registering
    a new category.
    """

    def test_record_transaction(self):
        tracker = InvestmentTracker()
        # First register the new category "buy" which is not among the default ones.
        registered = tracker.register_new_category("buy")
        assert registered is True

        # Record a transaction using the newly registered category.
        result = tracker.record_transaction(100, "buy", "stock")
        assert result is True

        # Verify that the expense list now contains one transaction.
        assert len(tracker.expenses) == 1

    """Test suite for the InvestmentTracker class."""

    def test_record_transaction(self):
        tracker = InvestmentTracker()
        # First register the new category "buy" which is not among the default ones.
        registered = tracker.register_new_category("buy")
        assert registered is True

        # Record a transaction using the newly registered category.
        result = tracker.record_transaction(100, "buy", "stock")
        assert result is True

        # Verify that the expense list now contains one transaction.
        assert len(tracker.expenses) == 1

    def test_invalid_inputs_and_empty_spending(self):
        """
        Test for various invalid inputs and edge cases:
        - Recording a transaction with negative amount.
        - Using an invalid category in record_transaction, filter_by_category, and compute_category_sum.
        - Registering an invalid new category.
        - Calculating overall spending with no transactions.
        """
        tracker = InvestmentTracker()

        # Overall spending without any transactions should be zero.
        assert tracker.calculate_overall_spending() == 0

        # Test recording a transaction with a negative amount.
        with pytest.raises(ValueError):
            tracker.record_transaction(-10, "food", "Negative expense")

        # Test recording a transaction with zero amount.
        with pytest.raises(ValueError):
            tracker.record_transaction(0, "food", "Zero expense")

        # Test recording a transaction with an invalid category.
        with pytest.raises(ValueError):
            tracker.record_transaction(10, "invalid_category", "Invalid category expense")

        # Test filter_by_category with an invalid category.
        with pytest.raises(ValueError):
            tracker.filter_by_category("invalid_category")

        # Test compute_category_sum with an invalid category.
        with pytest.raises(ValueError):
            tracker.compute_category_sum("invalid_category")

        # Test registering an invalid new category (empty/whitespace).
        with pytest.raises(ValueError):
            tracker.register_new_category("   ")

        # Test registering a duplicate category returns False.
        duplicate_result = tracker.register_new_category("food")
        assert duplicate_result is False

        # Add a valid transaction and verify the computed sum.
        tracker.record_transaction(20.0, "entertainment", "Movie ticket")
        tracker.record_transaction(30.0, "entertainment", "Concert ticket")
        category_sum = tracker.compute_category_sum("entertainment")
        assert category_sum == 50.0

        # Filtering should return two records for entertainment.
        filtered_expenses = tracker.filter_by_category("entertainment")
        assert len(filtered_expenses) == 2