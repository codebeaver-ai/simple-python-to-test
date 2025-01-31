import pytest
import unittest

from datetime import datetime
from investment_tracker import InvestmentTracker

class TestInvestmentTracker(unittest.TestCase):
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True

    def test_register_new_category(self):
        """
        Test the register_new_category method of InvestmentTracker.

        This test covers:
        1. Successfully adding a new category
        2. Failing to add an existing category
        3. Raising ValueError for an invalid category
        """
        tracker = InvestmentTracker()

        # Test successful category addition
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test adding an existing category
        assert tracker.register_new_category("food") == False

        # Test adding an invalid category (empty string)
        with pytest.raises(ValueError):
            tracker.register_new_category("")