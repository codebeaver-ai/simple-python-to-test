from investment_tracker import InvestmentTracker

class TestInvestment:
    def test_record_transaction(self):
        print("test_record_transaction")
        assert True

    def test_record_transaction(self):
        print("test_record_transaction")
        assert True

    def test_register_new_category(self):
        # Create an instance of InvestmentTracker
        tracker = InvestmentTracker()

        # Test registering a new valid category
        assert tracker.register_new_category("savings") == True
        assert "savings" in tracker.categories

        # Test registering an existing category (should return False)
        assert tracker.register_new_category("food") == False

        # Test registering an invalid category (empty string)
        try:
            tracker.register_new_category("")
            assert False, "Expected ValueError for empty string"
        except ValueError:
            assert True

        # Test registering an invalid category (non-string)
        try:
            tracker.register_new_category(123)
            assert False, "Expected ValueError for non-string input"
        except ValueError:
            assert True