from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from mongoengine import connect
from models.models import User
from routes.authentication import login_bp, signup_bp
from extension import bcrypt, jwt

app = Flask(__name__)
CORS(app)

bcrypt.init_app(app)

jwt.init_app(app)
app.config['JWT_SECRET_KEY'] = 'pls-select-yaswanth-**cute-cat-image**'

connect(db='NotFable', host='mongodb+srv://yaswanth:yaswanth@cluster0.szqvpi1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

app.register_blueprint(login_bp, url_prefix= '/api')
app.register_blueprint(signup_bp, url_prefix= '/api')


if __name__ == '__main__':
    app.run(port=5000)