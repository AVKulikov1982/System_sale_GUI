import datetime
import pandas as pd
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from create_sql import cur
from tkcalendar import DateEntry


class StartWindow:
	def __init__(self, results=None, width:int=250, height:int=150,
				 title:str='Start_system_sales', c_rows:int=4, c_columns:int=2, params=None):
		self.root = Tk()
		self.title = title
		self.root.title(self.title)
		if results:
			self.results = results
		else:
			self.results = []
		if params is None: self.params = {'padx': 5, 'pady': 5}
		self.width = width
		self.height = height
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()
		x_coordinate = int((screen_width / 2) - (self.width / 2))
		y_coordinate = int((screen_height / 2) - (self.height / 2))
		self.root.geometry("{}x{}+{}+{}".format(self.width, self.height, x_coordinate, y_coordinate))
		self.root.resizable(False, False)
		self.c_rows = c_rows
		self.c_columns = c_columns
		for column in range(self.c_columns):
			self.root.grid_columnconfigure(column, weight=1)
		for row in range(self.c_rows):
			self.root.grid_rowconfigure(row, weight=1)
		self.root.protocol('WM_DELETE_WINDOW', lambda: self.closing_procedure())
		self.entry_login = Entry(self.root)
		self.entry_password = Entry(self.root, show='*')

	def get_registration(self):
		login = self.entry_login.get()
		password = self.entry_password.get()
		try:
			if cur.execute("SELECT login FROM managers WHERE login=?", (login,)).fetchall():
				cur.execute("SELECT password, id_manager FROM managers WHERE login=?", (login,))
				row = cur.fetchall()
				test_password = row[0][0]
				id_manager = row[0][1]
				if login == 'admin' and test_password == password:
					self.root.destroy()
					admin_window = AdminWindow(results=self.results, id_manager=id_manager)
					admin_window.run()
				elif test_password == password:
					self.root.destroy()
					user_window = UserWindow(results=self.results, id_manager=id_manager)
					user_window.run()
				else:
					messagebox.showerror('Error', 'Password неверный')
			else:
				raise ValueError
		except ValueError:
			messagebox.showerror('Error', 'Login неверный')

	def draw_widgets(self):
		Label(self.root, text='Login').grid(row=0, column=0, sticky=W, **self.params)
		self.entry_login.grid(row=0, column=1, sticky=W + E, **self.params)
		Label(self.root, text='Password').grid(row=1, column=0, sticky=W, **self.params)
		self.entry_password.grid(row=1, column=1, sticky=W + E, **self.params)
		Button(self.root, text='Войти', command=self.get_registration).grid(row=3, column=1, sticky=W + E,
																			**self.params)

	def run(self):
		self.draw_widgets()
		self.root.mainloop()

	def closing_procedure(self):
		if datetime.datetime.time(datetime.datetime.now()) < datetime.time(18, 0, 0):
			messagebox.showinfo('Message', 'Приложение закрывается автоматически\nВы можете свернуть приложение')
		else:
			self.root.destroy()


