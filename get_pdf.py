import os
import fitz


def get_payments():
    try:
        list_pdf_document = []
        list_payments = []
        for value in os.listdir('payments'):
            if value.endswith('.pdf'):
                t_add = os.stat(f'payments\\{value}').st_ctime
                list_pdf_document.append((f'payments\\{value}', t_add))
        if list_pdf_document:
            doc = fitz.open(sorted(list_pdf_document, key=lambda x: x[1])[-1][0])

            for current_page in range(len(doc)):
                page = doc.load_page(current_page)

                page_text = page.get_textpage()

                tmp_text = page_text.extractText().split('Исходящий остаток')
                tmp_text = tmp_text[0].split('Сумма (RUB)')[-1]
                tmp_list = tmp_text.split('.00')[:-1]

                for sale in tmp_list:
                    tmp_name = sale.split('ИНН')[0]
                    tmp_payment = sale.split('ИНН')[-1]
                    tmp_code = tmp_name.split('\n')[2]
                    tmp_name = ' '.join(tmp_name.split('\n')[3:-1])
                    tmp_payment = tmp_payment.split('\n')[-1].replace(' ', '')
                    list_payments.append((tmp_code, tmp_name, tmp_payment))

            return list_payments
        else:
            raise ValueError
    except ValueError:
        return None
