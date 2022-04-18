import datetime
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkcalendar import DateEntry
from create_sql import cur
from main import StartWindow
from add_window import AddSale
from another_window import ShowResult, ChoiceSaleForAdd, ChoiceSaleForUpdate, UpdateWindow


class UserWindow(StartWindow):
	"""
	Класс — пользователя (наследник от стартового окна).
	Attributes:
	:param id_manager: id пользователя
	Methods:
	add_sale() - добавление сделки
	choice_sale_for_add() - добавление сделки из ведомости
	update_sale() - редактирование сделки
	create_payroll() - формирование ведомости
	"""

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
		"""Метод добавления сделки. Запускает окно добавления сделки"""

		self.root.destroy()
		self.results = None
		add_sale = AddSale(results=self.results, id_manager=self.id_manager)
		add_sale.run()

	def choice_sale_for_add(self):
		"""Метод добавления сделки из ведомости. Запускает окно добавления сделки из ведомости."""

		self.root.destroy()
		height = 35 * (len(self.results) + 4)
		choice_sale_for_add = ChoiceSaleForAdd(results=self.results, id_manager=self.id_manager,
											   c_rows=len(self.results), height=height,
											   rows=self.results)
		choice_sale_for_add.run()

	def update_sale(self):
		"""Метод редактирования сделки. Запускает окно редактирования сделки.
		Доступна возможность выбора сделки по id сделки, наименованию плательщика, дате создания, типу документа"""

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
		"""Метод формирования ведомости. Запускает окно ведомости. Для формирования необходимо выбрать этап / оригинал"""

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
