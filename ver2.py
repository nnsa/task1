import sqlite3
from tkinter import *
from tkinter import messagebox

# Підключення до бази даних SQLite
conn = sqlite3.connect('vehicle_maintenance.db')
c = conn.cursor()

# Створення таблиці, якщо вона ще не існує
c.execute('''
    CREATE TABLE IF NOT EXISTS maintenance (
        id INTEGER PRIMARY KEY,
        hours INTEGER,
        oil_change_date TEXT,
        oil_price REAL,
        fuel_price REAL,
        oil_consumption REAL,
        fuel_consumption REAL
    )
''')

# Функції для розрахунків
def calculate_oil_cost(hours, oil_price, oil_consumption):
    return (oil_consumption / 10 * hours) * (oil_price / 1000)

def calculate_fuel_cost(hours, fuel_price, fuel_consumption):
    return (fuel_consumption * hours) / 1000 * fuel_price

# Функція для введення даних
def insert_data(hours, oil_change_date, oil_price, fuel_price, oil_consumption, fuel_consumption):
    c.execute('''
        INSERT INTO maintenance (hours, oil_change_date, oil_price, fuel_price, oil_consumption, fuel_consumption)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (hours, oil_change_date, oil_price, fuel_price, oil_consumption, fuel_consumption))
    conn.commit()

# Функція для виведення результатів
def show_costs():
    c.execute('SELECT * FROM maintenance ORDER BY id DESC LIMIT 1')
    last_entry = c.fetchone()
    hours, oil_change_date, oil_price, fuel_price, oil_consumption, fuel_consumption = last_entry[1], last_entry[2], last_entry[3], last_entry[4], last_entry[5], last_entry[6]
    oil_cost = calculate_oil_cost(hours, oil_price, oil_consumption)
    fuel_cost = calculate_fuel_cost(hours, fuel_price, fuel_consumption)
    total_cost = oil_cost + fuel_cost
    messagebox.showinfo("Вартість витрат", f"Вартість мастила: {oil_cost:.2f}\nВартість палива: {fuel_cost:.2f}\nЗагальна вартість: {total_cost:.2f}")

# Графічний інтерфейс користувача
root = Tk()
root.title("Розрахунок витрат на обслуговування")

# Описи полів вводу
Label(root, text="Кількість мотогодин:").pack()
hours_entry = Entry(root)
hours_entry.pack()

Label(root, text="Дата останньої заміни мастила:").pack()
oil_change_date_entry = Entry(root)
oil_change_date_entry.pack()

Label(root, text="Ціна за літр мастила:").pack()
oil_price_entry = Entry(root)
oil_price_entry.pack()

Label(root, text="Ціна за літр палива:").pack()
fuel_price_entry = Entry(root)
fuel_price_entry.pack()

Label(root, text="Розхід мастила за паспортом (грам/10 годин):").pack()
oil_consumption_entry = Entry(root)
oil_consumption_entry.pack()

Label(root, text="Розхід палива за паспортом (грам/годину):").pack()
fuel_consumption_entry = Entry(root)
fuel_consumption_entry.pack()

submit_button = Button(root, text="Ввести дані", command=lambda: insert_data(
    int(hours_entry.get()),
    oil_change_date_entry.get(),
    float(oil_price_entry.get()),
    float(fuel_price_entry.get()),
    float(oil_consumption_entry.get()),
    float(fuel_consumption_entry.get())
))
submit_button.pack()

show_button = Button(root, text="Показати витрати", command=show_costs)
show_button.pack()

root.mainloop()
