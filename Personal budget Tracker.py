import csv
class BudgetTracker:
  def _init_(self, filename):
    self.filename = filename
    self.transactions = []
    self.load_transactions()
  def load_transactions(self):
    try:
      with open(self.filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        self.transactions = list(reader)
    except FileNotFoundError:
      pass
  def save_transactions(self):
    with open(self.filename, 'w') as csvfile:
      fieldnames = ['category', 'amount', 'type']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerows(self.transactions)
  def add_transaction(self):
    category = input("Enter transaction category (e.g., groceries, rent, salary): ")
    amount = float(input("Enter transaction amount: "))
    transaction_type = input("Enter transaction type (income/expense): ").lower()
    self.transactions.append({
      "category": category,
      "amount": amount,
      "type": transaction_type
    })
    self.save_transactions()
  def calculate_remaining_budget(self):
    total_income = sum(transaction["amount"] for transaction in self.transactions if transaction["type"] == "income")
    total_expense = sum(transaction["amount"] for transaction in self.transactions if transaction["type"] == "expense")
    return total_income - total_expense
  def display_transaction_summary(self):
    expense_categories = {}
    for transaction in self.transactions:
      if transaction["type"] == "expense":
        category = transaction["category"]
        amount = transaction["amount"]
        expense_categories.setdefault(category, 0)
        expense_categories[category] += amount
    if expense_categories:
      print("Expense Summary:")
      for category, total in expense_categories.items():
        print(f"\t{category}: {total}")
    else:
      print("No expenses recorded yet.")
budget_tracker = BudgetTracker('transactions.csv')
while True:
  print("\nBudget Tracker")
  print("1. Add Transaction")
  print("2. View Remaining Budget")
  print("3. View Expense Summary")
  print("4. Exit")
  choice = input("Enter your choice: ")
  if choice == '1':
    budget_tracker.add_transaction()
  elif choice == '2':
    remaining_budget = budget_tracker.calculate_remaining_budget()
    print(f"Remaining Budget: {remaining_budget}")
  elif choice == '3':
    budget_tracker.display_transaction_summary()
  elif choice == '4':
    print("Exiting Budget Tracker...")
    break
  else:
    print("Invalid choice. Please try again.")
