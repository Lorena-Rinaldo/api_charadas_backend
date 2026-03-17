from flask import Flask, jsonify
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

if __name__ == "__main__":
    app.run(debug=True)