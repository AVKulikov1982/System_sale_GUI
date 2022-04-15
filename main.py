from windows import StartWindow
from get_pdf import get_payments
from get_mail import get_email_payments


if __name__ == '__main__':
	get_email_payments()
	results = get_payments()
	start_window = StartWindow(results)
	start_window.run()
