from flask import Flask, render_template, request, redirect, jsonify
import psycopg2
from database import get_db_connection
from flask_cors import CORS

# FOR IDIOTS: https://dziezak.github.io/Comminicator/
app = Flask(__name__)
CORS(app)

# Tworzenie tabeli wiadomości w bazie danych (jednorazowo)
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

create_table()

# Strona główna
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint do pobierania wiadomości
@app.route('/messages', methods=['GET'])
def get_messages():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, message, timestamp FROM messages ORDER BY timestamp DESC LIMIT 10;")
    messages = cur.fetchall()
    cur.close()
    conn.close()
    
    #print(f"Wiadomosci: {messages}")
    return jsonify(messages)

# Endpoint do wysyłania wiadomości
@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    username = data.get("username")
    message = data.get("message")

    print(f"Recived message from {username}: {message}")

    if not username or not message:
        print("Brak nazwy uzytkownikach lub wiadomosci")
        return jsonify({"error": "Brak nazwy użytkownika lub wiadomości!"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (username, message) VALUES (%s, %s)", (username, message))
        conn.commit()
        cur.close()
        conn.close()
        print("Wiadomosc dodana pomysle")
    except Exception as e:
        print(f"Blad: {e}")
        return jsonify({"error":"Wystapil blad podczas dodawania wiadomosci."}), 500
    
    return jsonify({"status": "OK"})

# local home:
#if __name__ == '__main__':
#    app.run(debug=True)
# internet:
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
