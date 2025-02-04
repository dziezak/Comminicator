from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://korne:Kornel2012!@localhost/chatdb'
app.config['SECRET_KEY'] = 'tajny_klucz'
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@socketio.on('message')
def handle_message(data):
    msg = Message(sender_id=data['sender_id'], receiver_id=data['receiver_id'], content=data['content'])
    db.session.add(msg)
    db.session.commit()
    send(data, broadcast=True)  # Wysyłamy do wszystkich (lub można ograniczyć do konkretnego usera)

if __name__ == '__main__':
    db.create_all()
    socketio.run(app, debug=True)
