import os

from dotenv import load_dotenv


class Configuration:
    def __init__(self):
        load_dotenv()
        self.AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
        self.AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.AWS_S3_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME')
        self.AWS_S3_REGION = os.environ.get('AWS_S3_REGION')
        self.MAIL_FROM_ADDRESS = os.environ.get('MAIL_FROM_ADDRESS')
        self.MAIL_FROM_NAME = os.environ.get('MAIL_FROM_NAME')
        self.SEND_MAIL = os.environ.get('SEND_MAIL')
        self.SAVE_LOCAL = os.environ.get('SAVE_LOCAL')
