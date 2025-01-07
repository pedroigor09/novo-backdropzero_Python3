import os
import sys
import subprocess
import traceback
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from google.cloud import storage

# Configuração do Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

logging.basicConfig(level=logging.INFO)

# Configurar o cliente do Google Cloud Storage
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\global-pagoda-417001-1b4d82d4ba62.json'  # Caminho do seu arquivo JSON
storage_client = storage.Client()

# Nome do seu bucket no Google Cloud Storage
bucket_name = 'u2netaplicacao'

@app.route('/')
def home():
    logging.info("Requisição recebida na rota de boas-vindas")
    return "Bem-vindo ao seu servidor Python! O backend está no ar."

@app.route('/remove-background', methods=['POST'])
def remove_background():
    try:
        # Recebe a imagem da requisição
        file = request.files['file']
        input_image_path = 'input_image.png'
        file.save(input_image_path)
        logging.info("Imagem recebida na rota de remoção de fundo")

        # Carrega a imagem no Google Cloud Storage
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(input_image_path)
        blob.upload_from_filename(input_image_path)
        logging.info(f"Imagem carregada para o Google Cloud Storage: {input_image_path}")

        # Verifica o caminho do script de remoção de fundo
        potential_paths = [ 'C:/source/novo-backdropzero_Python3/app/U-2-Net/u2net_test.py',
            './u2net_test.py',
            '/u2net_test.py'
        ]
        script_path = next((path for path in potential_paths if os.path.isfile(path)), None)

        if not script_path:
            logging.error("Caminho do script não encontrado.")
            return jsonify({"message": "Caminho do script não encontrado"}), 500

        logging.info(f"Caminho do script: {script_path}")

        # Executa o script de remoção de fundo
        result = subprocess.run([sys.executable, script_path, input_image_path], capture_output=True, text=True)
        logging.info(f"Resultado da execução do script: {result.stdout}")
        logging.error(f"Erros da execução do script: {result.stderr}")

        # Caminho da imagem processada
        processed_image_path = os.path.join('test_data', 'u2net_results', 'input_image.png')

        if os.path.exists(processed_image_path):
            with open(processed_image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            # Retorna a imagem processada codificada em base64
            return jsonify({"id": 123, "data": encoded_string})
        else:
            logging.error("Imagem processada não encontrada.")
            return jsonify({"message": "Erro ao processar a imagem"}), 500

    except Exception as e:
        logging.error(f"Erro no processamento da imagem: {e}")
        logging.error(f"Stack trace: {traceback.format_exc()}")
        return jsonify({"message": "Erro no processamento da imagem"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
