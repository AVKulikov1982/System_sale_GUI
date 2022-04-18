import datetime
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkcalendar import DateEntry
from create_sql import cur, con
from main import StartWindow
import admin_window
import user_window


class AddSale(StartWindow):
	def __init__(self, results, id_manager, width=300, height=200, title='add_sale', c_rows=6, c_columns=2):
		super().__init__(results, width, height, title, c_rows, c_columns)
		self.id_manager = id_manager
		self.results_for_add = results
		self.entry_name = Entry(self.root, width=27)
		self.entry_payment = Entry(self.root, width=27)
		self.entry_type_document = Combobox(self.root,
											values=[type_document[0] for type_document in
													cur.execute("SELECT type_document FROM types_document").fetchall()],
											state='readonly', width=24)
		self.entry_executor = Combobox(self.root,
									   values=[executor[0] for executor in
											   cur.execute("SELECT executor FROM executors").fetchall()],
									   state='readonly', width=24)

	def draw_widgets(self):
		if self.results_for_add:
			self.entry_name.insert(0, self.results_for_add[1])
			self.entry_payment.insert(0, self.results_for_add[-1])
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
			window_admin = admin_window.AdminWindow(results=self.results, id_manager=self.id_manager)
			window_admin.run()
		else:
			window_user = user_window.UserWindow(results=self.results, id_manager=self.id_manager)
			window_user.run()

	def add_sale_to_sql(self):
		if self.entry_name.get() and self.entry_payment.get() and \
				self.entry_type_document.get() and self.entry_executor.get():
			name = self.entry_name.get()
			payment = int(self.entry_payment.get())
			type_document = self.entry_type_document.get()
			code_payment = ''
			if self.results_for_add:
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
				window_admin = admin_window.AdminWindow(results=self.results, id_manager=self.id_manager)
				window_admin.run()
			else:
				window_user = user_window.UserWindow(results=self.results, id_manager=self.id_manager)
				window_user.run()
		else:
			messagebox.showerror('Error', 'Необходимо заполнить все поля')


class AddUser(AddSale):
	def __init__(self, results, id_manager, width=280, height=230, title='add_user', c_rows=7, c_columns=2):
		super().__init__(results, id_manager, width, height, title, c_rows, c_columns)
		self.results_for_add = None
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
		window_admin = admin_window.AdminWindow(results=self.results, id_manager=self.id_manager)
		window_admin.run()


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
				window_admin = admin_window.AdminWindow(results=self.results, id_manager=self.id_manager)
				window_admin.run()
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
				window_admin = admin_window.AdminWindow(results=self.results, id_manager=self.id_manager)
				window_admin.run()
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
				window_admin = admin_window.AdminWindow(results=self.results, id_manager=self.id_manager)
				window_admin.run()
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
				window_admin = admin_window.AdminWindow(results=self.results, id_manager=self.id_manager)
				window_admin.run()
		except ValueError:
			messagebox.showerror('Error', 'Такой уже есть')
