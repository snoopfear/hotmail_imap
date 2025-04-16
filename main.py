import imaplib
import email
import re
from getpass import getpass

# Ввод данных с клавиатуры
EMAIL = input("Введите ваш email: ")
PASSWORD = getpass("Введите ваш пароль: ")

# Настройки сервера (можно изменить под Gmail, Mail.ru и т.п.)
IMAP_SERVER = 'outlook.office365.com'
IMAP_PORT = 993

try:
    # Подключение к почте
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')

    # Получаем последнее письмо
    result, data = mail.search(None, 'ALL')
    mail_ids = data[0].split()
    if not mail_ids:
        print("В папке 'Входящие' нет писем.")
        exit()

    latest_email_id = mail_ids[-1]
    result, data = mail.fetch(latest_email_id, '(RFC822)')
    raw_email = data[0][1]

    # Парсим письмо
    msg = email.message_from_bytes(raw_email)

    # Получаем текст письма
    body = ''
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode(errors='ignore')
                break
    else:
        body = msg.get_payload(decode=True).decode(errors='ignore')

    # Ищем 6-значный код
    match = re.search(r'\b\d{6}\b', body)
    if match:
        print("✅ Найден код:", match.group())
    else:
        print("❌ Код не найден в последнем письме.")

except imaplib.IMAP4.error as e:
    print("Ошибка подключения к почте:", e)

finally:
    try:
        mail.logout()
    except:
        pass
