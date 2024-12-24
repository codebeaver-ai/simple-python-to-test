import pytest
from datetime import datetime
from investment_tracker import record_transaction


class TestInvestmentTracker(pytest.TestCase):
    def test_record_transaction(self):
        assert record_transaction(100, "food", "groceries") == True