class UserWindow(StartWindow):
	def __init__(self, results, id_manager, width=460, height=300, title='user_window', c_rows=7, c_columns=3):
		super().__init__(results, width, height, title, c_rows, c_columns)
		self.id_manager = id_manager
		self.entry_stage = Combobox(self.root,
									values=[stage[0] for stage in
											cur.execute("SELECT stage FROM stages").fetchall()],
									state='readonly', width=24)
		self.entry_id_sale = Entry(self.root, width=27)
		self.entry_name = Entry(self.root, width=27)
		self.entry_type_document = Combobox(self.root,
											values=[stage[0] for stage in
													cur.execute("SELECT type_document FROM types_document").fetchall()],
											state='readonly', width=24, height=20)
		self.frame_date = Frame(self.root)
		self.cal_data_from = DateEntry(self.frame_date, width=7, borderwidth=5, year=2021)
		self.cal_data_to = DateEntry(self.frame_date, width=7, borderwidth=5, year=2021)

		self.entry_date = Entry(self.root, width=27)
		self.entry_date.insert(0, 'пока не реализовано')

		self.entry_original = Combobox(self.root,
									   values=[original[0] for original in
											   cur.execute("SELECT original FROM originals").fetchall()],
									   state='readonly', width=24, height=20)

	def draw_widgets(self):
		Button(self.root, text='Добавить сделку', command=self.add_sale, width=22). \
			grid(row=0, column=0, sticky=W + E, **self.params)
		if self.results:
			Label(self.root, text='Есть платежи', bg='green').grid(row=0, column=1, sticky=W + E, **self.params)
			Button(self.root, text='Посмотреть новые сделки', command=self.choice_sale_for_add, width=22). \
				grid(row=0, column=2, sticky=W + E, **self.params)
		Button(self.root, text='Редактировать сделку', command=self.update_sale, width=22). \
			grid(row=1, column=0, sticky=W + E, **self.params)
		Label(self.root, text='По номеру').grid(row=1, column=1, sticky=W, **self.params)
		self.entry_id_sale.grid(row=1, column=2, sticky=W + E, **self.params)
		Label(self.root, text='По имени').grid(row=2, column=1, sticky=W, **self.params)
		self.entry_name.grid(row=2, column=2, sticky=W + E, **self.params)
		Label(self.root, text='По дате').grid(row=3, column=1, sticky=W, **self.params)
		self.frame_date.grid(row=3, column=2, sticky=W + E + N + S, **self.params)
		Label(self.frame_date, text='C').pack(side=LEFT, padx=2)
		self.cal_data_from.pack(side=LEFT, padx=2)
		Label(self.frame_date, text='По').pack(side=LEFT, padx=2)
		self.cal_data_to.pack(side=LEFT, padx=2)
		Label(self.root, text='По типу док-та').grid(row=4, column=1, sticky=W, **self.params)
		self.entry_type_document.grid(row=4, column=2, sticky=W + E, **self.params)
		Button(self.root, text='Сформировать ведомость', command=self.create_payroll, width=22). \
			grid(row=5, column=0, sticky=W + E, **self.params)
		Label(self.root, text='По этапу: ').grid(row=5, column=1, sticky=W, **self.params)
		self.entry_stage.grid(row=5, column=2, sticky=W + E, **self.params)
		Label(self.root, text='По оригиналу: ').grid(row=6, column=1, sticky=W, **self.params)
		self.entry_original.grid(row=6, column=2, sticky=W + E, **self.params)

	def add_sale(self):
		self.root.destroy()
		self.results = None
		add_sale = AddSale(results=self.results, id_manager=self.id_manager)
		add_sale.run()

	def choice_sale_for_add(self):
		self.root.destroy()
		height = 35 * (len(self.results) + 4)
		choice_sale_for_add = ChoiceSaleForAdd(results=self.results, id_manager=self.id_manager,
											   c_rows=len(self.results), height=height,
											   rows=self.results)
		choice_sale_for_add.run()

	def update_sale(self):
		id_sale = self.entry_id_sale.get()
		name = self.entry_name.get()
		type_document = self.entry_type_document.get()
		date_from = self.cal_data_from.get()
		date_from = datetime.datetime.strptime(date_from, '%m/%d/%y').strftime('%Y-%m-%d')
		date_to = self.cal_data_to.get()
		date_to = datetime.datetime.strptime(date_to, '%m/%d/%y').strftime('%Y-%m-%d')

		try:
			if cur.execute('SELECT count(*) FROM types_document').fetchall()[0][0] != 0 and \
					cur.execute('SELECT count(*) FROM stages').fetchall()[0][0] != 0 and \
					cur.execute('SELECT count(*) FROM originals').fetchall()[0][0] != 0 and \
					cur.execute('SELECT count(*) FROM executors').fetchall()[0][0] != 0:

				if id_sale and cur.execute("SELECT count(*) FROM sales").fetchone()[0] >= int(id_sale):
					rows = cur.execute(f"SELECT sales.id_sale, sales.name, sales.cost_price, sales.payment, "
									   f"types_document.type_document, executors.executor, stages.stage, "
									   f"originals.original, sales.date_payment FROM sales INNER JOIN "
									   f"types_document on sales.id_type_document = types_document.id_type_document "
									   f"INNER "
									   f"JOIN stages on sales.id_stage = stages.id_stage INNER JOIN originals on "
									   f"sales.id_original = originals.id_original INNER JOIN executors on"
									   f" sales.id_executor = executors.id_executor WHERE sales.id_sale={id_sale} and"
									   f" sales.id_manager={self.id_manager}").fetchall()
				elif name and not type_document:
					rows = cur.execute(f"SELECT sales.id_sale, sales.name, sales.cost_price, sales.payment, "
									   f"types_document.type_document, executors.executor, stages.stage, "
									   f"originals.original, sales.date_payment FROM sales INNER JOIN "
									   f"types_document on sales.id_type_document = types_document.id_type_document "
									   f"INNER "
									   f"JOIN stages on sales.id_stage = stages.id_stage INNER JOIN originals on "
									   f"sales.id_original = originals.id_original INNER JOIN executors on"
									   f" sales.id_executor = executors.id_executor WHERE sales.name like '%{name}%'"
									   f" AND sales.id_manager={self.id_manager}").fetchall()
				elif type_document and not name:

					id_type_document = cur.execute(f"SELECT id_type_document FROM types_document WHERE"
												   f" type_document = '{type_document}'").fetchall()[0][0]
					rows = cur.execute(f"SELECT sales.id_sale, sales.name, sales.cost_price, sales.payment, "
									   f"types_document.type_document, executors.executor, stages.stage, "
									   f"originals.original, sales.date_payment FROM sales INNER JOIN "
									   f"types_document on sales.id_type_document = types_document.id_type_document "
									   f"INNER "
									   f"JOIN stages on sales.id_stage = stages.id_stage INNER JOIN originals on "
									   f"sales.id_original = originals.id_original INNER JOIN executors on"
									   f" sales.id_executor = executors.id_executor WHERE sales.id_type_document="
									   f"{id_type_document} AND sales.id_manager={self.id_manager}").fetchall()
				elif name or type_document:
					id_type_document = cur.execute(f"SELECT id_type_document FROM types_document WHERE"
												   f" type_document = '{type_document}'").fetchall()[0][0]
					rows = cur.execute(f"SELECT sales.id_sale, sales.name, sales.cost_price, sales.payment, "
									   f"types_document.type_document, executors.executor, stages.stage, "
									   f"originals.original, sales.date_payment FROM sales INNER JOIN "
									   f"types_document on sales.id_type_document = types_document.id_type_document "
									   f"INNER "
									   f"JOIN stages on sales.id_stage = stages.id_stage INNER JOIN originals on "
									   f"sales.id_original = originals.id_original INNER JOIN executors on"
									   f" sales.id_executor = executors.id_executor WHERE name='{name}' AND"
									   f" id_type_document={id_type_document} AND"
									   f" id_manager={self.id_manager}").fetchall()
				elif date_from and date_to:
					rows = cur.execute(f"SELECT sales.id_sale, sales.name, sales.cost_price, sales.payment, "
									   f"types_document.type_document, executors.executor, stages.stage, "
									   f"originals.original, sales.date_payment FROM sales INNER JOIN "
									   f"types_document on sales.id_type_document = types_document.id_type_document "
									   f"INNER "
									   f"JOIN stages on sales.id_stage = stages.id_stage INNER JOIN originals on "
									   f"sales.id_original = originals.id_original INNER JOIN executors on"
									   f" sales.id_executor = executors.id_executor WHERE sales.id_manager="
									   f"{self.id_manager} AND sales.date_payment >= '{date_from}'"
									   f" AND sales.date_payment <= '{date_to}'").fetchall()
				else:
					raise ValueError
				if len(rows) == 0:
					messagebox.showerror('Error', 'Нет таких сделок. Где-то ошибка')
				elif len(rows) == 1:
					self.root.destroy()
					update_window = UpdateWindow(results=self.results, id_manager=self.id_manager, id_sale=rows[0][0])
					update_window.run()
				else:
					self.root.destroy()
					choice_sale = ChoiceSaleForUpdate(results=self.results, id_manager=self.id_manager,
													  rows=rows, c_rows=len(rows))
					choice_sale.run()
			else:
				raise IndexError
		except ValueError:
			messagebox.showerror('Error', 'Нет таких сделок. Где-то ошибка')
		except IndexError:
			messagebox.showerror('Error', 'Нужно внести данные:\nисполнитель, тип документа, этап, оригинал')

	def create_payroll(self):
		stage = self.entry_stage.get()
		original = self.entry_original.get()
		try:
			if stage and not original:
				id_stage = cur.execute("SELECT id_stage FROM stages WHERE stage = ?", (stage,)).fetchall()[0][0]
				cur.execute("SELECT sales.id_sale, sales.name, sales.cost_price, sales.payment, (sales.payment - "
							"sales.cost_price)*0.9, types_document.type_document, stages.stage, originals.original "
							"FROM sales INNER JOIN "
							"stages on sales.id_stage = stages.id_stage INNER JOIN types_document on "
							"sales.id_type_document = types_document.id_type_document INNER JOIN originals ON "
							"sales.id_original = originals.id_original WHERE sales.id_manager = ? AND "
							"sales.id_stage = ?", (self.id_manager, id_stage))
				rows = cur.fetchall()
				height = 500
				c_rows = 2
				self.root.destroy()
				show_result = ShowResult(c_rows=c_rows, height=height, rows=rows,
										 results=self.results, id_manager=self.id_manager)
				show_result.run()
			elif original and not stage:
				id_original = cur.execute("SELECT id_original FROM originals"
										  " WHERE original = ?", (original,)).fetchall()[0][0]
				cur.execute("SELECT sales.id_sale, sales.name, sales.cost_price, sales.payment, (sales.payment - "
							"sales.cost_price)*0.9, types_document.type_document, stages.stage, originals.original "
							"FROM sales INNER JOIN "
							"stages on sales.id_stage = stages.id_stage INNER JOIN types_document on "
							"sales.id_type_document = types_document.id_type_document INNER JOIN originals ON "
							"sales.id_original = originals.id_original WHERE sales.id_manager = ? AND "
							"sales.id_original = ?", (self.id_manager, id_original))
				rows = cur.fetchall()
				height = 500
				c_rows = 5 + len(rows)
				self.root.destroy()
				show_result = ShowResult(c_rows=c_rows, height=height, rows=rows,
										 results=self.results, id_manager=self.id_manager)
				show_result.run()
			elif stage and original:
				id_stage = cur.execute("SELECT id_stage FROM stages WHERE stage = ?", (stage,)).fetchall()[0][0]
				id_original = cur.execute("SELECT id_original FROM originals"
										  " WHERE original = ?", (original,)).fetchall()[0][0]
				cur.execute("SELECT sales.id_sale, sales.name, sales.cost_price, sales.payment, (sales.payment - "
							"sales.cost_price)*0.9, types_document.type_document, stages.stage, originals.original "
							"FROM sales INNER JOIN stages on sales.id_stage = stages.id_stage INNER JOIN "
							"types_document on sales.id_type_document = types_document.id_type_document INNER JOIN "
							"originals ON sales.id_original = originals.id_original WHERE sales.id_manager = ? AND "
							"sales.id_stage = ? AND sales.id_original = ?", (self.id_manager, id_stage, id_original))
				rows = cur.fetchall()
				height = 500
				c_rows = 5 + len(rows)
				self.root.destroy()
				show_result = ShowResult(c_rows=c_rows, height=height, rows=rows,
										 results=self.results, id_manager=self.id_manager)
				show_result.run()
			else:
				raise ValueError
		except ValueError:
			messagebox.showerror('Error', 'Необходимо выбрать этап или оригинал')


