import sqlite3
import tkinter as tk
from tkinter import ttk


# Функція для виконання SQL запиту та отримання результатів
def fetch_data():
    conn = sqlite3.connect('vehicle_maintenance.db')
    cursor = conn.cursor()
    query = """
    SELECT 
        id AS 'ID',
        hours AS 'Мотогодини',
        oil_change_date AS 'Дата заміни мастила',
        oil_price AS 'Ціна за літр мастила',
        fuel_price AS 'Ціна за літр палива',
        oil_consumption AS 'Розхід мастила (грам/10 годин)',
        fuel_consumption AS 'Розхід палива (грам/годину)',
        (oil_consumption / 10 * hours) * (oil_price / 1000) AS 'Вартість мастила',
        (fuel_consumption * hours) / 1000 * fuel_price AS 'Вартість палива',
        ((oil_consumption / 10 * hours) * (oil_price / 1000)) + ((fuel_consumption * hours) / 1000 * fuel_price) AS 'Загальна вартість'
    FROM 
        maintenance
    ORDER BY 
        id DESC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows


# Функція для створення GUI
def create_gui(data):
    root = tk.Tk()
    root.title('Звіт по витратах на мастило та паливо')

    # Створення таблиці для виведення даних
    columns = ('ID', 'Мотогодини', 'Дата заміни мастила', 'Ціна за літр мастила', 'Ціна за літр палива',
               'Розхід мастила (грам/10 годин)', 'Розхід палива (грам/годину)', 'Вартість мастила',
               'Вартість палива', 'Загальна вартість')
    tree = ttk.Treeview(root, columns=columns, show='headings')

    # Налаштування заголовків таблиці
    for col in columns:
        tree.heading(col, text=col)

    # Додавання даних у таблицю
    for row in data:
        tree.insert('', tk.END, values=row)

    tree.pack(expand=True, fill='both')

    root.mainloop()


# Отримання даних з бази даних
data = fetch_data()

# Створення та запуск GUI
create_gui(data)
