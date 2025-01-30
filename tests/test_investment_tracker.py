import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from investment_tracker import InvestmentTracker

class TestInvestment:
    def test_record_transaction(self):
        """
        Test that the record_transaction method returns True when a valid transaction is recorded.
        """
        tracker = InvestmentTracker()
        assert tracker.record_transaction(100, "food", "groceries") == True