class AdminWindow(UserWindow):
	def __init__(self, results, id_manager, width=450, height=400, title='start_admin', c_rows=12, c_columns=3):
		super().__init__(results, id_manager, width, height, title, c_rows, c_columns)

	def draw_additional_widgets(self):
		Button(self.root, text='Добавить пользователя', command=self.add_user, width=22). \
			grid(row=7, column=0, sticky=W + E, **self.params)
		Button(self.root, text='Добавить исполнителя', command=self.add_executor, width=22). \
			grid(row=8, column=0, sticky=W + E, **self.params)
		Button(self.root, text='Добавить тип документа', command=self.add_type_document, width=22). \
			grid(row=9, column=0, sticky=W + E, **self.params)
		Button(self.root, text='Добавить этап', command=self.add_stage, width=22). \
			grid(row=10, column=0, sticky=W + E, **self.params)
		Button(self.root, text='Добавить этап оригинала', command=self.add_original, width=22). \
			grid(row=11, column=0, sticky=W + E, **self.params)

	def add_user(self):
		self.root.destroy()
		add_user = AddUser(results=self.results, id_manager=self.id_manager)
		add_user.run()

	def add_executor(self):
		self.root.destroy()
		add_executor = AddExecutor(results=self.results, id_manager=self.id_manager)
		add_executor.run()

	def add_type_document(self):
		self.root.destroy()
		add_type_document = AddTypeDocument(results=self.results, id_manager=self.id_manager)
		add_type_document.run()

	def add_stage(self):
		self.root.destroy()
		add_type_document = AddStage(results=self.results, id_manager=self.id_manager)
		add_type_document.run()

	def add_original(self):
		self.root.destroy()
		add_type_document = AddOriginal(results=self.results, id_manager=self.id_manager)
		add_type_document.run()

	def run(self):
		self.draw_widgets()
		self.draw_additional_widgets()
		self.root.mainloop()


