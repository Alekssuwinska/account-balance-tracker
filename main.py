from datetime import datetime

import matplotlib.pyplot as plt


class InputReader:
    def __init__(self):
        self.transactions = []

    def add_transaction(self):
        transaction = {}
        try:
            date = input("Podaj datę transakcji (RRRR-MM-DD): ")
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            if date_obj > datetime.now():
                print("Błąd: Data nie może być z przyszłości")
                return False
            transaction["date"] = date_obj
        except ValueError:
            print("Błąd: Podano niepoprawną datę")
            return False
        try:
            amount = float(
                input(
                    "Podaj kwotę transakcji (ujemna dla wydatku, dodatnia dla przychodu): "
                )
            )
            if amount == 0:
                print("Błąd: Kwota nie może być równa 0")
                return False
            transaction["amount"] = amount
        except ValueError:
            print("Błąd: Podano niepoprawną kwotę")
            return False
        self.transactions.append(transaction)
        return True

    def get_transactions(self):
        return self.transactions

    def clear_transactions(self):
        self.transactions = []
        print("Lista transakcji została wyczyszczona")


class ExpenseTracker:
    def __init__(self, input_reader):
        self.input_reader = input_reader
        self.reset_stats()

    def reset_stats(self):
        self.balance = 0
        self.num_expenses = 0
        self.num_incomes = 0
        self.lowest_balance = float("inf")
        self.lowest_balance_date = None
        self.highest_balance = float("-inf")
        self.highest_balance_date = None
        self.balance_history = []
        self.date_change = []

    def set_input_reader(self, input_reader):
        self.input_reader = input_reader
        self.reset_stats()

    def get_transaction_date(self, transaction):
        return transaction["date"]

    def get_sorted_transactions(self):
        transactions = self.input_reader.get_transactions()
        return sorted(transactions, key=self.get_transaction_date)

    def update_balance(self):
        self.reset_stats()
        sorted_transactions = self.get_sorted_transactions()

        date_balances = {}
        date_change = {}

        for transaction in sorted_transactions:
            self.balance += transaction["amount"]
            if transaction["amount"] < 0:
                self.num_expenses += 1
            else:
                self.num_incomes += 1

            current_date = transaction["date"]
            date_balances[current_date] = self.balance
            date_change[current_date] = (
                date_change.get(current_date, 0) + transaction["amount"]
            )

        if len(date_balances) > 0:
            self.lowest_balance = min(date_balances.values())
            self.lowest_balance_date = min(date_balances, key=date_balances.get)
            self.highest_balance = max(date_balances.values())
            self.highest_balance_date = max(date_balances, key=date_balances.get)

        for date, balance in date_balances.items():
            self.balance_history.append([str(date.date()), balance])

        for date, change in date_change.items():
            self.date_change.append([str(date.date()), change])

    def print_transactions(self):
        transactions = self.get_sorted_transactions()

        print("")
        if len(transactions) == 0:
            print("Brak transakcji do wyświetlenia")
        else:
            print("Lista transakcji:")
            for index, transaction in enumerate(transactions):
                print(
                    f"{index + 1}. {transaction['date'].date()}: {transaction['amount']}"
                )

    def print_stats(self):
        print("")
        print("Statystyki:")
        print(f"Aktualne saldo: {self.balance}")
        if self.lowest_balance_date is not None:
            print(
                f"Najniższe saldo: {self.lowest_balance} z dnia {self.lowest_balance_date.date()}"
            )
        if self.highest_balance_date is not None:
            print(
                f"Najwyższe saldo: {self.highest_balance} z dnia {self.highest_balance_date.date()}"
            )
        print(f"Liczba wydatków: {self.num_expenses}")
        print(f"Liczba przychodów: {self.num_incomes}")


class Visualization:
    def __init__(self, expense_tracker):
        self.expense_tracker = expense_tracker

    def plot_balance_history(self):
        balance_history = self.expense_tracker.balance_history
        if len(balance_history) == 0:
            print("Błąd: Brak danych do wyświetlenia")
            return

        dates = [item[0] for item in balance_history]
        balances = [item[1] for item in balance_history]
        plt.figure(figsize=(10, 6))
        plt.plot(dates, balances, marker="o", linestyle="-", color="b")
        plt.title("Historia salda")
        plt.xlabel("Data")
        plt.ylabel("Saldo")
        plt.grid(True)
        plt.show()

    def plot_daily_transactions(self):
        date_change = self.expense_tracker.date_change
        if len(date_change) == 0:
            print("Błąd: Brak danych do wyświetlenia")
            return

        dates = [item[0] for item in date_change]
        amounts = [item[1] for item in date_change]

        plt.figure(figsize=(10, 6))
        bars = plt.bar(dates, amounts)

        # Color bars based on amount
        for bar in bars:
            if bar.get_height() >= 0:
                bar.set_color("green")
            else:
                bar.set_color("red")

        plt.title("Dzienny bilans transakcji")
        plt.xlabel("Data")
        plt.ylabel("Kwota")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


def show_choices():
    print("")
    print("1. Dodaj transakcję")
    print("2. Wyświetl listę transakcji")
    print("3. Wyświetl statystyki")
    print("4. Wyczyść listę transakcji")
    print("5. Narysuj wykres z historii salda")
    print("6. Narysuj wykres z dziennego bilansu transakcji")
    print("7. Wyjście")


# Główna logika programu
input_reader = InputReader()
expense_tracker = ExpenseTracker(input_reader)
visualization = Visualization(expense_tracker)
choice = 0
while choice != 7:
    show_choices()
    try:
        choice = int(input("Wybierz opcję: "))
    except ValueError:
        print("Błąd: Podano niepoprawną opcję")
        continue

    if choice == 1:
        input_reader.add_transaction()
    elif choice == 2:
        expense_tracker.print_transactions()
    elif choice == 3:
        expense_tracker.update_balance()
        expense_tracker.print_stats()
    elif choice == 4:
        input_reader.clear_transactions()
        expense_tracker.reset_stats()
    elif choice == 5:
        expense_tracker.update_balance()
        visualization.plot_balance_history()
    elif choice == 6:
        expense_tracker.update_balance()
        visualization.plot_daily_transactions()
    elif choice == 7:
        exit()
