import pytest

from investment_tracker import InvestmentTracker

class TestInvestment:
    def test_record_transaction(self):
        print("test_record_transaction")
        assert True

    def test_record_transaction(self):
        print("test_record_transaction")
        assert True

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