class AddSale(StartWindow):
	def __init__(self, results, id_manager, width=300, height=200, title='add_sale', c_rows=6, c_columns=2):
		super().__init__(results, width, height, title, c_rows, c_columns)
		self.id_manager = id_manager
		self.results_for_add = results
		self.entry_name = Entry(self.root, width=27)
		self.entry_payment = Entry(self.root, width=27)
		if self.results_for_add:
			self.entry_name.insert(0, self.results_for_add[1])
			self.entry_payment.insert(0, self.results_for_add[-1])
		self.entry_type_document = Combobox(self.root,
											values=[type_document[0] for type_document in
													cur.execute("SELECT type_document FROM types_document").fetchall()],
											state='readonly', width=24)
		self.entry_executor = Combobox(self.root,
									   values=[executor[0] for executor in
											   cur.execute("SELECT executor FROM executors").fetchall()],
									   state='readonly', width=24)

	def draw_widgets(self):
		list_headers = ['Юр. лицо', 'Сумма продажи', 'Исполнитель', 'Тип документа']
		for index_row, header in enumerate(list_headers):
			Label(self.root, text=header).grid(row=index_row, column=0, sticky=W, **self.params)
		self.entry_name.grid(row=0, column=1, sticky=W + E, **self.params)
		self.entry_payment.grid(row=1, column=1, sticky=W + E, **self.params)
		self.entry_executor.grid(row=2, column=1, sticky=W + E, **self.params)
		self.entry_type_document.grid(row=3, column=1, sticky=W + E, **self.params)

		Button(self.root, text='Добавить', command=self.add_sale_to_sql, width=22). \
			grid(row=4, column=1, sticky=W + E, **self.params)
		Button(self.root, text='В меню', command=self.go_to_start, width=22). \
			grid(row=5, column=1, sticky=W + E, **self.params)

	def go_to_start(self):
		self.root.destroy()
		if self.id_manager == 1:
			admin_window = AdminWindow(results=self.results, id_manager=self.id_manager)
			admin_window.run()
		else:
			user_window = UserWindow(results=self.results, id_manager=self.id_manager)
			user_window.run()

	def add_sale_to_sql(self):
		if self.entry_name.get() and self.entry_payment.get() and \
				self.entry_type_document.get() and self.entry_executor.get():
			name = self.entry_name.get()
			payment = int(self.entry_payment.get())
			type_document = self.entry_type_document.get()
			code_payment = self.results_for_add[0]
			id_type_document = cur.execute(
				f"SELECT id_type_document FROM types_document WHERE type_document='{type_document}'").fetchall()[0][
				0]
			executor = self.entry_executor.get()
			id_executor = cur.execute(f"SELECT id_executor FROM executors WHERE executor='{executor}'").fetchall()[0][0]

			cost_price = cur.execute(f"SELECT cost_price from prices WHERE id_executor={id_executor} AND "
									 f"id_type_document={id_type_document}").fetchall()[0][0]

			cur.execute("INSERT INTO sales VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
						(self.id_manager, name, id_type_document, cost_price, payment, id_executor, 1, 1,
						 datetime.date.today(), code_payment))
			con.commit()
			if self.results_for_add in self.results:
				self.results.remove(self.results_for_add)
			self.root.destroy()
			if self.id_manager == 1:
				admin_window = AdminWindow(results=self.results, id_manager=self.id_manager)
				admin_window.run()
			else:
				user_window = UserWindow(results=self.results, id_manager=self.id_manager)
				user_window.run()
		else:
			messagebox.showerror('Error', 'Необходимо заполнить все поля')


class AddUser(AddSale):
	def __init__(self, results, id_manager, width=280, height=230, title='add_user', c_rows=7, c_columns=2):
		super().__init__(results, id_manager, width, height, title, c_rows, c_columns)
		self.entry_name = Entry(self.root)
		self.entry_s_mame = Entry(self.root)
		self.entry_department = Entry(self.root)
		self.entry_login = Entry(self.root)
		self.entry_pass = Entry(self.root)

	def draw_widgets(self):
		list_headers = ['Имя', 'Фамилия', 'Отдел', 'Логин', 'Пароль']
		for index_row, header in enumerate(list_headers):
			Label(self.root, text=header).grid(row=index_row, column=0, sticky=W, **self.params)
		self.entry_name.grid(row=0, column=1, sticky=W + E, **self.params)
		self.entry_s_mame.grid(row=1, column=1, sticky=W + E, **self.params)
		self.entry_department.grid(row=2, column=1, sticky=W + E, **self.params)
		self.entry_login.grid(row=3, column=1, sticky=W + E, **self.params)
		self.entry_pass.grid(row=4, column=1, sticky=W + E, **self.params)

		Button(self.root, text='Добавить', command=self.add_user_to_sql). \
			grid(row=5, column=1, sticky=W + E, **self.params)
		Button(self.root, text='В меню', command=self.go_to_start).grid(row=6, column=1, sticky=W + E, **self.params)

	def add_user_to_sql(self):
		name = self.entry_name.get()
		s_mame = self.entry_s_mame.get()
		department = self.entry_department.get()
		login = self.entry_login.get()
		password = self.entry_pass.get()
		cur.execute("INSERT INTO managers VALUES (NULL, ?, ?, ?, ?, ?)",
					(name, s_mame, department, login, password))
		con.commit()
		self.root.destroy()
		admin_window = AdminWindow(results=self.results, id_manager=self.id_manager)
		admin_window.run()


