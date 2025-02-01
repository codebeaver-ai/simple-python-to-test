import pytest
from investment_tracker import InvestmentTracker


class TestInvestment:
    """Tests for the InvestmentTracker class's record_transaction functionality."""
    
    def test_record_transaction(self):
        """Test that a valid transaction is recorded correctly."""
        tracker = InvestmentTracker()
        
        # Record a valid expense transaction
        result = tracker.record_transaction(20.00, "food", "Test expense")
        assert result is True, "record_transaction should return True for a valid transaction."
        
        # Verify that the expense is correctly added
        assert len(tracker.expenses) == 1, "There should be exactly one expense recorded."
        expense = tracker.expenses[0]
        assert expense["amount"] == 20.00, "The expense amount must match the recorded value."
        assert expense["category"] == "food", "The expense category must be stored in lowercase."
        assert expense["description"] == "Test expense", "The expense description must match the input."
