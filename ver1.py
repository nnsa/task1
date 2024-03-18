import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar
from datetime import datetime

# Створення бази даних та таблиць
def create_db():
    conn = sqlite3.connect('engine.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS oil_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            hours INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fuel_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            hours INTEGER,
            fuel_cost REAL
        )
    ''')
    conn.commit()
    conn.close()

# Функція для додавання запису про заміну масла
def add_oil_change(date, hours):
    conn = sqlite3.connect('engine.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO oil_changes (date, hours) VALUES (?, ?)', (date, hours))
    conn.commit()
    conn.close()

# Функція для розрахунку вартості масла та палива
def calculate_costs(hours, oil_price, fuel_price):
    oil_cost = (100 / 10) * (hours / 1000) * oil_price
    fuel_cost = (500 / 1000) * hours * fuel_price
    return oil_cost, fuel_cost

# Головне вікно програми
def main_app():
    root = Tk()
    root.title("Розрахунок вартості роботи двигуна")

    # Змінні для зберігання даних введених користувачем
    hours_var = StringVar()
    oil_price_var = StringVar()
    fuel_price_var = StringVar()
    oil_cost_var = StringVar()
    fuel_cost_var = StringVar()

    # Елементи інтерфейсу
    Label(root, text="Кількість мотогодин:").grid(row=0, column=0)
    Entry(root, textvariable=hours_var).grid(row=0, column=1)

    Label(root, text="Ціна за літр масла (грн):").grid(row=1, column=0)
    Entry(root, textvariable=oil_price_var).grid(row=1, column=1)

    Label(root, text="Ціна за літр палива (грн):").grid(row=2, column=0)
    Entry(root, textvariable=fuel_price_var).grid(row=2, column=1)

    Label(root, text="Вартість масла (грн):").grid(row=4, column=0)
    Label(root, textvariable=oil_cost_var).grid(row=4, column=1)

    Label(root, text="Вартість палива (грн):").grid(row=5, column=0)
    Label(root, textvariable=fuel_cost_var).grid(row=5, column=1)

    # Кнопка для розрахунку вартості
    def on_calculate():
        hours = int(hours_var.get())
        oil_price = float(oil_price_var.get())
        fuel_price = float(fuel_price_var.get())
        oil_cost, fuel_cost = calculate_costs(hours, oil_price, fuel_price)
        oil_cost_var.set(f"{oil_cost:.2f}")
        fuel_cost_var.set(f"{fuel_cost:.2f}")

    Button(root, text="Розрахувати вартість", command=on_calculate).grid(row=3, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    create_db()
    main_app()
