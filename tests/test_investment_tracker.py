import pytest

from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    def test_record_transaction(self):
        """
        Test that a transaction can be recorded successfully.
        """
        tracker = InvestmentTracker()
        result = tracker.record_transaction(100, "food", "Grocery shopping")
        assert result == True

    def test_register_new_category(self):
        """
        Test that a new category can be registered successfully and that
        attempting to register an existing category returns False.
        """
        tracker = InvestmentTracker()

        # Test registering a new category
        result = tracker.register_new_category("savings")
        assert result == True
        assert "savings" in tracker.categories

        # Test attempting to register an existing category
        result = tracker.register_new_category("food")
        assert result == False

        # Test that category names are case-insensitive
        result = tracker.register_new_category("ENTERTAINMENT")
        assert result == False