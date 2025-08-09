# from flask import Flask, render_template, request, redirect,session,url_for
# # import mysql.connector
# import requests
# from werkzeug.security import generate_password_hash,check_password_hash
# import os
# import pymysql
# pymysql.install_as_MySQLdb()
# import hashlib
# print(dir(hashlib))
# import werkzeug.security
# print(werkzeug.security._hash_internal.__code__.co_consts)


# import MySQLdb  # Now works via PyMySQL


# print(os.urandom(15))

# app = Flask(__name__)

# app.secret_key = b'\xc5\x12Ub\xe1\xf8TT_\x1f"\xaa\xa5\x89\x1b'.hex()

# # MySQL setup
# # db = mysql.connector.connect(
# #     host="localhost",
# #     user="root",
# #     password="Rohith@007",
# #     database="weather"
# # )
# # cursor = db.cursor(dictionary=True)


# db = pymysql.connect(
#     host="localhost",
#     user="root",
#     password="Rohith@007",
#     database="weather",
#     cursorclass=pymysql.cursors.DictCursor
# )
# cursor = db.cursor()


# # OpenWeatherMap API
# api_key = "00cb2e9f246e6c80dfe87e4ec49324ae"
# base_url = "http://api.openweathermap.org/data/2.5/weather?"

# @app.route('/')

# def home():
#     if 'user' in session:
#         return redirect(url_for('index'))
#     return redirect(url_for('login'))

# @app.route('/login', methods=['GET', 'POST'])

# def login():
#     error = None
#     if request.method == 'POST':

#         username = request.form['username']
#         password = request.form['password']

#         cursor.execute ("select * from users where username =%s",(username,))
#         user = cursor.fetchone()

#         if user and check_password_hash (user['password'],password):
#             session['user'] = user['username']
#             return redirect(url_for('index'))
#         else:
#             error = 'invalid credentials'

#     return render_template('login.html',error=error)

# @app.route('/register', methods=['GET', 'POST'])

# def register():
#     error = None
#     if request.method == 'POST':

#         username = request.form['username']
#         password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')


#         try:
#             cursor.execute("insert into users (username,password) values (%s,%s)",(username,password))
#             db.commit()
#             return redirect(url_for('login'))
#         except pymysql.connector.IntegrityError:
#             error = "Username already exists"
#     return render_template('register.html',error =error)

# @app.route('/logout')
# def logout():
#     session.pop('user',None)
#     return redirect(url_for('login'))


# @app.route('/index', methods=['GET', 'POST'])
# def index():

#     if 'user' not in session:
#         return redirect(url_for('login'))

#     weather_data = None
#     error = None

#     if request.method == 'POST':
#         city = request.form.get('city')

#         params = {
#             'q': city,
#             'appid': api_key,
#             'units': 'metric'
#         }

#         response = requests.get(base_url, params=params)

#         if response.status_code == 200:
#             data = response.json()
#             main = data['main']
#             weather = data['weather'][0]
#             lat = data['coord']['lat']
#             lon = data['coord']['lon']

#             weather_data = {
#                 'city': data['name'],
#                 'condition': weather['description'].capitalize(),
#                 'temperature': main['temp'],
#                 'humidity': main['humidity'],
#                 'latitude': lat,
#                 'longitude': lon
#             }

#             # Insert into MySQL
#             insert_query = """
#                 INSERT INTO weather_data (city, `condition`, temperature, humidity, latitude, longitude)
#                 VALUES (%s, %s, %s, %s, %s, %s)
#             """
#             values = (
#                 weather_data['city'],
#                 weather_data['condition'],
#                 weather_data['temperature'],
#                 weather_data['humidity'],
#                 weather_data['latitude'],
#                 weather_data['longitude']
#             )

#             cursor.execute(insert_query, values)
#             db.commit()

#         else:
#             error = "City not found. Please try again."

#     return render_template('index.html', weather=weather_data, error=error, user=session['user'])

# if __name__ == '__main__':
#     app.run(debug=True)




import requests
from flask import Flask, render_template, request, redirect, session, url_for
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
import os

pymysql.install_as_MySQLdb()
import MySQLdb

app = Flask(__name__)
app.secret_key = os.urandom(15).hex()

# MySQL setup
db = pymysql.connect(
    host="localhost",
    user="root",
    password="Rohith@007",
    database="weather",
    cursorclass=pymysql.cursors.DictCursor
)
cursor = db.cursor()

# API keys
api_key = "00cb2e9f246e6c80dfe87e4ec49324ae"  # OpenWeather
unsplash_key = "-rWnPswTqr3hjW7sJy22wKYzqEFHEz-LbHK0UMC6e9s"     # Unsplash

base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Function to get city image
def get_city_image(city):
    try:
        url = f"https://api.unsplash.com/photos/random?query={city}&orientation=landscape&client_id={unsplash_key}"
        response = requests.get(url).json()
        return response["urls"]["full"]
    except:
        return "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee"

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("select * from users where username =%s", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], password):
            session['user'] = user['username']
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        try:
            cursor.execute("insert into users (username,password) values (%s,%s)", (username, password))
            db.commit()
            return redirect(url_for('login'))
        except pymysql.IntegrityError:
            error = "Username already exists"
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    weather_data = None
    error = None
    background_url = "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee"

    if request.method == 'POST':
        city = request.form.get('city')

        params = {'q': city, 'appid': api_key, 'units': 'metric'}
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            main = data['main']
            weather = data['weather'][0]
            lat = data['coord']['lat']
            lon = data['coord']['lon']

            weather_data = {
                'city': data['name'],
                'condition': weather['description'].capitalize(),
                'temperature': main['temp'],
                'humidity': main['humidity'],
                'latitude': lat,
                'longitude': lon
            }

            background_url = get_city_image(city)

            insert_query = """
                INSERT INTO weather_data (city, `condition`, temperature, humidity, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                weather_data['city'],
                weather_data['condition'],
                weather_data['temperature'],
                weather_data['humidity'],
                weather_data['latitude'],
                weather_data['longitude']
            )
            cursor.execute(insert_query, values)
            db.commit()
        else:
            error = "City not found. Please try again."

    return render_template(
        'index.html',
        weather=weather_data,
        error=error,
        user=session['user'],
        background_url=background_url
    )

if __name__ == '__main__':
    app.run(debug=True)
