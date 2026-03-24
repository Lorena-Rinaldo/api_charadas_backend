from flask import Flask, jsonify, request
import random
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os

# Carrega as credenciais do Firebase
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

# 1. Carrega as variáveis do arquivo .env
load_dotenv()

# 2. Captura o valor da variável
TOKEN_API = os.getenv("TOKEN_API")


if not TOKEN_API:
    raise ValueError("A variável TOKEN_API não foi encontrada no arquivo .env!")


def validar_token():
    auth = request.headers.get("Authorization")
    if auth == f"Bearer {TOKEN_API}":
        return True
    return False


# ----- MÉTODOS PÚBLICOS -----


# Rota PRINCIPAL - Apresentação da API
@app.route("/", methods=["GET"])
def root():
    return jsonify({"api": "charadas", "version": "1.0", "author": "Lorena Rinaldo"})


# Rota 1 - Método GET - Todas as charadas
@app.route("/charadas", methods=["GET"])
def get_charadas():
    charadas = []  # Lista vazia
    lista = db.collection("charadas").stream()  # stream lista todos os dados

    # Tranforma objeto do firestore em dicionário python
    for item in lista:
        charadas.append(item.to_dict())
    return jsonify(charadas), 200


# Rota 2 - Método GET - Charada aleatória
@app.route("/charadas/aleatoria", methods=["GET"])
def get_charadas_random():
    charadas = []  # Lista vazia
    lista = db.collection("charadas").stream()

    for item in lista:
        charadas.append(item.to_dict())
    return jsonify(random.choice(charadas)), 200


# Rota 3 - Método GET - Retorna charada pelo id
@app.route("/charadas/<int:id>", methods=["GET"])
def get_charada_by_id(id):
    lista = db.collection("charadas").where("id", "==", id).stream()

    for item in lista:
        return jsonify(item.to_dict()), 200
    return jsonify({"error": "Charada não encontrada"}), 404


# ----- MÉTODOS PRIVADOS -----


# Rota 4 - Método POST - Cadastro de novas charadas
@app.route("/charadas", methods=["POST"])
def post_charadas():
    if not validar_token():
        return jsonify({"error": "Acesso negado!"}), 401

    dados = request.get_json()
    if not dados or "pergunta" not in dados or "resposta" not in dados:
        return jsonify({"error": "Dados inválidos ou incompletos"}), 400

    try:
        # Busca pelo contador de id
        contador_ref = db.collection("contador").document("controle_id")
        contador_doc = contador_ref.get()
        ultimo_id = contador_doc.to_dict().get("ultimo_id")

        # Somar 1 ao último id
        novo_id = ultimo_id + 1

        # Atualiza o id do contador do firebase
        contador_ref.update({"ultimo_id": novo_id})

        # Cadastrar nova charada
        db.collection("charadas").add(
            {
                "id": novo_id,
                "pergunta": dados["pergunta"],
                "resposta": dados["resposta"],
            }
        )

        return (jsonify({"message": "Charada criada com sucesso!"}), 201)

    except:
        return (jsonify({"error": "Falha no envio do arquivo"}), 400)


# Rota 5 - Método PUT - Alteração total
@app.route("/charadas/<int:id>", methods=["PUT"])
def charadas_put(id):
    if not validar_token():
        return jsonify({"error": "Acesso negado!"}), 401

    dados = request.get_json()

    # PUT - É necessário enviar PERGUNTA e resposta
    if not dados or "pergunta" not in dados or "resposta" not in dados:
        return jsonify({"error": "Dados inválidos ou incompletos"}), 400

    try:
        docs = db.collection("charadas").where("id", "==", id).limit(1).get()
        if not docs:
            return jsonify({"error": "Charada não encontrada"}), 404

        # Pega o primeiro (e único) documento da lista
        for doc in docs:
            doc_ref = db.collection("charadas").document(doc.id)

            doc_ref.update(
                {"pergunta": dados["pergunta"], "resposta": dados["resposta"]}
            )

        return (jsonify({"message": "Charada alterada com sucesso!"}), 200)
    except:
        return jsonify({"error": "Dados inválidos ou incompletos"}), 400


# Rota 6 - Método PATCH - Alteração parcial(pergunta OU resposta)
@app.route("/charadas/<int:id>", methods=["PATCH"])
def charadas_patch(id):
    if not validar_token():
        return jsonify({"error": "Acesso negado!"}), 401

    dados = request.get_json()

    # PATCH - Pode ter SÓ a PERGUNTA ou SÓ a RESPOSTA
    if not dados or ("pergunta" not in dados and "resposta" not in dados):
        return jsonify({"error": "Dados inválidos!"}), 400

    try:
        docs = db.collection("charadas").where("id", "==", id).limit(1).get()
        if not docs:
            return jsonify({"error": "Charada não encontrada"}), 404

        doc_ref = db.collection("charadas").document(docs[0].id)

        update_charada = {}

        if "pergunta" in dados:
            update_charada["pergunta"] = dados["pergunta"]
        if "resposta" in dados:
            update_charada["resposta"] = dados["resposta"]

        # Atualiza o Firestore
        doc_ref.update(update_charada)

        return (jsonify({"message": "Charada alterada com sucesso!"}), 200)
    except:
        return jsonify({"error": "Dados inválidos ou incompletos"}), 400


# Rota 7 - Método DELETE - Deletar charadas
@app.route("/charadas/<int:id>", methods=["DELETE"])
def charadas_delete(id):
    if not validar_token():
        return jsonify({"error": "Acesso negado!"}), 401

    docs = db.collection("charadas").where("id", "==", id).limit(1).get()

    if not docs:
        return jsonify({"error": "Charada não encontrada"}), 404

    doc_ref = db.collection("charadas").document(docs[0].id)
    doc_ref.delete()

    return (jsonify({"message": "Charada deletada com sucesso!"}), 200)


# ----- ROTAS DE TRATAMENTO DE ERRO -----


@app.errorhandler(404)
def error404(error):
    return jsonify({"error": "URL não encontrada"}), 404

@app.errorhandler(500)
def error500(error):
    return jsonify({"error": "Servidor interno com falhas. Tente mais tarde!"}), 500


if __name__ == "__main__":
    app.run(debug=True)
