from dotenv import load_dotenv
import os 
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import func
from flask_cors import CORS

# config app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class BlogModel(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    tags = db.Column(JSONB)
    date_created = db.Column(db.DateTime(), default=func.now())

    def __init__(self, title, content, tags):
        self.title = title
        self.content = content
        self.tags = tags

    def __repr__(self):
        return f"<Post {self.title}>"

# make route!
@app.route('/')
def hello_world():
  return {"Goodbye":"world"}

@app.route('/posts', methods=['POST', 'GET'])
def handle_posts():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_post = BlogModel(title=data['title'], content=data['content'], tags=data['tags'])
            db.session.add(new_post)
            db.session.commit()
            return {"message": f"post {new_post.title} has been created successfully."}
        else:
            return{"error": "the request payload is not in JSON format"}

    elif request.method == 'GET':
        posts = BlogModel.query.order_by(BlogModel.id.desc()).all()
        results = [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "tags": post.tags,
                "created": post.date_created,
            } for post in posts]

        return {"count": len(results), "posts": results}

@app.route('/posts/<int:post_id>', methods=['GET'])
def show_post(post_id):
    post = BlogModel.query.get_or_404(post_id)
    response = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "tags": post.tags,
        "created": post.date_created,
    }
    return {"post": response}

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = BlogModel.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return{"message": f"Post {post.title} successfully deleted"}

@app.route('/posts/<int:post_id>', methods=['PUT'])
def edit_post(post_id):
    post = BlogModel.query.get_or_404(post_id)
    data = request.get_json()
    post.title = data['title']
    post.content = data['content']
    post.tags = data['tags']
    db.session.add(post)
    db.session.commit()
    return {"message": f"Post {post.title} successfully updated"}