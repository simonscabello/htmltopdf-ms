import re


def validate_email(email) -> bool:
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return True if email_pattern.match(email) else False


def save_pdf_locally(pdf_data, pdf_name):
    with open(pdf_name, 'wb') as f:
        f.write(pdf_data.getvalue())
    return f"./{pdf_name}"