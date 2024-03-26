from config import Configuration

import boto3
import requests
from botocore.exceptions import ClientError

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(pdf_url, pdf_name, email) -> str | None:
    try:
        sender_email = Configuration().MAIL_FROM_ADDRESS
        receiver_email = email

        ses_client = boto3.client('ses', region_name=Configuration().AWS_S3_REGION)

        msg = MIMEMultipart()
        msg['Subject'] = 'Relatório'
        msg['From'] = sender_email
        msg['To'] = receiver_email

        msg.attach(MIMEText(f'O relatório PDF foi gerado com sucesso!', 'plain'))

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
    except Exception as e:
        print(f"Erro inesperado durante o envio de e-mail: {e}")
    return None


def sign_url(path, expiration: int = 86400):
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=Configuration().AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Configuration().AWS_SECRET_ACCESS_KEY
        )

        return s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': Configuration().AWS_S3_BUCKET_NAME, 'Key': path},
            ExpiresIn=expiration
        )
    except ClientError as e:
        print(f"Erro ao gerar URL assinada: {e}")
    except Exception as e:
        print(f"Erro inesperado ao gerar URL assinada: {e}")
    return None


def upload_to_s3(pdf_data, pdf_name: str) -> str | None:
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=Configuration().AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Configuration().AWS_SECRET_ACCESS_KEY
        )

        path = f'{Configuration().AWS_S3_DIRECTORY}/{pdf_name}'

        s3.put_object(Body=pdf_data, Bucket=Configuration().AWS_S3_BUCKET_NAME, Key=path)
        signed_url = sign_url(path)

        return None if not signed_url else signed_url
    except ClientError as e:
        print(f"Erro ao fazer upload do arquivo para o S3: {e}")
    except Exception as e:
        print(f"Erro inesperado durante o upload para o S3: {e}")
    return None
