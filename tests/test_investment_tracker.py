import pytest
from investment_tracker import InvestmentTracker

import pytest 

from unittest.mock import patch
from io import StringIO

def test_register_new_category_invalid():
    tracker = InvestmentTracker()

    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.register_new_category("")

    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.register_new_category("   ")

    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.register_new_category(None)

    with pytest.raises(ValueError, match="Category must be a non-empty string"):
        tracker.register_new_category(123)

    assert "shopping" not in tracker.categories
    assert tracker.register_new_category("shopping") == True
    assert "shopping" in tracker.categories
    assert tracker.register_new_category("shopping") == False

def test_record_transaction_invalid():
    tracker = InvestmentTracker()

    with pytest.raises(ValueError, match="Amount must be a positive number"):
        tracker.record_transaction(-50, "food", "Invalid negative amount")

    with pytest.raises(ValueError, match="Amount must be a positive number"):  
        tracker.record_transaction(0, "food", "Invalid zero amount")

    with pytest.raises(ValueError, match="Amount must be a positive number"):
        tracker.record_transaction("abc", "food", "Invalid non-numeric amount")

    with pytest.raises(ValueError, match="Category must be one of:"):
        tracker.record_transaction(50, "invalid", "Invalid category")

    assert len(tracker.expenses) == 0

def test_main(monkeypatch):
    # Patch the print function to capture output
    with patch('builtins.print') as mock_print:
        mock_print.side_effect = lambda *args: print(*args, file=StringIO())

        # Call the main function
        import investment_tracker
        investment_tracker.main()

    # Get the printed output from the string buffer
    output = mock_print.mock_calls[0].args[1].getvalue().strip()

    # Assert the expected output
    assert "Total expenses: $210.50" in output

    assert "Food expenses:" in output
    assert "$25.50 - Lunch at cafe" in output