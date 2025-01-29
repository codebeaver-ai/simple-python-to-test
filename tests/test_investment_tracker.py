import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from investment_tracker import InvestmentTracker


class TestInvestment:
    def test_record_transaction(self):
        """
        Test that recording a valid transaction returns True.
        This test checks if the record_transaction method correctly
        adds a new expense and returns True for a valid input.
        """
        tracker = InvestmentTracker()
        assert tracker.record_transaction(100, "food", "groceries") == True
