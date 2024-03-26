import re
import os
from config import Configuration


def validate_email(email) -> bool:
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return True if email_pattern.match(email) else False


def save_pdf_locally(pdf_data, pdf_name):
    files_directory = os.path.join(os.getcwd(), Configuration().FILES_DIRECTORY)

    if not os.path.exists(files_directory):
        os.makedirs(files_directory)

    file_path = os.path.join(files_directory, pdf_name)
    with open(file_path, 'wb') as f:
        f.write(pdf_data.getvalue())

    return f'{Configuration().APP_URL}/download/{pdf_name}'
