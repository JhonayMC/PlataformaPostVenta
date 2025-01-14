from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Importando poryecto, hello!!!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
