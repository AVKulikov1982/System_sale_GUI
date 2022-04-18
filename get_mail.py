import email
import imaplib
import re
from email.header import decode_header
from imap_tools import MailBox


def get_email_imap_tools() -> None:
	"""
	Функция для поиска в почтовом ящике писем с файлами в формате .pdf с почтового ящика бухгалтерии.
	:return: None
	"""

	with MailBox('imap.yandex.ru').login('test.system.sale@yandex.ru', 'pnmikqsnhpmcdreb',
										 'INBOX') as mailbox:
		for msg in mailbox.fetch():

			# email от кого пришло письмо
			print(msg.from_)

			# дата письма
			print(msg.date)

			# тема письма
			print(msg.subject)

			# узнать тип файла и скачать его
			#print(msg.attachments)
			print(msg.attachments[1].filename)
			#print(msg.attachments[0].size)
			#print(msg.attachments[0].payload)
			#print(msg.attachments[0].content_type)

			# тело письма
			msg_text = ''
			for val in re.findall(r'[А-Яа-я]*', msg.html):
				if val:
					msg_text += val + ' '
			print(msg_text)


def get_email_payments() -> None:
	"""
	Функция для поиска в почтовом ящике писем с файлами в формате .pdf с почтового ящика бухгалтерии.
	Сохраняет файл в случае успеха в заданной директории.
	:return: None
	"""

	imap = imaplib.IMAP4_SSL("imap.mail.ru")
	imap.login('test_system_sale@mail.ru', 'H5dYFa6g4Qp3CTmN1Mrv')
	imap.select("inbox")
	status, search_data = imap.search(None, 'ALL')
	try:
		if status == 'OK':
			for message_id in search_data[0].split():
				status, msg_data = imap.fetch(message_id, '(RFC822)')
				msg_raw = msg_data[0][1]
				raw_email_string = msg_raw.decode('utf8')
				list_mail = ['kulikov@ncl24.ru']

				# email от кого пришло письмо
				email_from = raw_email_string.split('\n')[1].split()[-1][1:-1]
				print(email_from)

				if email_from in list_mail:
					email_message = email.message_from_string(raw_email_string)

					# дата письма
					print(email_message['Date'])

					# тема письма
					subject = email_message['Subject']
					print(subject)

					# узнать тип файла и скачать его
					if email_message.get_payload():
						for obj in email_message.get_payload():
							if obj.get_filename():
								filename = obj.get_filename()
								if filename.endswith('pdf') and re.match(r'test', filename):
									with open('payments/' + filename, 'wb') as f_o:
										f_o.write(obj.get_payload(decode=True))
										print(filename)

					# тело письма

				# Удалить письмо
				# imap.store(message_id, '+FLAGS', '\\Deleted')
				# imap.expunge()
	except ValueError:
		print(ValueError)
	finally:
		imap.close()
		imap.logout()


# get_email_payments()
# get_email_imap_tools()
