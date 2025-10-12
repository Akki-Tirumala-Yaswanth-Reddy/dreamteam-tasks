from flask import Flask
from flask_cors import CORS
from mongoengine import connect
from routes.authentication import login_bp, signup_bp
from routes.books import books_bp
from routes.social import social_bp
from routes.reviews import reviews_bp
from routes.readingList import lists_bp
from extension import bcrypt, jwt

app = Flask(__name__)

# I had an error related to CORS, after few days, this seems to fix this(all the extra statements).
CORS(app,
     origins=["http://localhost:3000", "http://127.0.0.1:3000"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True)

bcrypt.init_app(app)

jwt.init_app(app)
app.config['JWT_SECRET_KEY'] = 'pls-select-yaswanth-**cute-cat-image**'

connect(db='NotFable', host='mongodb+srv://yaswanth:yaswanth@cluster0.szqvpi1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

app.register_blueprint(login_bp, url_prefix= '/api/auth')
app.register_blueprint(signup_bp, url_prefix= '/api/auth')
app.register_blueprint(books_bp, url_prefix= '/api/books')
app.register_blueprint(reviews_bp, url_prefix='/api/reviews')
app.register_blueprint(social_bp, url_prefix= '/api/social')
app.register_blueprint(lists_bp, url_prefix= '/api/reading_list')


if __name__ == '__main__':
    app.run(port=5000)