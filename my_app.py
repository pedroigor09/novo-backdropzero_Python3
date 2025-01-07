import os
import sys
import subprocess
import traceback
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS

# Instalar torch em tempo de execução
os.system('pip install torch')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    print("Requisição recebida na rota de boas-vindas")
    return "Bem-vindo ao seu servidor Python! O backend está no ar."

@app.route('/remove-background', methods=['POST'])
def remove_background():
    try:
        file = request.files['file']
        input_image_path = 'input_image.png'
        file.save(input_image_path)
        print("Imagem recebida na rota de remoção de fundo")

        # Verificar a estrutura de diretórios
        print("Estrutura de diretórios atual:")
        for root, dirs, files in os.walk(os.getcwd()):
            print(f"Diretório: {root}")
            for filename in files:
                print(f"Arquivo: {filename}")

        # Caminhos potenciais para o script
        potential_paths = [
            './u2net_test.py',  # Caminho no diretório raiz
            '/u2net_test.py'    # Caminho absoluto no diretório raiz
        ]

        script_path = None
        for path in potential_paths:
            print(f"Verificando caminho: {path}")
            if os.path.isfile(path):
                script_path = path
                break

        if not script_path:
            print("Erro: Caminho do script não encontrado.")
            return jsonify({"message": "Caminho do script não encontrado"}), 500

        print("Caminho do script:", script_path)

        result = subprocess.run([sys.executable, script_path, input_image_path], capture_output=True, text=True)
        print("Resultado da execução do script:", result.stdout)
        print("Erros da execução do script:", result.stderr)

        processed_image_path = os.path.join('test_data', 'u2net_results', 'input_image.png')
        if os.path.exists(processed_image_path):
            with open(processed_image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            if not encoded_string:
                print("Erro: A string codificada está vazia.")
                return jsonify({"message": "Erro ao processar a imagem"}), 500
            print("String base64 codificada:", encoded_string)  # Log da string base64
            return jsonify({"id": 123, "data": encoded_string})
        else:
            print("Erro: Imagem processada não encontrada.")
            return jsonify({"message": "Erro ao processar a imagem"}), 500

    except Exception as e:
        print("Erro no processamento da imagem:", str(e))
        print("Stack trace:", traceback.format_exc())
        return jsonify({"message": "Erro no processamento da imagem"}), 500

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(host='0.0.0.0', port=5000)