class AddExecutor(AddSale):
	def __init__(self, results, id_manager, width=280, height=200, title='add_executor', c_rows=6, c_columns=2):
		super().__init__(results, id_manager, width, height, title, c_rows, c_columns)

		self.entry_executor = Entry(self.root)
		self.entry_contact_person = Entry(self.root)
		self.entry_phone_number = Entry(self.root)
		self.entry_mail = Entry(self.root)

	def draw_widgets(self):
		list_headers = ['Исполнитель', 'Контактное лицо', 'Телефон', 'Почта']
		for index_row, header in enumerate(list_headers):
			Label(self.root, text=header).grid(row=index_row, column=0, sticky=W, **self.params)
		self.entry_executor.grid(row=0, column=1, sticky=W + E, **self.params)
		self.entry_contact_person.grid(row=1, column=1, sticky=W + E, **self.params)
		self.entry_phone_number.grid(row=2, column=1, sticky=W + E, **self.params)
		self.entry_mail.grid(row=3, column=1, sticky=W + E, **self.params)

		Button(self.root, text='Добавить', command=self.add_executor_to_sql). \
			grid(row=4, column=1, sticky=W + E, **self.params)
		Button(self.root, text='В меню', command=self.go_to_start).grid(row=5, column=1, sticky=W + E, **self.params)

	def add_executor_to_sql(self):
		executor = self.entry_executor.get()
		contact_person = self.entry_contact_person.get()
		phone_number = self.entry_phone_number.get()
		mail = self.entry_mail.get()
		try:
			if cur.execute(f"SELECT executor FROM executors"
						   f" WHERE executor='{executor}'").fetchall():
				raise ValueError
			else:
				cur.execute("INSERT INTO executors VALUES (NULL, ?, ?, ?, ?)",
							(executor, contact_person, phone_number, mail))
				con.commit()

				id_executor = \
					cur.execute(f"SELECT id_executor FROM executors WHERE executor='{executor}'").fetchall()[0][0]
				list_id_type_document = cur.execute('''SELECT id_type_document FROM types_document''').fetchall()
				cost = 0
				for id_type_document in list_id_type_document:
					cur.execute("INSERT INTO prices VALUES (NULL, ?, ?, ?)", (id_executor, id_type_document[0], cost))
					con.commit()
				self.root.destroy()
				admin_window = AdminWindow(results=self.results, id_manager=self.id_manager)
				admin_window.run()
		except ValueError:
			messagebox.showerror('Error', 'Такой уже есть')


class AddTypeDocument(AddSale):
	def __init__(self, results, id_manager, width=280, height=100, title='add_type_document', c_rows=3, c_columns=2):
		super().__init__(results, id_manager, width, height, title, c_rows, c_columns)

		self.entry_type_document = Entry(self.root)

	def draw_widgets(self):
		Label(self.root, text='Тип документа').grid(row=0, column=0, sticky=W, **self.params)
		self.entry_type_document.grid(row=0, column=1, sticky=W + E, **self.params)

		Button(self.root, text='Добавить', command=self.add_type_document_to_sql). \
			grid(row=1, column=1, sticky=W + E, **self.params)
		Button(self.root, text='В меню', command=self.go_to_start).grid(row=2, column=1, sticky=W + E, **self.params)

	def add_type_document_to_sql(self):
		type_document = self.entry_type_document.get()
		try:
			if cur.execute(f"SELECT type_document FROM types_document"
						   f" WHERE type_document='{type_document}'").fetchall():
				raise ValueError
			else:
				cur.execute("INSERT INTO types_document VALUES (NULL, ?)", (type_document,))
				con.commit()

				list_id_executor = cur.execute(f"SELECT id_executor FROM executors").fetchall()
				id_type_document = cur.execute(f"SELECT id_type_document FROM types_document"
											   f" WHERE type_document='{type_document}'").fetchall()[0][0]
				cost = 0
				for id_executor in list_id_executor:
					cur.execute("INSERT INTO prices VALUES (NULL, ?, ?, ?)", (id_executor[0], id_type_document, cost))
					con.commit()
				self.root.destroy()
				admin_window = AdminWindow(results=self.results, id_manager=self.id_manager)
				admin_window.run()
		except ValueError:
			messagebox.showerror('Error', 'Такой уже есть')


class AddStage(AddTypeDocument):
	def __init__(self, results, id_manager, width=280, height=100, title='add_stage', c_rows=3, c_columns=2):
		super().__init__(results, id_manager, width, height, title, c_rows, c_columns)

		self.entry_stage = Entry(self.root)

	def draw_widgets(self):
		Label(self.root, text='Этап').grid(row=0, column=0, sticky=W, **self.params)
		self.entry_stage.grid(row=0, column=1, sticky=W + E, **self.params)

		Button(self.root, text='Добавить', command=self.add_stage_to_sql). \
			grid(row=1, column=1, sticky=W + E, **self.params)
		Button(self.root, text='В меню', command=self.go_to_start).grid(row=2, column=1, sticky=W + E, **self.params)

	def add_stage_to_sql(self):
		stage = self.entry_stage.get()
		try:
			if cur.execute(f"SELECT stage FROM stages"
						   f" WHERE stage='{stage}'").fetchall():
				raise ValueError
			else:
				cur.execute("INSERT INTO stages VALUES (NULL, ?)", (stage,))
				con.commit()
				self.root.destroy()
				admin_window = AdminWindow(results=self.results, id_manager=self.id_manager)
				admin_window.run()
		except ValueError:
			messagebox.showerror('Error', 'Такой уже есть')


