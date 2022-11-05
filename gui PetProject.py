#Если VSCode нахуй посылает
#& C:/Users/Плотников/AppData/Local/Programs/Python/Python310/python.exe "c:/Users/Плотников/Desktop/Proekt_crm/gui PetProject.py"

import sqlite3
import datetime
from tkinter import *
import pandas as pd


#Содание базы данных
my_file = open("Orders.db", "w+")
#conn = sqlite3.connect(r'C:\Users\Плотников\Desktop\Proekt_crm\Orders.db')
conn = sqlite3.connect(r'./Orders.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS Orders(
prdid INTEGER PRIMARY KEY autoincrement,
name_prod TEXT,
count INT,
datetime TEXT);""")
conn.commit()
prod_name=[]

class Sklad:

    def note_bd(self, name, count):
        self.name=name
        self.count=count

        prod_name_slov={}

        if name in prod_name:
            cur.execute(f"UPDATE Orders SET count=count+'{count}' WHERE name_prod='{name}'")
            conn.commit()
        else:
            dtim = str(datetime.datetime.now())
            dt_now=dtim[:19]
            prod_name_slov[name]=int(count)
            spis=(name, count, dt_now)
            cur.execute("INSERT INTO Orders(name_prod, count, datetime) VALUES(?, ?, ?);", spis)
            conn.commit()
            prod_name.append(name)

    def database_out(self, name, count):
        self.name=name
        self.count=count
        cur.execute(f"UPDATE Orders SET count=count-'{count}' WHERE name_prod='{name}'")
        conn.commit()
    
    def clicked_btn_get(self):
        cur.execute("SELECT * FROM Orders;")
        three_results = cur.fetchall()
        name=[]
        count=[]
        date_time=[]
        for i in three_results:
            name.append(i[1])
            count.append(i[2])
            date_time.append(i[3])

        df=pd.DataFrame({'Name':name, 'Count':count, 'Date_time':date_time})
        df.to_excel('./Orders.xlsx')

        

    def clicked_btn1(self):
        def clicked_1():
            lbl1.grid_forget()
            txt1.grid_forget()
            lbl2.grid_forget()
            txt2.grid_forget()
            btn_ok.grid_forget()
    
        def info():
            name=txt1.get()
            txt1.delete(0, 'end')
            count=txt2.get()
            txt2.delete(0, 'end')
            zxc=Sklad()
            zxc.note_bd(name, count)
        
        def xlsx():
            name=txt1.get()
            txt1.delete(0, 'end')
            count=txt2.get()
            txt2.delete(0, 'end')
            zxc=Sklad()
            zxc.clicked_btn_get()
    
        lbl1=Label(window, text="Наименование", font=('Arial Bold', 10))
        lbl1.grid(column=0, row=4)
        txt1 = Entry(window,width=15)
        txt1.grid(column=1, row=4)
        lbl2=Label(window, text="Количество", font=('Arial Bold', 10))
        lbl2.grid(column=0, row=5)
        txt2 = Entry(window,width=15)  
        txt2.grid(column=1, row=5)
        btn_ok = Button(window, text="Ok", command=info)
        btn_ok.grid(column=3, row=6)
        btn_xlsx = Button(window, text="Выгрузить в Excel", command=xlsx)
        btn_xlsx.grid(column=3, row=7)

    def clicked_btn2(self):
        def clicked_2():
            lbl1.grid_forget()
            txt1.grid_forget()
            lbl2.grid_forget()
            txt2.grid_forget()
            btn_ok.grid_forget()
    
        def info():
            name=txt1.get()
            txt1.delete(0, 'end')
            count=txt2.get()
            txt2.delete(0, 'end')
            zxc=Sklad()
            zxc.database_out(name, count)

        def xlsx():
            name=txt1.get()
            txt1.delete(0, 'end')
            count=txt2.get()
            txt2.delete(0, 'end')
            zxc=Sklad()
            zxc.clicked_btn_get()
    
        lbl1=Label(window, text="Наименование", font=('Arial Bold', 10))
        lbl1.grid(column=0, row=4)
        txt1 = Entry(window,width=15)
        txt1.grid(column=1, row=4)
        lbl2=Label(window, text="Количество", font=('Arial Bold', 10))
        lbl2.grid(column=0, row=5)
        txt2 = Entry(window,width=15)  
        txt2.grid(column=1, row=5)
        btn_ok = Button(window, text="Ok", command=info)
        btn_ok.grid(column=3, row=6)
        btn_xlsx = Button(window, text="Выгрузить в Excel", command=xlsx)
        btn_xlsx.grid(column=3, row=7)

xyz=Sklad()
window=Tk()
window.title("Склад")
window.geometry('400x300')

lbl=Label(window, text="Выберите действие:", font=('Arial Bold', 10))
lbl.grid(column=0, row=0)

btn1 = Button(window, text="    Привезли товар    ", command=xyz.clicked_btn1)
btn1.grid(column=0, row=1)

btn2 = Button(window, text="    Отправили товар    ", command=xyz.clicked_btn2)
btn2.grid(column=1, row=1)

window.mainloop()