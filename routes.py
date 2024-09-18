from flask import request, jsonify
from app import app, db
from models import User, Post
from schemas import UserSchema, PostSchema

# Инициализация схем для сериализации
user_schema = UserSchema()
users_schema = UserSchema(many=True)
post_schema = PostSchema()
posts_schema = PostSchema(many=True)

# Работа с пользователями
@app.route('/users', methods=['POST'])
def create_user():
    username = request.json['username']
    email = request.json['email']
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)

# Работа с постами
@app.route('/posts', methods=['POST'])
def create_post():
    title = request.json['title']
    content = request.json['content']
    user_id = request.json['user_id']
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return post_schema.jsonify(new_post)

@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get(id)
    if post:
        return post_schema.jsonify(post)
    return jsonify({"message": "Post not found"}), 404

@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = Post.query.get(id)
    if post:
        post.title = request.json.get('title', post.title)
        post.content = request.json.get('content', post.content)
        db.session.commit()
        return post_schema.jsonify(post)
    return jsonify({"message": "Post not found"}), 404

@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return post_schema.jsonify(post)
    return jsonify({"message": "Post not found"}), 404

