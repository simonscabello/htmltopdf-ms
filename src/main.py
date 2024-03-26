import io
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from weasyprint import HTML, CSS

from config import Configuration
from s3 import send_email, upload_to_s3
from util import save_pdf_locally, validate_email


app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({'message': 'OK'})


@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    try:
        data = request.json

        html = data.get('html')
        email = data.get('email')
        page_type = data.get('page_type', 'portrait')

        if not html:
            return jsonify({'error': 'HTML não informado'}), 400

        if not validate_email(email):
            return jsonify({'error': 'E-mail inválido'}), 400

        if page_type == 'landscape':
            css_content = '@page { size: landscape; margin: 1cm; }'
        else:
            css_content = '@page { size: portrait; margin: 1cm; }'

        pdf_data = io.BytesIO()
        HTML(string=html).write_pdf(pdf_data, stylesheets=[CSS(string=css_content)])

        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        random_id = str(uuid.uuid4())[:8]
        pdf_name = f"document_{timestamp}_{random_id}.pdf"

        if Configuration.SAVE_LOCAL:
            pdf_url = save_pdf_locally(pdf_data, pdf_name)
            if not pdf_url:
                return jsonify({'error': 'Erro ao salvar o arquivo localmente'}), 500
            return jsonify({'pdf_url': pdf_url}), 200
        else:
            pdf_url = upload_to_s3(pdf_data.getvalue(), pdf_name)
            if not pdf_url:
                return jsonify({'error': 'Erro ao fazer upload do arquivo para o S3'}), 500

        if not Configuration.SEND_MAIL:
            return jsonify({'pdf_url': pdf_url}), 200

        send_result = send_email(pdf_url, pdf_name, email)
        if not send_result:
            return jsonify({'error': 'Erro ao enviar e-mail com o PDF'}), 500

        return jsonify({'pdf_url': pdf_url}), 200
    except Exception as e:
        print(f"Erro inesperado durante a conversão para PDF: {e}")
        return jsonify({'error': 'Ocorreu um erro inesperado'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
