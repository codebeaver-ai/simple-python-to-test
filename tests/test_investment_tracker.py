import unittest
from datetime import datetime
from investment_tracker import InvestmentTracker


class TestInvestmentTracker(unittest.TestCase):
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
        tracker = InvestmentTracker()

        # Test registering a new category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test registering an existing category
        assert tracker.register_new_category("savings") == False

        # Test registering with invalid input
        with pytest.raises(ValueError):
            tracker.register_new_category("")

        with pytest.raises(ValueError):
            tracker.register_new_category(123)
