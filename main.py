import os
import smtplib
from contextlib import nullcontext
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request,jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def send_email(subject, recipient_email, body_html):
    email_sender = os.getenv('GoogleMail_EmailSender')
    email_password = os.getenv('GoogleMail_Apikey')
    smtp_port = os.getenv('GoogleMail_Port')
    smtp_server = os.getenv('GoogleMail_Host')

    print(f'Email sender: {email_sender}')
    print(f'Email password: {email_password}')
    print(f'SMTP server: {smtp_server}')
    print(f'SMTP port: {smtp_port}')

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body_html, 'html'))

    try:
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.sendmail(email_sender, recipient_email, msg.as_string())

        return True
    except Exception as e:
        return False, str(e)

@app.route('/send-email', methods=['POST'])
def send_email_endpoint():
    data = request.json
    subject = data.get('subject')
    recipient = data.get('recipient')
    body_html = data.get('body_html')

    success = send_email(subject, recipient, body_html)
    print(f'success: {success}')
    if success:
        print('Email sent successfully')
        return jsonify({'message': 'Email send successfully'})
    else:
        print(f'Failed to send email')
        return jsonify({'error': f'failed to send email'})


# Endpoint para enviar el correo
@app.route('/welcom', methods=['POST'])
def Send_welcom():
    data = request.json
    recipient = data.get('recipient')
    username = data.get('username')


    body_html = f"<p>Hola {username} bienvenido a nuestra pagina<p>"
    subject = "Bienvenido a Nuestro Servicio"


    success = send_email(subject, recipient, body_html)
    print(f'Success: {success}')
    if success:
        print('Email sent successfully')
        return jsonify({'message': 'Email sent successfully'})
    else:
        print(f'Failed to send email')
        return jsonify({'error': 'Failed to send email'})

@app.route('/delete', methods=['DELETE'])
def Send_delete():
    data = request.json
    recipient = data.get('recipient')
    username = data.get('username')

    body_html = f"<p>El usuario: {username} ha sido eliminado<p>"
    subject = "Eliminado de Nuestro Servicio"


    success = send_email(subject, recipient, body_html)
    print(f'Success: {success}')
    if success:
        print('Email sent successfully')
        return jsonify({'message': 'Email sent successfully'})
    else:
        print(f'Failed to send email')
        return jsonify({'error': 'Failed to send email'})

@app.route('/newuser', methods=['PUT'])
def Send_update():
    data = request.json
    recipient = data.get('recipient')
    username = data.get('username')

    body_html = f"<p>El usuario {username} ha sido actualizado <p>"
    subject = "Datos Modificados"

    success = send_email(subject, recipient, body_html)
    print(f'Success: {success}')
    if success:
        print('Email sent successfully')
        return jsonify({'message': 'Email sent successfully'})
    else:
        print(f'Failed to send email')
        return jsonify({'error': 'Failed to send email'})

@app.route("/validation", methods=['POST'])
def ValidationUser():
    data = request.json
    email = data.get('email')
    code = data.get('code')
    subject = ("Su codigo de validacion es")

    success = send_email(subject, email, code)

    if success:
        print('Email sent successfully')
        return jsonify({'message': 'Email sent successfully'})
    else:
        print(f'Failed to send email')
        return jsonify({'error': 'Failed to send email'})


if __name__ == '__main__':
    app.run(debug=True)