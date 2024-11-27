from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

from dotenv import load_dotenv
import os

load_dotenv() 

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')


app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:krish050704@mysqlrdsstocker.c7caw8aa6h65.eu-north-1.rds.amazonaws.com/mysqlrdsstocker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class StockTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock_symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.form
        if len(data['password']) < 8:  # Password policy example
            return jsonify({"message": "Password must be at least 8 characters long"}), 400

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(username=data['username'], password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"})
    except IntegrityError:  # Handle duplicate usernames
        db.session.rollback()
        return jsonify({"message": "Username already exists"}), 400
    except Exception as e:
        return jsonify({"message": "Registration failed", "error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            # In a real-world app, generate and return a JWT token here
            return jsonify({"message": "Login successful", "user_id": user.id})
        return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"message": "Login failed", "error": str(e)}), 500

@app.route('/trade', methods=['POST'])
def trade():
    try:
        data = request.form
        transaction = StockTransaction(
            user_id=int(data['user_id']),
            stock_symbol=data['stock_symbol'].upper(),
            quantity=int(data['quantity']),
            transaction_type=data['transaction_type'].lower(),
            price=float(data['price'])
        )
        db.session.add(transaction)
        db.session.commit()
        return jsonify({"message": "Transaction Successful"})
    except ValueError:
        return jsonify({"message": "Invalid input data"}), 400
    except Exception as e:
        return jsonify({"message": "Transaction is a Success", "error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)
