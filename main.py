import json
import os
import math


def data_error():
    print("Error: Data file is corrupted or missing required information.")
    print("Please check 'data.json' before restarting the program.")
    exit(1)

def save_data(new_balance, expenses):
    data = {
        "balance": new_balance,
        "expenses": expenses
    }
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def load_data():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return {"balance": None, "expenses": []}
    except json.JSONDecodeError:
        return None


def show_menu():
    print("\n=== MENU ===")
    print("What would you like to do?")
    print("1. Add an expense")
    print("2. View current balance")
    print("3. View all expenses")
    print("4. View total spent")
    print("5. Add income")
    print("6. View expenses by category")
    print("7. View totals for all categories")
    print("8. View largest expense")
    print("9. View average expense")
    print("10. Exit")

def get_initial_balance():
    while True:
        try:
            balance = float(input("Enter your current balance: $"))
            if balance < 0 or not math.isfinite(balance):
                print("Error: Balance must be a valid non-negative number.")
                continue
            return balance
        except ValueError:
            print("Error: Please enter a valid number for the balance.")

def is_valid_amount(amount):
    return amount > 0 and math.isfinite(amount) and not isinstance(amount, bool)

def has_enough_balance(balance, amount):
    return balance >= amount

def show_balance(balance):
    print(f"Current balance: ${balance:.2f}")

def show_expenses(expenses):
    if not expenses:
        print("No expenses recorded yet.")
    else:
        print("All expenses:")
        for i, expense in enumerate(expenses, start=1):
            print(f"  {i}. {expense['description']}: {expense['category']}: ${expense['amount']:.2f}")

def calculate_total_expenses(expenses):
    return sum(expense['amount'] for expense in expenses)

def calculate_category_total(expenses, category):
    return sum(expense['amount'] for expense in expenses if expense['category'].lower() == category.lower())

def calculate_total_by_category(expenses):
    category_totals = {}
    for expense in expenses:
        category = expense['category'].title()
        if category in category_totals:
            category_totals[category] += expense['amount']
        else:
            category_totals[category] = expense['amount']
    return category_totals

def category_exists(expenses, category):
    return any(expense['category'].lower() == category.lower() for expense in expenses)

def show_category_total(expenses, category):
    total = calculate_category_total(expenses, category)
    print(f"Total expenses for category '{category}': ${total:.2f}")

def show_total_by_category(expenses):
    category_totals = calculate_total_by_category(expenses)
    if not category_totals:
        print("No expenses recorded yet.")
    else:
        print("Total expenses by category:")
        for category, total in category_totals.items():
            print(f"  {category}: ${total:.2f}")

def show_total_expenses(expenses):
    total = calculate_total_expenses(expenses)
    print(f"Total expenses: ${total:.2f}")

def calculate_new_balance(balance, expense):
    return balance - expense

def create_expense(description, category, amount):
    return {
        "description": description,
        "category": category,
        "amount": amount
    }

def add_expense(expenses, balance, description, category, amount):
    if not is_valid_amount(amount):
        print("Error: Expense must be a positive number.")
        return balance

    if not has_enough_balance(balance, amount):
        print("Error: Expense exceeds current balance.")
        return balance

    new_balance = calculate_new_balance(balance, amount)
    expense_data = create_expense(description, category, amount)
    expenses.append(expense_data)

    save_data(new_balance, expenses)

    print(f"Expense added: {description} - {category} - ${amount:.2f}")
    show_balance(new_balance)

    return new_balance

def get_expense_details():
 
    while True:
        description = input("Enter a description for the expense (or 'q' to quit): ")
        if description.strip().lower() == 'q':
            print("Operation cancelled. Returning to main menu.")
            return None, None, None
        if not description.strip():
            print("Error: Description cannot be empty.")
            continue

        while True:
            category = input("Enter a category for the expense (or 'q' to quit): ").title()
            if category.strip().lower() == 'q':
                print("Operation cancelled. Returning to main menu.")
                return None, None, None
            if not category.strip():
                print("Error: Category cannot be empty.")
                continue
            break
        
        while True:
            amount_input =(input("Enter the amount for the expense (or 'q' to quit): $"))
            if amount_input.strip().lower() == 'q':
                print("Operation cancelled. Returning to main menu.")
                return None, None, None
            try:
                amount = float(amount_input)
                if not is_valid_amount(amount):
                    print("Error: Expense must be a positive number.")
                    continue
                return description, category, amount
            except ValueError:
                print("Error: Please enter a valid number for the amount.")

def get_income_amount():
    while True:
        income_input = input("Enter the amount of income to add (or 'q' to quit): $")

        if income_input.strip().lower() == 'q':
            print("Operation cancelled. Returning to main menu.")
            return None

        try:
            income = float(income_input)

            if not is_valid_amount(income):
                print("Error: Income must be a positive number.")
                continue

            return income

        except ValueError:
            print("Error: Please enter a valid number for the income.")

def add_income(balance, income, expenses):
    if not is_valid_amount(income):
        print("Error: Income must be a positive number.")
        return balance
    new_balance = calculate_balance_after_income(balance, income)
    save_data(new_balance, expenses)

    print(f"Income added: ${income:.2f}")
    show_balance(new_balance)

    return new_balance

def calculate_balance_after_income(balance, income):
    return balance + income

