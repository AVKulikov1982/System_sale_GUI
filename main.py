from windows import StartWindow
from get_mail import get_email_payments


def get_file_payments():
    get_email_payments()


if __name__ == '__main__':
    # get_file_payments()
    start_window = StartWindow()
    start_window.run()
