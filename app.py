from flask import Flask, jsonify, request
import random
import firebase_admin
from firebase_admin import credentials, firestore

# Carrega as credenciais do Firebase
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

# ----- MÉTODOS PÚBLICOS -----

# Rota PRINCIPAL - Apresentação da API
@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "api": "charadas",
        "version" : "1.0",
        "author" : "Lorena Rinaldo"
    })


# Rota 1 - Método GET - Todas as charadas
@app.route("/charadas", methods=["GET"])
def get_charadas():
    charadas = [] #Lista vazia
    lista = db.collection('charadas').stream() #stream lista todos os dados
    
    # Tranforma objeto do firestore em dicionário python
    for item in lista:
        charadas.append(item.to_dict())
    return jsonify(charadas), 200


# Rota 2 - Método GET - Charadas aleatórias
@app.route("/charadas/aleatorias", methods=["GET"])
def get_charadas_random():
    charada = random.choice()
    return jsonify(charada), 200


# ----- MÉTODOS PRIVADOS -----

# Rota 3 - Método POST - Cadastro de novas charadas
@app.route("/charadas", methods=["POST"])
def post_charadas():
    dados = request.get_json()
    if not dados or "pergunta" not in dados or "resposta" not in dados:
        return jsonify({"error": "Dados inválidos"}), 400
    nova_charada = {"pergunta": dados["pergunta"], "resposta": dados["resposta"]}

    # .append(nova_charada)
    return (
        jsonify({"message": "Charada criada com sucesso!", "charada": nova_charada}),
        201,
    )


if __name__ == "__main__":
    app.run(debug=True)