class AddOriginal(AddTypeDocument):
	def __init__(self, results, id_manager, width=280, height=100, title='add_original', c_rows=3, c_columns=2):
		super().__init__(results, id_manager, width, height, title, c_rows, c_columns)

		self.entry_original = Entry(self.root)

	def draw_widgets(self):
		Label(self.root, text='Этап оригинала').grid(row=0, column=0, sticky=W, **self.params)
		self.entry_original.grid(row=0, column=1, sticky=W + E, **self.params)

		Button(self.root, text='Добавить', command=self.add_original_to_sql). \
			grid(row=1, column=1, sticky=W + E, **self.params)
		Button(self.root, text='В меню', command=self.go_to_start).grid(row=2, column=1, sticky=W + E, **self.params)

	def add_original_to_sql(self):
		original = self.entry_original.get()
		try:
			if cur.execute(f"SELECT original FROM originals"
						   f" WHERE original='{original}'").fetchall():
				raise ValueError
			else:
				cur.execute("INSERT INTO originals VALUES (NULL, ?)", (original,))
				con.commit()
				self.root.destroy()
				admin_window = AdminWindow(results=self.results, id_manager=self.id_manager)
				admin_window.run()
		except ValueError:
			messagebox.showerror('Error', 'Такой уже есть')


class ShowResult(StartWindow):
	def __init__(self, results, id_manager, rows, height, c_rows,
				 width=1000, title='show_result', c_columns=8):
		super().__init__(results, width, height, title, c_rows, c_columns)
		self.id_manager = id_manager
		self.results_for_show = rows

		self.frame_head = Frame(self.root, bd=1, relief=RAISED)
		self.frame_head.pack(fill=X)
		self.canvas_head = Canvas(self.frame_head, width=self.width, height=30)
		self.canvas_head.pack(fill=X, expand=True)
		self.frame_head_l = Frame(self.canvas_head)
		self.frame_head_l.pack(fill=X, expand=True)
		self.canvas_head.create_window((0, 0), window=self.frame_head_l, anchor=NW, width=self.width - 20)

		self.frame_body = Frame(self.root)
		self.frame_body.pack(fill=BOTH, expand=True)
		self.canvas = Canvas(self.frame_body)
		self.canvas.pack(fill=BOTH, expand=True)

		self.scrollbar_y = Scrollbar(self.canvas, orient=VERTICAL, command=self.canvas.yview)
		self.scrollbar_y.pack(side=RIGHT, fill=Y)

		self.frame_l = Frame(self.canvas)
		self.frame_l.pack(fill=BOTH)
		self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
		self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
		self.canvas.create_window((0, 0), window=self.frame_l, anchor=NW, width=self.width - 20)

		self.frame_footer = Frame(self.root, bd=1, relief=RAISED)
		self.frame_footer.pack(fill=BOTH)

		self.list_for_export = None
		self.list_headers = None
		self.c_rows = c_rows
		self.c_columns = c_columns

		for column in range(self.c_columns):
			self.frame_head_l.grid_columnconfigure(column, weight=1)
		for row in range(1):
			self.frame_head_l.grid_rowconfigure(row, weight=1)
		for column in range(self.c_columns):
			self.frame_l.grid_columnconfigure(column, weight=1)
		for column in range(3):
			self.frame_footer.grid_columnconfigure(column, weight=1)
		for row in range(2):
			self.frame_footer.grid_rowconfigure(row, weight=1)

	def draw_widgets(self):
		summa = 0
		self.list_headers = ['№ сделки', 'Юр. лицо', 'Закупка', 'Продажа',
							 'Дельта-10%', 'Тип документа', 'Этап', 'Оригинал']
		for index_column, header in enumerate(self.list_headers):
			if index_column in [0, 2, 3, 4, 6, 7]:
				Label(self.frame_head_l, text=header, width=10, anchor=W).grid(row=0, column=index_column, sticky=W,
																			   **self.params)
			else:
				Label(self.frame_head_l, text=header, width=20, anchor=W).grid(row=0, column=index_column, sticky=W,
																			   **self.params)
		for index_row, row in enumerate(self.results_for_show, 1):
			for index_value, value in enumerate(row):
				if index_value in [0, 2, 3, 4, 6, 7]:
					Label(self.frame_l, text=str(value), width=10, anchor=W).grid(row=index_row, column=index_value,
																				  sticky=W, **self.params)
				else:
					Label(self.frame_l, text=str(value), width=20, anchor=W).grid(row=index_row, column=index_value,
																				  sticky=W, **self.params)
				if index_value == 4:
					summa += value

		Label(self.frame_l, text='Итого').grid(row=len(self.results_for_show) + 1, column=0, sticky=W, **self.params)
		Label(self.frame_l, text=str(round(summa, 2))).grid(row=len(self.results_for_show) + 1,
															column=4, sticky=W, **self.params)

		Label(self.frame_l, text='К выдаче').grid(row=len(self.results_for_show) + 2, column=0, sticky=W, **self.params)
		Label(self.frame_l, text=str(round(summa * 0.2, 2))).grid(row=len(self.results_for_show) + 2,
																  column=4, sticky=W, **self.params)
		list_footers = [('ИТОГО', '', '', '', str(summa), '', ''), ('К выдаче', '', '', '', str(summa * 0.2), '', '')]
		self.list_for_export = self.results_for_show + list_footers

		Button(self.frame_footer, text='В меню', command=self.go_to_start).grid(row=1, column=1, sticky=W + E,
																				**self.params)
		Button(self.frame_footer, text='Экспорт в Excel', command=self.export_to_excel).grid(row=0, column=1,
																							 sticky=W + E,
																							 **self.params)

	def export_to_excel(self):
		dict_month = {'01': 'январь', '02': 'февраль', '03': 'март', '04': 'апрель', '05': 'май', '06': 'июнь',
					  '07': 'июль', '08': 'август', '09': 'сентябрь', '10': 'октябрь', '11': 'ноябрь',
					  '12': 'декабрь', }
		month = str(datetime.date.today()).split('-')[1]
		year = str(datetime.date.today()).split('-')[0]
		file_name = 'Ведомость_' + month + '_' + year + '.xlsx'
		df = pd.DataFrame(self.list_for_export)
		df.to_excel(file_name, dict_month[month], header=self.list_headers, index=False)

	def go_to_start(self):
		self.root.destroy()
		if self.id_manager == 1:
			admin_window = AdminWindow(results=self.results, id_manager=self.id_manager)
			admin_window.run()
		else:
			user_window = UserWindow(results=self.results, id_manager=self.id_manager)
			user_window.run()


