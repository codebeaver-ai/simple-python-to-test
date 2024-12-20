import pytest
from datetime import datetime
from expense_tracker import record_transaction


class TestExpenseTracker:
    def test_record_transaction(self):
        assert record_transaction(100, "food", "groceries") == True