def get_largest_expense(expenses):
    if not expenses:
        return None
    return max(expenses, key=lambda x: x['amount'])

def show_largest_expense(expenses):
    largest_expense = get_largest_expense(expenses)
    if largest_expense:
        print(f"Largest expense: {largest_expense['description']} - {largest_expense['category']} - ${largest_expense['amount']:.2f}")
    else:
        print("No expenses recorded yet.")

def calculate_average_expense(expenses):
    if not expenses:
        return 0
    total = calculate_total_expenses(expenses)
    return total / len(expenses)

def show_average_expense(expenses):
    average = calculate_average_expense(expenses)
    print(f"Average expense amount: ${average:.2f}")
    
def confirm_operation(prompt):
    while True:
        response = input(f"{prompt} (y/n/e): ").strip().lower()

        if response == 'y':
            return 'confirm'

        elif response == 'n':
            return 'cancel'

        elif response == 'e':
            return 'edit'

        else:
            print("Invalid input. Please enter 'y', 'n', or 'e'.")

def show_edit_expense_menu():
    print("\n=== EDIT EXPENSE MENU ===")
    print("1. Edit description")
    print("2. Edit category")
    print("3. Edit amount")
    print("4. Back to summary")
 

print("=== EXPENSE TRACKER ===")
print("Personal finance manager")

data = load_data()

if not isinstance(data, dict):
    data_error()


if "balance" not in data or "expenses" not in data:
    data_error()

balance = data["balance"]
expenses = data["expenses"]

if not isinstance(expenses, list):
    data_error()


for expense in expenses:

    if not isinstance(expense, dict) or "description" not in expense or "category" not in expense or "amount" not in expense:
        data_error()
    if not isinstance(expense["amount"], (int, float)) or expense["amount"] <=0 or not math.isfinite(expense["amount"]) or isinstance(expense["amount"], bool):
        data_error()


    if not isinstance(expense["description"], str) or not isinstance(expense["category"], str):
        data_error()
    if not expense["description"].strip() or not expense["category"].strip():
        data_error()




if balance is not None:
    if not isinstance(balance, (int, float)) or balance < 0 or not math.isfinite(balance) or isinstance(balance, bool):
        data_error()

if balance is None:

    if os.path.exists("data.json"):
        data_error()

    balance = get_initial_balance()
    save_data(balance, expenses)


while True:

    show_menu()

    choice = input("Enter your choice (1, 2, 3, 4, 5, 6, 7, 8, 9, or 10): ")

    if choice == '2':
        show_balance(balance)
        continue

    elif choice == '3':
        show_expenses(expenses)
        continue

    elif choice == '4':
        show_total_expenses(expenses)
        continue

    elif choice == '5':
        income = get_income_amount()

        if income is None:
            continue

        while True:
            print("\n=== INCOME SUMMARY ===")
            print(f"Income amount: ${income:.2f}")

            confirmation = confirm_operation("Confirm income")

            if confirmation == 'confirm':
                balance = add_income(balance, income, expenses)
                break

            elif confirmation == 'cancel':
                print("Operation cancelled. Returning to main menu.")
                break

            elif confirmation == 'edit':
                print("\n=== EDIT INCOME ===")
                new_income = get_income_amount()

                if new_income is not None:
                    income = new_income
        continue

    elif choice == '6':
        category = input("Enter the category to view expenses for: ").title()
        if category_exists(expenses, category):
            show_category_total(expenses, category)
        else:
            print(f"No expenses found for category '{category}'.")
        continue

    elif choice == '7':
        show_total_by_category(expenses)
        continue

    elif choice == '8':
        show_largest_expense(expenses)
        continue

    elif choice == '9':
        show_average_expense(expenses)
        continue

    elif choice == '10':
        print("Exiting the expense tracker. Goodbye!")
        break

    elif choice != '1':
        print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, 7, 8, 9, or 10.")
        continue

    description, category, amount = get_expense_details()

    if amount is None:
        continue

    while True:
        print("\n=== EXPENSE SUMMARY ===")
        print(f"Description: {description}")
        print(f"Category: {category}")
        print(f"Amount: ${amount:.2f}")

        confirmation = confirm_operation("Confirm expense")

        if confirmation == 'confirm':
            balance = add_expense(expenses, balance, description, category, amount)
            break

        elif confirmation == 'cancel':
            print("Operation cancelled. Returning to main menu.")
            break

        elif confirmation == 'edit':
            show_edit_expense_menu()
            edit_choice = input("Enter your choice (1, 2, 3, or 4): ")

            if edit_choice == '1':
                new_description = input("Enter a new description for the expense: ")
                if not new_description.strip():
                    print("Error: Description cannot be empty.")
                    continue
                description = new_description

            elif edit_choice == '2':
                new_category = input("Enter a new category for the expense: ").title()
                if not new_category.strip():
                    print("Error: Category cannot be empty.")
                    continue
                category = new_category

            elif edit_choice == '3':
                while True:
                    amount_input = input("Enter a new amount for the expense: $")
                    try:
                        new_amount = float(amount_input)
                        if not is_valid_amount(new_amount):
                            print("Error: Expense must be a positive number.")
                            continue
                        amount = new_amount
                        break
                    except ValueError:
                        print("Error: Please enter a valid number for the amount.")

            elif edit_choice == '4':
                print("Returning to expense summary.")
                continue

            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")