from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkcalendar import DateEntry
from create_sql import cur
from user_window import UserWindow
from add_window import AddUser, AddStage, AddExecutor, AddOriginal, AddTypeDocument


class AdminWindow(UserWindow):
	"""
	Класс — администратора (наследник от класса окно пользователя).
	Attributes:

	Methods:
	draw_additional_widgets() - отрисовка дополнительных кнопок
	add_user() - добавление пользователя
	add_executor() - добавление исполнителя
	add_type_document() - добавление типа документа
	add_stage() - добавление этапа сделки
	add_original() - добавление этапа стадии оригинала документа
	"""


	def __init__(self, results, id_manager, width=450, height=400, title='start_admin', c_rows=12, c_columns=3):
		super().__init__(results, id_manager, width, height, title, c_rows, c_columns)

	def draw_additional_widgets(self):
		"""Метод отрисовки дополнительных кнопок"""

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
		"""Метод добавления пользователя. Запускает окно добавления пользователя"""

		self.root.destroy()
		add_user = AddUser(results=self.results, id_manager=self.id_manager)
		add_user.run()

	def add_executor(self):
		"""Метод добавления исполнителя. Запускает окно добавления исполнителя"""

		self.root.destroy()
		add_executor = AddExecutor(results=self.results, id_manager=self.id_manager)
		add_executor.run()

	def add_type_document(self):
		"""Метод добавления типа документа. Запускает окно добавления типа документа"""

		self.root.destroy()
		add_type_document = AddTypeDocument(results=self.results, id_manager=self.id_manager)
		add_type_document.run()

	def add_stage(self):
		"""Метод добавления этапа сделки. Запускает окно добавления этапа сделки"""

		self.root.destroy()
		add_type_document = AddStage(results=self.results, id_manager=self.id_manager)
		add_type_document.run()

	def add_original(self):
		"""Метод добавления этапа стадии оригинала документа. Запускает окно добавления этапа стадии оригинала документа"""

		self.root.destroy()
		add_type_document = AddOriginal(results=self.results, id_manager=self.id_manager)
		add_type_document.run()

	def run(self):
		"""Метод запуска окна администратора. Запускает окно администратора"""

		self.draw_widgets()
		self.draw_additional_widgets()
		self.root.mainloop()