from flask import Flask, jsonify, request
import random

charadas = [
    {"pergunta": "O que é o que é? Tem cabeça, tem dente, tem barba, mas não é gente?", "resposta": "Alho"},
    {"pergunta": "O que é o que é? Tem asa, mas não voa?", "resposta": "Galinha"},
    {"pergunta": "O que é o que é? Tem um pescoço, mas não tem cabeça?", "resposta": "Garrafa"},
    {"pergunta": "O que é o que é? Tem um olho, mas não pode ver?", "resposta": "Agulha"},
    {"pergunta": "O que é o que é? Tem um coração que não bate?", "resposta": "Alcachofra"}
]

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return "API TÁ ON"

# Rota 1 - Método GET - Todas as charadas
@app.route("/charadas", methods=['GET'])
def get_charadas():
    return jsonify(charadas), 200

# Rota 2 - Método GET - Charadas aleatórias
@app.route("/charadas/aleatorias", methods=['GET'])
def get_charadas_random():
    charada = random.choice(charadas)
    return jsonify(charada), 200

# Rota 3 - Método POST - Cadastro de novas charadas
@app.route("/charadas", methods=['POST'])
def post_charadas():
    dados = request.get_json()
    if not dados or "pergunta" not in dados or "resposta" not in dados:
        return jsonify({"error":"Dados inválidos"}), 400
    nova_charada = {
        "pergunta": dados["pergunta"],
        "resposta": dados["resposta"]
    }
    
    charadas.append(nova_charada)
    return jsonify({"message": "Charada criada com sucesso!", "charada": nova_charada}), 201
        

if __name__ == "__main__":
    app.run(debug=True)