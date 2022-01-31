import email
import imaplib
import re
from email.header import decode_header
from imap_tools import MailBox


def get_email_imap_tools():
    with MailBox('imap.yandex.ru').login('test.system.sale@yandex.ru', 'FZ4]fY[VJ63/+w', 'INBOX') as mailbox:
        for msg in mailbox.fetch():
            print(msg.subject)
            print(msg.date)
            print(msg.attachments)
            print(msg.attachments[0].filename)
            print(msg.attachments[0].size)
            # print(msg.attachments[0].payload)
            print(msg.attachments[0].content_type)
            print(msg.from_)
            msg_text = ''
            for val in re.findall(r'[А-Яа-я]*', msg.html):
                if val:
                    msg_text += val + ' '
            print(msg_text)


def get_email_payments():
    imap = imaplib.IMAP4_SSL("imap.mail.ru")
    imap.login('test_system_sale@mail.ru', 'FZ4]fY[V~J63/+w')
    imap.select("inbox")
    status, search_data = imap.search(None, 'ALL')
    print(status, search_data)
    try:
        if status == 'OK':

            for message_id in search_data[0].split():
                status, msg_data = imap.fetch(message_id, '(RFC822)')

                msg_raw = msg_data[0][1]

                raw_email_string = msg_raw.decode('utf-8')
                list_mail = []
                # email от кого пришло письмо
                email_from = raw_email_string.split('\n')[1].split()[-1][1:-1]
                if raw_email_string.split('\n')[1].split()[-1][1:-1] in list_mail:
                    email_message = email.message_from_string(raw_email_string)
                    # тело письма
                    body_text = email_message.get_payload()[0].get_payload()
                    if type(body_text) is list:
                        body_text = ','.join(str(v) for v in body_text)
                    print(body_text)

                    # тема письма
                    subject = email_message['Subject']
                    subject_decode = decode_header(subject)[0][0].decode(decode_header(subject)[0][1])
                    print(subject_decode)
                    # узнать тип файла и скачать его
                    if email_message.get_payload():
                        attachment = email_message.get_payload()[1]
                        type_attachment = '.' + attachment.get_content_type().split('/')[-1]

                        if not attachment.get_filename().endswith(type_attachment):
                            filename = decode_header(attachment.get_filename())[0][0] \
                                .decode(decode_header(attachment.get_filename())[0][1])
                        else:
                            filename = attachment.get_filename()

                        if type_attachment == 'pdf' and re.match(r'statement', filename):
                            with open('payments/' + filename, 'wb') as f_o:
                                f_o.write(attachment.get_payload(decode=True))
                # Удалить письмо
                # imap.store(message_id, '+FLAGS', '\\Deleted')
                # imap.expunge()
    except ValueError:
        print(ValueError)
    finally:
        imap.close()
        imap.logout()


# get_email_imap_tools()