from flask import render_template,url_for,redirect,request,abort,flash,Blueprint
from flaskblog.models import Post
from flaskblog.posts.forms import NewPostForm
from flask_login import current_user,login_required
from flaskblog import db



posts = Blueprint("posts", __name__)

@posts.route("/post/new", methods = ["GET","POST"])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        long_post = True
        if len(form.content.data)<250:
            long_post = False
        post = Post(title = form.title.data, content = form.content.data , author = current_user, long_post = long_post)
        db.session.add(post)
        db.session.commit()
        flash("Post Added", "success")
        return redirect(url_for("main.home"))
    return render_template("create_update_post.html", title = "New Post", form = NewPostForm())

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title = post.title, post = post)


@posts.route("/post/<int:post_id>/update", methods = ["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = NewPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Yout Post has been updated", "success")
        return redirect(url_for("posts.post", post_id = post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        return render_template("create_update_post.html", title = "Update Post", form = form)


@posts.route("/post/<int:post_id>/delete", methods = ["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted", "success")
    return redirect(url_for("main.home"))

