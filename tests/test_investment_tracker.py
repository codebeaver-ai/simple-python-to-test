import pytest
from datetime import datetime
from investment_tracker import InvestmentTracker

# TODO: add more tests


class TestInvestmentTracker:
    def test_record_transaction(self):
        assert InvestmentTracker().record_transaction(100, "food", "groceries") == True
