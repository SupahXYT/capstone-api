from flask import Flask, jsonify, request
from mongoengine import Document, StringField, connect
from flask_jwt_extended import (
create_access_token,
get_jwt_identity,
jwt_required,
JWTManager
)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = 'mango'
jwt = JWTManager(app)


class User(Document):
    username = StringField()
    password = StringField()


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.objects(username=username).first()
    if user:
        if user.password == password:
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token)
    return jsonify({'msg': "Invalid username or password"})


@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if User.objects(username=username).first():
        return jsonify({'msg': 'User already exists'})
    user = User(username=username, password=password)
    user.save()
    return jsonify({'msg': 'ok'})


@app.route('/list', methods=['get'])
@jwt_required()
def list_user():
    current_user = get_jwt_identity()
    return current_user


if __name__ == '__main__':
    _username = 'azuma'
    _password = 'CotGiQnKX1hQGbkjw4JlIpEyE6mvqwto'
    connect('myFirstDatabase',
            host=f'mongodb+srv://{_username}:{_password}@cluster0.9amyl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    app.run(port=8008, debug=True)
