import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title('Win percentage calculation')
root.grid_columnconfigure(0, minsize=100)
root.grid_columnconfigure(1, minsize=650)
root.resizable(False, False)

def make_label(name):
    return tk.Label(root, text=name, font=('Arial', 20), anchor='w')
def make_button(name):
    return

make_label('enter the number of matches').grid(column=0, row=0, sticky='wnse')
entry_match = tk.Entry(root)
entry_match.grid(column=1, row=0, sticky='wnse', columnspan=2)

make_label('enter current wr').grid(column=0, row=1, sticky='wnse')
entry_wr = tk.Entry(root)
entry_wr.grid(column=1, row=1, sticky='wnse', columnspan=2)


entry_result = tk.Entry(root, font=('Arial', 15), justify='center')
entry_result['state'] = tk.DISABLED
entry_result.grid(column=1, row=2, sticky='wnse')

def enter():
    try:
        bar = float(entry_match.get())
        bar2 = float(entry_wr.get())
        n = bar
        n1 = bar
        n2 = bar
        n3 = bar
        n4 = bar
        n5 = bar

        p = bar2

        bar90 = 90
        bar80 = 80
        bar70 = 70
        bar60 = 60
        bar50 = 50
        second_count1 = n / 100 * p
        second_count2 = n / 100 * p
        second_count3 = n / 100 * p
        second_count4 = n / 100 * p
        second_count5 = n / 100 * p

        while (second_count1 / n1 * 100) < bar50:
            n1 += 1
            second_count1 += 1
        while (second_count2 / n2 * 100) < bar60:
            n2 += 1
            second_count2 += 1
        while (second_count3 / n3 * 100) < bar70:
            n3 += 1
            second_count3 += 1
        while (second_count4 / n4 * 100) < bar80:
            n4 += 1
            second_count4 += 1
        while (second_count5 / n5 * 100) < bar90:
            n5 += 1
            second_count5 += 1
        far1 = float(n1) - float(n)
        far2 = float(n2) - float(n)
        far3 = float(n3) - float(n)
        far4 = float(n4) - float(n)
        far5 = float(n5) - float(n)

        if far5 == 0.0:
            account5 = 'Are you an idiot? the program is not designed to count above 90 VR or you entered something wrong down'
            return result(account5)
        elif far4 == 0.0:
            account4 = 'to 90:   ' + str(far5)
            return result(account4)
        elif far3 == 0.0:
            account3 = 'to 80:   ' + str(far4) + '    to 90:   ' + str(far5)
            return result(account3)
        elif far2 == 0.0:
            account2 = 'to 70:   ' + str(far3) + '    to 80:   ' + str(far4) + '    to 90:   ' + str(far5)
            return result(account2)
        elif far1 == 0.0:
            account1 = 'to 60:   ' + str(far2) + '    to 70:   ' + str(far3) + '    to 80:   ' + str(far4) + '    to 90:   ' + str(far5)
            return result(account1)
        else:
            account = 'to 50:   ' + str(far1) + '    to 60:   ' + str(far2) + '    to 70:   ' + str(far3) + '    to 80:   ' + str(far4) + '    to 90:   ' + str(far5)
            return result(account)
    except:
           messagebox.showinfo('mistake', "you're an idiot, you did something wrong")

def result(date):
    entry_result['state'] = tk.NORMAL
    entry_result.delete(0, tk.END)
    entry_result.insert(0, date)
    entry_result['state'] = tk.DISABLED

tk.Button(text='enter', font=('Arial', 15), command=lambda: enter()) .grid(column=0, row=2, sticky='wnse')

root.mainloop()