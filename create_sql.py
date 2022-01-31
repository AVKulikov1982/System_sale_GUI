import sqlite3
import os

path = f'C:\\Users\\{os.environ.get("USERNAME")}\\Desktop\\Proect_Sales\\test_sales.db'
if not os.path.exists('test_sales.db'):
    con = sqlite3.connect('test_sales.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE if not exists sales (id_sale INTEGER PRIMARY KEY, id_manager INTEGER NOT NULL,
    name TEXT NOT NULL, id_type_document INTEGER NOT NULL, cost_price INTEGER NOT NULL, payment INTEGER NOT NULL, 
    id_executor INTEGER NOT NULL, id_stage INTEGER NOT NULL, id_original INTEGER NOT NULL, date_payment Date NOT NULL, 
    code_payment TEXT NOT NULL)''')

    cur.execute('''CREATE TABLE if not exists managers (id_manager INTEGER PRIMARY KEY, name TEXT NOT NULL,
    s_name TEXT NOT NULL, department TEXT NOT NULL, login TEXT NOT NULL,  password TEXT NOT NULL)''')

    cur.execute('''CREATE TABLE if not exists executors (id_executor INTEGER PRIMARY KEY, executor TEXT NOT NULL,
    contact_person TEXT NOT NULL, phone_number TEXT NOT NULL, mail TEXT NOT NULL)''')

    cur.execute('''CREATE TABLE if not exists types_document (id_type_document INTEGER PRIMARY KEY, type_document TEXT 
    NOT NULL)''')

    cur.execute('''CREATE TABLE if not exists originals (id_original INTEGER PRIMARY KEY, original TEXT NOT NULL)''')

    cur.execute('''CREATE TABLE if not exists stages (id_stage INTEGER PRIMARY KEY, stage TEXT NOT NULL)''')

    cur.execute('''CREATE TABLE if not exists prices (id_price INTEGER PRIMARY KEY, id_executor INTEGER NOT NULL, 
    id_type_document INTEGER NOT NULL, cost_price INTEGER NOT NULL)''')

    cur.execute("INSERT INTO managers VALUES (NULL, ?, ?, ?, ?, ?)",
                ('name', 's_name', 'IT', 'admin', 'admin'))
    con.commit()
else:
    con = sqlite3.connect('test_sales.db')
    cur = con.cursor()