class ChoiceSaleForUpdate(ShowResult):
	def __init__(self, results, c_rows, id_manager, rows, height=500, width=1000,
				 title='choice_sale_for_update', c_columns=10):
		super().__init__(results, id_manager, rows, height, c_rows, width, title, c_columns)
		self.results_for_choice = rows
		self.parameters = tuple()
		for index_row, row in enumerate(self.results_for_choice):
			self.parameters += ((row[0], IntVar()),)

	def draw_widgets(self):
		list_headers = ['', '№ сделки', 'Юр. лицо', 'Закупка', 'Продажа',
						'Тип документа', 'Исполнитель', 'Этап', 'Оригинал', 'Дата']
		for index_column, header in enumerate(list_headers):
			if index_column in [0, 1, 3, 4, 8, 9]:
				Label(self.frame_head_l, text=header, anchor=W, width=10).grid(row=0, column=index_column, sticky=W,
																			   **self.params)
			else:
				Label(self.frame_head_l, text=header, anchor=W, width=15).grid(row=0, column=index_column, sticky=W,
																			   **self.params)
		for index_row, row in enumerate(self.results_for_choice):
			Checkbutton(self.frame_l, variable=self.parameters[index_row - 2][1], width=7).grid(row=index_row, column=0,
																								sticky=W, **self.params)
			for index_value, value in enumerate(row, 1):
				if index_value in [1, 3, 4, 8, 9]:
					Label(self.frame_l, text=str(value), anchor=W, width=10).grid(row=index_row, column=index_value,
																				  sticky=W, **self.params)
				else:
					Label(self.frame_l, text=str(value), anchor=W, width=15).grid(row=index_row, column=index_value,
																				  sticky=W, **self.params)
		Button(self.frame_footer, text='В меню', command=self.go_to_start). \
			grid(row=1, column=1, sticky=W + E, **self.params)
		Button(self.frame_footer, text='Редактировать', command=self.update_sale). \
			grid(row=0, column=1, sticky=W + E, **self.params)

	def update_sale(self):
		for id_sale, check in self.parameters:
			if check.get():
				self.root.destroy()
				update_sale = UpdateWindow(results=self.results, id_manager=self.id_manager, id_sale=id_sale,
										   c_rows=4)
				update_sale.run()
				return
		messagebox.showerror('Error', 'необходимо выбрать сделку для редактирования')


class ChoiceSaleForAdd(ShowResult):
	def __init__(self, results, height, c_rows, id_manager, rows,
				 width=800, title='choice_sale_for_add', c_columns=4):
		super().__init__(results, id_manager, rows, height, c_rows, width, title, c_columns)
		self.parameters = tuple()
		for index_row, row in enumerate(self.results):
			self.parameters += ((row[0], row[1], row[2], IntVar()),)

	def draw_widgets(self):
		Label(self.frame_head_l, text='Уточните пожалуйста, какую сделку необходимо добавить?').grid(
			row=0, column=0, columnspan=4, sticky=W + E, **self.params)
		Label(self.frame_head_l, text='Юр. лицо').grid(row=1, column=1, sticky=W, **self.params)
		Label(self.frame_head_l, text='Продажа').grid(row=1, column=2, sticky=W, **self.params)
		for index_row, row in enumerate(self.results, 1):
			Checkbutton(self.frame_l, variable=self.parameters[index_row - 1][-1]).grid(row=index_row + 1, column=0,
																						sticky=W, **self.params)
			for index_value, value in enumerate(row, 1):
				Label(self.frame_l, text=str(value)).grid(row=index_row + 1, column=index_value,
														  sticky=W, **self.params)

		Button(self.frame_footer, text='В меню', command=self.go_to_start).grid(row=1, column=1, sticky=W + E,
																				**self.params)
		Button(self.frame_footer, text='Добавить', command=self.add_sale).grid(row=0, column=1, sticky=W + E,
																			   **self.params)

	def add_sale(self):
		for code, name, payment, check in self.parameters:
			if check.get():
				self.root.destroy()
				self.results = (code, name, payment)
				add_sale = AddSale(results=self.results, id_manager=self.id_manager)
				add_sale.run()
				return
		messagebox.showerror('Error', 'необходимо выбрать сделку для добавления')


