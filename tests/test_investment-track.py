import pytest
from datetime import datetime
from investment_track import Investment, Portfolio


class TestInvestment:
    @pytest.fixture
    def sample_investment(self):
        return Investment(
            symbol="AAPL",
            shares=10,
            purchase_price=150.00,
            purchase_date=datetime(2023, 1, 1),
        )

    def test_investment_creation(self, sample_investment):
        assert sample_investment.symbol == "AAPL"
        assert sample_investment.shares == 10
        assert sample_investment.purchase_price == 150.00
        assert sample_investment.purchase_date == datetime(2023, 1, 1)


class TestPortfolio:
    @pytest.fixture
    def sample_portfolio(self):
        portfolio = Portfolio()
        portfolio.add_investment(Investment("AAPL", 10, 150.00, datetime(2023, 1, 1)))
        portfolio.add_investment(Investment("GOOGL", 5, 2500.00, datetime(2023, 1, 1)))
        return portfolio

    def test_portfolio_creation(self, sample_portfolio):
        assert len(sample_portfolio.investments) == 2
