import sqlite3 as sq
import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime

# создание двух таблиц в базе даных
con = sq.connect("../engine.db")
cur = con.cursor()
cur.execute("""
        CREATE TABLE IF NOT EXISTS oil_changes (
        id INTEGER PRIMARY KEY,
        dates TEXT,
        hours INTEGER
        )
        """)
cur.execute(""" 
        CREATE TABLE IF NOT EXISTS fuel_expenses (
        id INTEGER PRIMARY KEY,
        dates TEXT,
        hours INTEGER,
        oil_cost REAL,
        fuel_cost REAL
        )
        """)
con.commit()
con.close()

root = tk.Tk()
root.title("Розрахунок вартості роботи двигуна")
root.geometry("710x500+450+150")

root.grid_columnconfigure(0, minsize=100)
root.grid_columnconfigure(1, minsize=100)
root.grid_columnconfigure(2, minsize=100)
root.grid_columnconfigure(3, minsize=100)
root.grid_columnconfigure(4, minsize=100)
root.grid_rowconfigure(0, minsize=100)
root.grid_rowconfigure(1, minsize=100)
root.grid_rowconfigure(2, minsize=100)
root.grid_rowconfigure(3, minsize=100)
root.grid_rowconfigure(4, minsize=100)
root.grid_anchor('nw')   #grid # размеры кнопок и прочего

#создание лейблов
def make_label(name):
    return tk.Label(root, text=name, font=('Arial', 20), anchor='w')

make_label('введіть мотогодини').grid(column=0, row=0, sticky='wnse')
entry_hrs = tk.Entry(root)
entry_hrs.grid(column=1, row=0, sticky='wnse', columnspan=2)

make_label('введіть ціну за літр палива').grid(column=0, row=1, sticky='wnse')
entry_fuel_cost = tk.Entry(root)
entry_fuel_cost.grid(column=1, row=1, sticky='wnse', columnspan=2)

make_label('введіть ціну за літр масла').grid(column=0, row=2, sticky='wnse')
entry_oil_cost = tk.Entry(root)
entry_oil_cost.grid(column=1, row=2, sticky='wnse', columnspan=2)

make_label('введіть дату заміни масла').grid(column=0, row=3, sticky='wnse')
entry_date = tk.Entry(root)
entry_date.grid(column=1, row=3, sticky='wnse', columnspan=2)

make_label('загальна вартість витрат:').grid(column=3, row=2, sticky='wnse')
entry_total = tk.Entry(root, font=('Arial', 20), justify='right')
entry_total.insert(0, '0')
entry_total['state'] = tk.DISABLED
entry_total.grid(column=3, row=3, sticky='wnse')

make_label('день останньої заміни олії').grid(column=3, row=0, sticky='wnse')
entry_last_date = tk.Entry(root, font=('Arial', 20), justify='center')
# установка последней даты в окно при открытие
con_ = sq.connect("../engine.db")
cursor = con_.cursor()
cursor.execute('SELECT count(id) FROM oil_changes')
cnt = cursor.fetchall()
cursor.execute('SELECT dates FROM oil_changes')
days_befor = cursor.fetchmany(int(cnt[0][0])-1)
last_date = cursor.fetchone()
con_.close()
try:
    entry_last_date.insert(0, last_date[0])
except:
    entry_last_date.insert(0, '00-00-0000')
entry_last_date['state'] = tk.DISABLED
entry_last_date.grid(column=3, row=1, sticky='wnse')  # entry и вызов лейблов

#создание кнопок
def make_operation_button(name):
    return tk.Button(text=name, font=('Arial', 15), command=a[name])

# форматирование времени
def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d-%m-%Y')
    except ValueError:
        raise ValueError("Дата не відповідає формату dd-mm-yyyy")
    return date_obj.strftime('%d-%m-%Y')

#ввод даных в базу
def add_to_db(funk1, funk2, funk3, funk4):
    conn = sq.connect("../engine.db")
    curs = conn.cursor()
    curs.execute('INSERT INTO oil_changes (dates, hours) VALUES (?, ?)', (funk1, funk2))
    curs.execute('INSERT INTO fuel_expenses (dates, hours , fuel_cost, oil_cost) VALUES (?, ?, ?, ?)', (funk1, funk2, funk3, funk4))
    conn.commit()
    conn.close()

# збор и проверка даных
def enter():
    bar1 = entry_date.get()
    bar2 = entry_hrs.get()
    bar3 = entry_fuel_cost.get()
    bar4 = entry_oil_cost.get()
    formatted_date = format_date(bar1)
    for i in [bar2, bar3, bar4]:
        for j in i:
            if j.isdigit() or j == '.':
                pass
            else:
                entry_date.delete(0, tk.END)
                entry_hrs.delete(0, tk.END)
                entry_fuel_cost.delete(0, tk.END)
                entry_oil_cost.delete(0, tk.END)
                messagebox.showinfo('ошибка', 'ввели не правильне число')
                break
    return add_to_db(formatted_date, bar2, bar3, bar4), change_last_day(bar1)

# подсчеты загальной вартості витрат
oil_consumption = 100
fuel_consumption = 500
def total():        #тут подсчет цены
    far1 = float(entry_oil_cost.get())
    far2 = float(entry_hrs.get())
    far3 = float(entry_fuel_cost.get())
    entry_total['state'] = tk.NORMAL
    entry_total.delete(0, tk.END)
    entry_total.insert(0,  (oil_consumption / 10) * (far1 / 1000) * far2 + (fuel_consumption / 1000) * far3 * far2)
    entry_total['state'] = tk.DISABLED

# функция для кнопки сегодняшняя дата
def present_day():
    entry_date.delete(0, tk.END)
    entry_date.insert(0, str(time.localtime().tm_mday) + '-0' + str(time.localtime().tm_mon) + '-' + str(time.localtime().tm_year))

# функция для смены последнего дня смены масла
def change_last_day(date):
    entry_last_date['state'] = tk.NORMAL
    entry_last_date.delete(0, tk.END)
    entry_last_date.insert(0, date)
    entry_last_date['state'] = tk.DISABLED

# Вызовы кнопок
a = {'ввести': enter, 'Сьогоднішня дата': present_day, 'розрахувати': total}
make_operation_button('ввести').grid(column=1, row=4, sticky='wnse', columnspan=2)
make_operation_button('розрахувати').grid(column=3, row=4, sticky='wnse')
make_operation_button('Сьогоднішня дата').grid(column=0, row=4, sticky='wnse')

root.mainloop()
