
import csv
import os
from datetime import datetime
from collections import defaultdict

FILE_NAME = "expenses.csv"


def load_expenses():
    expenses = []

    if not os.path.exists(FILE_NAME):
        print(f"{FILE_NAME} not found!")
        print("Keep it in the same folder as this program.")
        return expenses

    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    expense_date = datetime.strptime(
                        row["Date"].strip(), "%Y-%m-%d"
                    )
                    amount = float(row["Amount"])

                    expenses.append({
                        "date": expense_date,
                        "category": row["Category"].strip(),
                        "amount": amount,
                        "description": row["Description"].strip()
                    })

                except (ValueError, KeyError, AttributeError):
                    print(f"Skipping invalid record: {row}")

    except (OSError, csv.Error) as error:
        print("Could not read the CSV file:", error)

    return expenses


def monthly_report(expenses):
    month = input("Enter month (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid format! Example: 2026-10")
        return

    selected = [
        expense for expense in expenses
        if expense["date"].strftime("%Y-%m") == month
    ]

    if not selected:
        print("No expenses found for this month.")
        return

    category_totals = defaultdict(float)
    total = 0

    print(f"\n===== EXPENSE REPORT: {month} =====")

    for expense in selected:
        category_totals[expense["category"]] += expense["amount"]
        total += expense["amount"]

    for expense in selected:
        print(
            f'{expense["date"].strftime("%Y-%m-%d")} | '
            f'{expense["category"]} | '
            f'Rs. {expense["amount"]:.2f} | '
            f'{expense["description"]}'
        )

    print("\n--- Category-wise Total ---")
    for category, amount in sorted(category_totals.items()):
        print(f"{category}: Rs. {amount:.2f}")

    print(f"\nTotal expenses: Rs. {total:.2f}")
    print(f"Number of transactions: {len(selected)}")
    print(f"Average expense: Rs. {total / len(selected):.2f}")


def main():
    expenses = load_expenses()

    if not expenses:
        print("No valid expense records found.")
        return

    while True:
        print("\n===== MONTHLY EXPENSE ANALYZER =====")
        print("1. View Monthly Report")
        print("2. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            monthly_report(expenses)
        elif choice == "2":
            print("Analyzer closed.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
