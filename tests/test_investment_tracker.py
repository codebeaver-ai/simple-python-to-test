import pytest

from investment_tracker import InvestmentTracker

class TestInvestmentTracker:
    """Tests for the InvestmentTracker class."""

    def test_new_category_and_compute_sum(self):
        """
        Test registering a new category 'health' and verifying:
        - Attempting to record a transaction in an unregistered category raises a ValueError.
        - Registering a new category returns True.
        - Attempting to register a duplicate category returns False.
        - Transactions recorded under the new category sum to the expected total.
        """
        tracker = InvestmentTracker()

        # Attempt to record a transaction with an unregistered category; should raise ValueError.
        with pytest.raises(ValueError):
            tracker.record_transaction(50, "health", "Gym membership")

        # Register the new category 'health'
        result = tracker.register_new_category("health")
        assert result is True, "Expected registering new category 'health' to return True."

        # Register duplicate category should return False.
        duplicate_result = tracker.register_new_category("health")
        assert duplicate_result is False, "Expected registering duplicate category 'health' to return False."

        # Record transactions under the newly registered category 'health'
        tracker.record_transaction(50, "health", "Gym membership")
        tracker.record_transaction(25, "health", "Yoga class")

        # Compute total spending for 'health'; should equal 75.
        health_total = tracker.compute_category_sum("health")
        assert health_total == 75, "Expected computed sum for 'health' to be 75."