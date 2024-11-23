from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import re
import jwt  
import os
import datetime
from utils.connection import get_db_connection  # Adjust based on your project structure

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS for all routes

# Secret key for encoding the JWT
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")  # Use environment variable for secret key

# Validation function for password strength
def is_password_strong(password):
    if (len(password) >= 8 and re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and re.search(r"[0-9]", password) and
        re.search(r"[!@#$%^&*()_+=\-]", password)):
        return True
    return False

# JWT decoding function
def decode_jwt_token(token):
    try:
        return jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Registration endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    firstname = data.get('firstName')
    lastname = data.get('lastName')
    account_type = data.get('accountType')
    email = data.get('email')
    mobile_no = data.get('mobileNo')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')

    if not all([firstname, lastname, account_type, email, mobile_no, password, confirm_password]):
        return jsonify({"error": "All fields are required"}), 400

    if not is_password_strong(password):
        return jsonify({"error": "Password is too weak"}), 400

    if password != confirm_password:
        return jsonify({"error": "Password and confirm password should be the same!"}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users WHERE email = %s", (email,))
        existing_user = cur.fetchone()
        if existing_user:
            return jsonify({"error": "Email already registered"}), 400

        cur.execute("""
            INSERT INTO Users (firstname, lastname, account_type, email, mobile_no, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (firstname, lastname, account_type, email, mobile_no, hashed_password))

        conn.commit()
        return jsonify({"message": "User  registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users WHERE email = %s", (email,))
        user = cur.fetchone()

        if user and check_password_hash(user[6], password):  # Assuming password hash is stored in the 6th column
            token = jwt.encode({
                'user_id': user[0],
                'email': email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm="HS256")

            user_details = {
                "id": user[0],
                "firstname": user[ 1],
                "lastname": user[2],
                "account_type": user[3],
                "email": user[4],
                "mobile_no": user[5],
                "profile_photo": user[7],
                "country": user[8],
                "working_domain": user[9],
                "technical_skills": user[10],
                "work_experience": user[11],
                "educational_details": user[12],
                "hourly_rate": user[13],
                "social_media_links": user[14],
                "connects": user[15]
            }

            response = make_response(jsonify({"message": "Login successful", "user": user_details}), 200)
            response.set_cookie('token', token, httponly=True, secure=True, max_age=datetime.timedelta(hours=1))
            return response
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Logout endpoint
@app.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({"message": "Logout successful"}), 200)
    response.set_cookie('token', '', httponly=True, secure=True, expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True)