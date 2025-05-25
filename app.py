from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, current_user
from models.user import User
from database import db


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
#view login
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("passwor")
    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and user.passwor == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message":"Autenticacao com sucesso"}),200
    return jsonify({"message":"Credenciais invalidas"}),400


@app.route("/hello", methods=["GET"])
def hello():
    return "Hello"

if __name__ == '__main__':
    app.run(debug=True)