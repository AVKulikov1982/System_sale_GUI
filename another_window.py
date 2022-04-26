import datetime
import xlwt
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkcalendar import DateEntry
from create_sql import cur
from main import StartWindow
import admin_window
import user_window
import add_window


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
		month = str(datetime.date.today()).split('-')[1]
		year = str(datetime.date.today()).split('-')[0]
		file_name = 'Ведомость_' + month + '_' + year + '.xls'
		book = xlwt.Workbook(encoding="utf-8")
		sheet1 = book.add_sheet(month + '_' + year)
		row = sheet1.row(0)
		for column in range(8):
			row.write(column, self.list_headers[column])
		for index, sale in enumerate(self.list_for_export):
			for column in range(len(sale)):
				row = sheet1.row(index + 1)
				row.write(column, sale[column])
		book.save(file_name)

	def go_to_start(self):
		self.root.destroy()
		if self.id_manager == 1:
			window_admin = admin_window.AdminWindow(results=self.results, id_manager=self.id_manager)
			window_admin.run()
		else:
			window_user = user_window.UserWindow(results=self.results, id_manager=self.id_manager)
			window_user.run()


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
				add_sale = add_window.AddSale(results=self.results, id_manager=self.id_manager)
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
			window_admin = admin_window.AdminWindow(results=self.results, id_manager=self.id_manager)
			window_admin.run()
		else:
			window_user = user_window.UserWindow(results=self.results, id_manager=self.id_manager)
			window_user.run()

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
