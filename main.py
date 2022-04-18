import datetime
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkcalendar import DateEntry
from create_sql import cur
import admin_window
import user_window
from get_pdf import get_payments
from get_mail import get_email_payments


class StartWindow:
	"""Класс — стартовое окно. Базовый родительский класс. С формой регистрации пользователя.
	Attributes:
	:param results: список сделок в формате кортежей ('номер ПП', 'наименование плательщика', 'сумма платежа')
	:param width: ширина окна.
	:param height: высота окна.
	:param title: название окна.
	:param c_rows: количество строк.
	:param c_columns: количество столбцов.
	:param params:
	Methods:
	get_registration() - авторизация пользователя
	draw_widgets() - отрисовка полей ввода и кнопок
	run() - запуск окна
	closing_procedure() - метод проверки возможности закрытия программы
	"""

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
		# self.root.protocol('WM_DELETE_WINDOW', lambda: self.closing_procedure())
		self.entry_login = Entry(self.root)
		self.entry_password = Entry(self.root, show='*')

	def get_registration(self):
		"""
		Метод авторизации пользователя
		При успешной авторизации запускает окно пользователя, в противном случае выдает
		всплывающее сообщение об ошибке авторизации.
		При вводе логина и пароля администратора запускает окно администратора
		"""

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
					window_admin = admin_window.AdminWindow(results=self.results, id_manager=id_manager)
					window_admin.run()
				elif test_password == password:
					self.root.destroy()
					window_user = user_window.UserWindow(results=self.results, id_manager=id_manager)
					window_user.run()
				else:
					messagebox.showerror('Error', 'Password неверный')
			else:
				raise ValueError
		except ValueError:
			messagebox.showerror('Error', 'Login неверный')

	def draw_widgets(self):
		"""Метод отрисовки полей ввода и кнопок """

		Label(self.root, text='Login').grid(row=0, column=0, sticky=W, **self.params)
		self.entry_login.grid(row=0, column=1, sticky=W + E, **self.params)
		Label(self.root, text='Password').grid(row=1, column=0, sticky=W, **self.params)
		self.entry_password.grid(row=1, column=1, sticky=W + E, **self.params)
		Button(self.root, text='Войти', command=self.get_registration).grid(row=3, column=1, sticky=W + E,
																			**self.params)

	def run(self):
		"""Метод запуска окна """

		self.draw_widgets()
		self.root.mainloop()

	# def closing_procedure(self):
	# 	"""Метод проверки возможности закрытия окна."""
	#
	# 	if datetime.datetime.time(datetime.datetime.now()) < datetime.time(18, 0, 0):
	# 		messagebox.showinfo('Message', 'Приложение закрывается автоматически\nВы можете свернуть приложение')
	# 	else:
	# 		self.root.destroy()

if __name__ == '__main__':
	get_email_payments()
	results = get_payments()
	start_window = StartWindow(results)
	start_window.run()