class UpdateWindow(ShowResult):
	def __init__(self, results, id_manager, id_sale, rows=None,
				 height=160, width=1000, title='update_window', c_rows=4, c_columns=8):
		super().__init__(results, id_manager, rows, height, c_rows, width, title, c_columns)
		self.id_sale = id_sale
		self.list_for_check = None
		self.results_for_update = cur.execute("SELECT sales.id_sale, sales.name, sales.cost_price, sales.payment, "
											  "types_document.type_document, stages.stage, originals.original, "
											  "executors.executor FROM sales INNER JOIN types_document on "
											  "sales.id_type_document = types_document.id_type_document INNER JOIN "
											  "stages on "
											  "sales.id_stage = stages.id_stage INNER JOIN originals on "
											  "sales.id_original = "
											  "originals.id_original INNER JOIN executors on sales.id_executor = "
											  "executors.id_executor WHERE id_sale =?", (id_sale,)).fetchall()[0]
		self.parameters_for_insert = []
		for index, parameter in enumerate(self.results_for_update):
			if index == 0:
				self.parameters_for_insert.append(self.id_sale)
			elif index == 4:
				self.parameters_for_insert.append(Combobox(self.frame_l,
														   values=[type_document[0] for type_document in
																   cur.execute("SELECT type_document FROM "
																			   "types_document").fetchall()],
														   state='readonly', width=20))
				id_type_document = cur.execute("SELECT id_type_document FROM types_document WHERE type_document=?",
											   (parameter,)).fetchall()[0][0]
				self.parameters_for_insert[-1].current(id_type_document - 1)
			elif index == 5:
				self.parameters_for_insert.append(Combobox(self.frame_l,
														   values=[type_document[0] for type_document in
																   cur.execute("SELECT stage FROM "
																			   "stages").fetchall()],
														   width=20, state='readonly'))
				id_stage = cur.execute("SELECT id_stage FROM stages WHERE stage=?",
									   (parameter,)).fetchall()[0][0]
				self.parameters_for_insert[-1].current(id_stage - 1)
			elif index == 6:
				self.parameters_for_insert.append(Combobox(self.frame_l,
														   values=[type_document[0] for type_document in
																   cur.execute("SELECT original FROM "
																			   "originals").fetchall()],
														   width=20, state='readonly'))
				id_original = cur.execute("SELECT id_original FROM originals WHERE original=?",
										  (parameter,)).fetchall()[0][0]
				self.parameters_for_insert[-1].current(id_original - 1)
			elif index == 7:
				self.parameters_for_insert.append(Combobox(self.frame_l,
														   values=[type_document[0] for type_document in
																   cur.execute("SELECT executor FROM "
																			   "executors").fetchall()],
														   width=20, state='readonly'))
				id_executor = cur.execute("SELECT id_executor FROM executors WHERE executor=?",
										  (parameter,)).fetchall()[0][0]
				self.parameters_for_insert[-1].current(id_executor - 1)
			else:
				self.parameters_for_insert.append(Entry(self.frame_l,
														width=20))  # 2 * len(str(parameter))
				# if 2 * len(str(parameter)) < 30 else 30))
				self.parameters_for_insert[-1].insert(0, str(parameter))

	def draw_widgets(self):
		list_headers = ['№ сделки', 'Юр. лицо', 'Закупка', 'Продажа',
						'Тип документа', 'Этап', 'Оригинал', 'Исполнитель']
		for index_column, header in enumerate(list_headers):
			if index_column == 0:
				Label(self.frame_head_l, text=header, anchor=W, width=12).grid(row=0, column=index_column, sticky=W,
																			   **self.params)
			else:
				Label(self.frame_head_l, text=header, anchor=W, width=20).grid(row=0, column=index_column, sticky=W,
																			   **self.params)
		for index_value, value in enumerate(self.parameters_for_insert):
			if index_value == 0:
				Label(self.frame_l, text=value, anchor=W, width=10).grid(row=1, column=index_value, sticky=W,
																		 **self.params)
			else:
				value.grid(row=1, column=index_value, sticky=W, **self.params)

		Button(self.frame_footer, text='В меню', command=self.go_to_start).grid(row=1, column=1,
																				sticky=W + E, **self.params)
		Button(self.frame_footer, text='Сохранить', command=self.save_sale).grid(row=0, column=1,
																				 sticky=W + E, **self.params)

	def go_to_start(self):
		self.root.destroy()
		if self.id_manager == 1:
			admin_window = AdminWindow(results=self.results, id_manager=self.id_manager)
			admin_window.run()
		else:
			user_window = UserWindow(results=self.results, id_manager=self.id_manager)
			user_window.run()

	def save_sale(self):
		name = cost_price = payment = id_type_document = id_stage = id_original = id_executor = None
		for index_value, value in enumerate(self.parameters_for_insert[1:]):
			if index_value == 0:
				name = value.get()
			elif index_value == 1:
				try:
					if str(value.get()).isdigit():
						cost_price = int(value.get())
					else:
						raise ValueError
				except ValueError:
					messagebox.showerror('Error', 'Значение поля Закупка должно быть числом')
			elif index_value == 2:
				try:
					if str(value.get()).isdigit():
						payment = int(value.get())
					else:
						raise ValueError
				except ValueError:
					messagebox.showerror('Error', 'Значение поля Продажа должно быть числом')
			elif index_value == 3:
				id_type_document = cur.execute(f"SELECT id_type_document FROM types_document WHERE"
											   f" type_document='{value.get()}'").fetchall()[0][0]
			elif index_value == 4:
				id_stage = cur.execute(f"SELECT id_stage FROM stages WHERE"
									   f" stage='{value.get()}'").fetchall()[0][0]
			elif index_value == 5:
				id_original = cur.execute(f"SELECT id_original FROM originals WHERE"
										  f" original='{value.get()}'").fetchall()[0][0]
			elif index_value == 6:
				id_executor = cur.execute(f"SELECT id_executor FROM executors WHERE"
										  f" executor='{value.get()}'").fetchall()[0][0]
		cur.execute(f"UPDATE sales SET name='{name}', cost_price={cost_price}, payment={payment},"
					f" id_type_document={id_type_document}, id_stage={id_stage}, id_original={id_original}, "
					f"id_executor={id_executor} WHERE id_sale={self.id_sale}")
		self.list_for_check = [name, cost_price, payment, id_type_document, id_executor, id_stage, id_original]
		self.check_update()

	def check_update(self):
		result = cur.execute(f"SELECT name, cost_price, payment, id_type_document, id_executor, id_stage,"
							 f" id_original FROM sales WHERE id_sale={self.id_sale}").fetchall()[0]
		for value_for_check, value_result in zip(self.list_for_check, result):
			if value_for_check != value_result:
				messagebox.showerror('Error', 'Не получается. Проверьте данные')
				break
		else:
			messagebox.showinfo('Message', 'Сделка успешно отредактирована')
