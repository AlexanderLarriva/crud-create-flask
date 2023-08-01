from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
import os

from crud_create_flask_3107.repository import PostsRepository
from crud_create_flask_3107.validator import validate

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/posts')
def posts_get():
    repo = PostsRepository()
    messages = get_flashed_messages(with_categories=True)
    posts = repo.content()
    return render_template(
        'posts/index.html',
        posts=posts,
        messages=messages,
        )


# BEGIN (write your solution here)
@app.route('/posts/new')
def new_post():
    post = []
    errors = []

    return render_template(
        'posts/new.html',
        post=post,
        errors=errors,
        )


@app.post('/posts')
def add_post():
    repo = PostsRepository()
    data = request.form.to_dict()
    errors = validate(data)
    if errors:
        return render_template(
            'posts/new.html',
            post=data,
            errors=errors,
        ), 422

    repo.save(data)
    flash('Post has been created', 'success')

    return redirect(url_for('posts_get'))

# END
