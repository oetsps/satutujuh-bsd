import smtplib
from email.mime.text import MIMEText

def send_mail(nama, kota, tanggal, nokk, nonik, phone, email):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    username = '6afe6752275d0f'
    password = '6350c79dc64636'
    message = f"<h3>New Feedback Submission</h3><ul><li>Warga: {nama}</li><li>Kota Lahir: {kota}</li><li>Tanggal Lahir: {tanggal}</li><li>KK: {nokk}</li><li>NIK: {nonik}</li><li>Phone: {phone}</li><li>Email: {email}</li></ul>"

    sender_email = 'email1@example.com'
    receiver_email = 'email2@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Pendaftaran Data Warga Sektor 1.7'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(username, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
