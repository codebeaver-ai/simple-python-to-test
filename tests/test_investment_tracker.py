import pytest
from datetime import datetime
from investment_track import record_transaction


class TestInvestment:
    def test_record_transaction(self):
        record_transaction(100, "buy", "stock", "2024-01-01")
        assert True
