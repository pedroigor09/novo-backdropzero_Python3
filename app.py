from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import subprocess
import os
import sys

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    print("Requisição recebida na rota de boas-vindas")
    return "Bem-vindo ao seu servidor Python! O backend está no ar."

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['file']
    file.save('uploaded_image.png')
    print("Imagem recebida e salva como uploaded_image.png")
    return jsonify({"message": "Upload bem-sucedido"}), 200

@app.route('/remove-background', methods=['POST'])
def remove_background():
    file = request.files['file']
    file.save('input_image.png')
    print("Imagem recebida na rota de remoção de fundo")

    # Caminho relativo para o script
    script_path = os.path.join(os.path.dirname(__file__), 'U-2-Net', 'u2net_test.py')
    result = subprocess.run([sys.executable, script_path, 'input_image.png'], capture_output=True, text=True)
    print("Resultado da execução do script:", result.stdout)
    print("Erros da execução do script:", result.stderr)

    processed_image_path = 'input_image_processed.png'
    if os.path.exists(processed_image_path):
        return send_file(processed_image_path, mimetype='image/png')
    else:
        return jsonify({"message": "Erro ao processar a imagem"}), 500

@app.route('/images/all', methods=['GET'])
def get_all_images():
    try:
        image_directory = 'images'

        if not os.path.exists(image_directory):
            return jsonify({"message": "Diretório de imagens não encontrado"}), 500

        image_list = os.listdir(image_directory)
        image_list = [img for img in image_list if img.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        return jsonify({"images": image_list}), 200

    except Exception as e:
        print("Erro ao listar imagens:", str(e))
        return jsonify({"message": "Erro ao listar imagens"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
