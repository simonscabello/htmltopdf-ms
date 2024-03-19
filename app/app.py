import io
import os
import uuid
import boto3
import requests
from botocore.exceptions import ClientError
from datetime import datetime
from flask import Flask, request, jsonify
from weasyprint import HTML
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

load_dotenv()

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME')
AWS_S3_REGION = os.environ.get('AWS_S3_REGION')
MAIL_FROM_ADDRESS = os.environ.get('MAIL_FROM_ADDRESS')
MAIL_FROM_NAME = os.environ.get('MAIL_FROM_NAME')


app = Flask(__name__)


def sign_url(path, expiration=86400):
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': AWS_S3_BUCKET_NAME, 'Key': path},
            ExpiresIn=expiration
        )

        return url
    except ClientError as e:
        print(f"Erro ao gerar URL assinada: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado ao gerar URL assinada: {e}")


def upload_to_s3(pdf_data, pdf_name):
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        path = f'relatorios/{pdf_name}'

        s3.put_object(Body=pdf_data, Bucket=AWS_S3_BUCKET_NAME, Key=path)

        signed_url = sign_url(path)

        if not signed_url:
            return None

        return signed_url
    except ClientError as e:
        print(f"Erro ao fazer upload do arquivo para o S3: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado durante o upload para o S3: {e}")
        return None


def send_email(pdf_url, pdf_name, email):
    try:
        region_name = AWS_S3_REGION
        sender_email = MAIL_FROM_ADDRESS
        receiver_email = email
        subject = 'Relatório'
        body_text = f'O relatório PDF foi gerado com sucesso!'

        ses_client = boto3.client('ses', region_name=region_name)

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        msg.attach(MIMEText(body_text, 'plain'))

        response = requests.get(pdf_url)
        pdf_data = response.content

        attachment = MIMEApplication(pdf_data)
        attachment.add_header('Content-Disposition', 'attachment', filename=pdf_name)
        msg.attach(attachment)

        response = ses_client.send_raw_email(
            Source=sender_email,
            Destinations=[receiver_email],
            RawMessage={'Data': msg.as_string()}
        )

        return f"E-mail enviado com sucesso! Message ID: {response['MessageId']}"
    except ClientError as e:
        print(f"Erro ao enviar e-mail: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado durante o envio de e-mail: {e}")
        return None


@app.route('/')
def index():
    return jsonify({'message': 'OK'})


@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    try:
        data = request.json
        html = data.get('html')
        email = data.get('email')
        if not html:
            return jsonify({'error': 'HTML não informado'}), 400

        # Gerar o arquivo PDF em memória
        pdf_data = io.BytesIO()
        HTML(string=html).write_pdf(pdf_data)

        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        random_id = str(uuid.uuid4())[:8]
        pdf_name = f"document_{timestamp}_{random_id}.pdf"

        pdf_url = upload_to_s3(pdf_data.getvalue(), pdf_name)
        if not pdf_url:
            return jsonify({'error': 'Erro ao fazer upload do arquivo para o S3'}), 500

        send_result = send_email(pdf_url, pdf_name, email)
        if not send_result:
            return jsonify({'error': 'Erro ao enviar e-mail com o PDF'}), 500

        return jsonify({'pdf_url': pdf_url}), 200
    except Exception as e:
        print(f"Erro inesperado durante a conversão para PDF: {e}")
        return jsonify({'error': 'Ocorreu um erro inesperado'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
