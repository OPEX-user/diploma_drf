import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

username = ''
password = ''


def send_mail(html=None, text='', subject='', from_email='', to_emails=[]):
    assert isinstance(to_emails, list)
    msg = MIMEMultipart('alternative')
    msg['От'] = from_email
    msg['К'] = ", ".join(to_emails)
    msg['Объект'] = subject
    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)

    html_part = MIMEText(f"<p>Вот ваш токен сброса пароля</p><h1>{html}</h1>", 'html')
    msg.attach(html_part)
    msg_str = msg.as_string()

    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_emails, msg_str)
    server.quit()
