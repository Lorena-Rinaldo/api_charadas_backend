from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])

def root():
    return "API TÁ ON"

if __name__ == "__main__":
    app.run(debug=True)