class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.categories = set(
            ["food", "transport", "utilities", "entertainment", "other"]
        )

    def add_expense(self, amount, category, description):
        """Add a new expense to the tracker."""
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be a positive number")

        if category.lower() not in self.categories:
            raise ValueError(f"Category must be one of: {', '.join(self.categories)}")

        expense = {
            "amount": amount,
            "category": category.lower(),
            "description": description,
        }
        self.expenses.append(expense)
        return True

    def get_total_expenses(self):
        """Calculate total expenses."""
        return sum(expense["amount"] for expense in self.expenses)

    def get_expenses_by_category(self, category):
        """Get all expenses for a specific category."""
        if category.lower() not in self.categories:
            raise ValueError(f"Category must be one of: {', '.join(self.categories)}")

        return [
            expense
            for expense in self.expenses
            if expense["category"] == category.lower()
        ]

    def get_category_total(self, category):
        """Get total expenses for a specific category."""
        if category.lower() not in self.categories:
            raise ValueError(f"Category must be one of: {', '.join(self.categories)}")

        return sum(
            expense["amount"]
            for expense in self.expenses
            if expense["category"] == category.lower()
        )

    def add_category(self, category):
        """Add a new expense category."""
        if not isinstance(category, str) or not category.strip():
            raise ValueError("Category must be a non-empty string")

        category = category.lower().strip()
        if category in self.categories:
            return False

        self.categories.add(category)
        return True


def main():
    # Example usage
    tracker = ExpenseTracker()

    # Add some sample expenses
    tracker.add_expense(25.50, "food", "Lunch at cafe")
    tracker.add_expense(35.00, "transport", "Uber ride")
    tracker.add_expense(150.00, "utilities", "Electricity bill")

    # Print total expenses
    print(f"Total expenses: ${tracker.get_total_expenses():.2f}")

    # Print food expenses
    food_expenses = tracker.get_expenses_by_category("food")
    print("\nFood expenses:")
    for expense in food_expenses:
        print(f"${expense['amount']:.2f} - {expense['description']}")


if __name__ == "__main__":
    main()
