#Если VSCode нахуй посылает
#& C:/Users/Плотников/AppData/Local/Programs/Python/Python310/python.exe "c:/Users/Плотников/Desktop/Proekt_crm/gui.py"

import sqlite3
import datetime
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Combobox
import pandas as pd


#Содание базы данных
conn = sqlite3.connect(r'./Orders.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS Orders(
prdid INTEGER PRIMARY KEY autoincrement,
name_prod TEXT,
count INT,
datetime DATETIME,
type_prod TEXT);""")
conn.commit()
prod_name=[]

class Sklad:

    def note_bd(self, name, count, type_prod):
        self.name=name
        self.count=count
        self.type_prod=type_prod
        prd_name_mass=[]
        cur.execute("SELECT name_prod FROM Orders")
        prd_name=cur.fetchall()
        for i in prd_name:
            prd_name_mass.append(i[0])

        if name in prd_name_mass:
            if int(count)>=0:
                dtim = str(datetime.datetime.now())
                dt_now=dtim[:19]
                cur.execute(f"UPDATE Orders SET count=count+'{count}' WHERE name_prod='{name}'")
                conn.commit()
                cur.execute(f"UPDATE Orders SET datetime='{dt_now}' WHERE name_prod='{name}'")
                conn.commit()
            else:
                messagebox.showerror("Ошибка!","количество должно быть больше нуля")
        else:
            if int(count)>0:
                dtim = str(datetime.datetime.now())
                dt_now=dtim[:19]
                spis=(name, count, dt_now, type_prod)
                cur.execute("INSERT INTO Orders(name_prod, count, datetime, type_prod) VALUES(?, ?, ?, ?);", spis)
                conn.commit()
                prod_name.append(name)
            else:
                messagebox.showerror("Ошибка!","количество должно быть больше нуля")

    def database_out(self, name, count):
        self.name=name
        self.count=count
        cur.execute(f"SELECT count FROM Orders WHERE name_prod='{name}'")
        prd_count=cur.fetchone()
        for i in prd_count:
            prd_spis=[]
            prd_spis.append(i)
        int_prd_spis=prd_spis[0]
        int_prd_spis=int(prd_spis[0])
        ostatok_fakt=int_prd_spis-int(count)
        if ostatok_fakt>=0:
            cur.execute(f"UPDATE Orders SET count=count-'{count}' WHERE name_prod='{name}'")
            conn.commit()
        else:
            messagebox.showerror("Ошибка!", "Столько нет в наличии")


    
    def clicked_btn_get(self):
        cur.execute("SELECT * FROM Orders;")
        three_results = cur.fetchone()
        print(three_results)
        name=[]
        count=[]
        date_time=[]
        type_prod=[]
        for i in three_results:
            name.append(i[1])
            count.append(i[2])
            date_time.append(i[3])
            type_prod.append(i[4])

        df=pd.DataFrame({'Name':name, 'Count':count, 'Date_time':date_time, 'Type_prod':type_prod})
        df.to_excel('./Orders.xlsx')
    
    def clear_bd(self):
        cur.execute("DROP TABLE Orders;")
        conn.commit()
        cur.execute("""CREATE TABLE IF NOT EXISTS Orders(
        prdid INTEGER PRIMARY KEY autoincrement,
        name_prod TEXT,
        count INT,
        datetime DATETIME,
        type_prod TEXT);""")    
        conn.commit()

    def btn1info(self):
        name=txt1.get()
        txt1.delete(0, 'end')
        count=txt2.get()
        txt2.delete(0, 'end')
        type_prod=combo.get()
        zxc=Sklad()
        zxc.note_bd(name, count, type_prod)

    def btn2info(self):
        name=txt1.get()
        txt1.delete(0, 'end')
        count=txt2.get()
        txt2.delete(0, 'end')
        zxc=Sklad()
        zxc.database_out(name, count)

    def xlsx(self):
        name=txt1.get()
        txt1.delete(0, 'end')
        count=txt2.get()
        txt2.delete(0, 'end')
        zxc=Sklad()
        zxc.clicked_btn_get()


xyz=Sklad()
window=tk.Tk()
window.title("Склад")
window.geometry('600x400')

lbl1=Label(window, text="Наименование", font=('Arial Bold', 10))
lbl1.grid(column=0, row=0)
txt1 = Entry(window,width=15)
txt1.grid(column=1, row=0)
lbl2=Label(window, text="Количество", font=('Arial Bold', 10))
lbl2.grid(column=0, row=1)
txt2 = Entry(window,width=15)
txt2.grid(column=1, row=1)
lbl3=Label(window, text="Тип товара", font=('Arial Bold', 10))
lbl3.grid(column=0, row=2)

box_value=tk.StringVar()
combo = ttk.Combobox(textvariable=box_value)
combo["values"] = ["Овощи", "Молочная продукция", "Мясо и рыба", "Алкоголь", "Прочее"]
combo.grid(column=1, row=2)

btn1 = Button(window, text="    Привезли товар    ", command=xyz.btn1info)
btn1.grid(column=7, row=0)

btn2 = Button(window, text="    Отправили товар    ", command=xyz.btn2info)
btn2.grid(column=7, row=1)

btn3 = Button(window, text="    Очистить базу данных    ", command=xyz.clear_bd)
btn3.grid(column=8, row=0)

btn_xlsx = Button(window, text="Выгрузить в Excel", command=xyz.clicked_btn_get)
btn_xlsx.grid(column=8, row=1)

window.mainloop()