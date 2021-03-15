from blog.models import User, Post, Comment, Vote, Fave
from flask import render_template, url_for, redirect, request, flash, Blueprint, jsonify
from blog import app, db
from flask_login import login_user, logout_user, current_user, login_required
from blog.forms import RegistrationForm, LoginForm, CommentForm, SearchForm, VoteForm, FaveForm, SortForm
from sqlalchemy import desc
from datetime import datetime

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    search = SearchForm(request.form)
    if request.method == 'POST':
        print(search.data)
        return search_results(search)
    posts= Post.query.limit(3).all()
    return render_template('home.html', posts=posts, form=search)

@app.route('/results', methods=['GET', 'POST'])
def search_results(search):
    results = []
    search_string = search.data['userquery']

    if search.data['userquery']:
        post = Post.query.filter(Post.title.contains(search_string) | Post.content.contains(search_string))
        results = post.all()
    
    if not results:
        flash('No results found.')
        return redirect('/home')

    else:
        return render_template('results.html', post=post, results=results)


@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    votes = Vote.query.filter(Vote.post_id == post.id)
    comments = Comment.query.filter(Comment.post_id == post.id)
    comment_form = CommentForm()
    vote_form = VoteForm()
    fave_form = FaveForm()
    return render_template('post.html', title=post.title, post=post, comments=comments, votes=votes, comment_form=comment_form, vote_form=vote_form, fave_form=fave_form)

@app.route('/post/<int:post_id>/vote', methods=["GET", "POST"])
@login_required
def upvote(post_id):
    post = Post.query.get_or_404(post_id)
    form = VoteForm()
    if form.validate_on_submit():
        if Vote.query.filter(Vote.vote_id==current_user.id, Vote.post_id==post.id).first() != None:
            flash("You've already vote on this post!")
            return redirect(f'/post/{post.id}')
        x = Vote.query.filter(Vote.post_id == post.id).first()
        x.number = x.number+1
        db.session.add(Vote(number=x.number, post_id=post.id, vote_id=current_user.id))
        db.session.commit()
        flash("Voted")
        return redirect(f'/post/{post.id}')

@app.route('/post/<int:post_id>/downvote', methods=["GET", "POST"])
@login_required
def downvote(post_id):
    post = Post.query.get_or_404(post_id)
    form = VoteForm()
    if form.validate_on_submit():
        if Vote.query.filter(Vote.vote_id==current_user.id, Vote.post_id==post.id).first() != None:
            flash("You've already voted on this post!")
            return redirect(f'/post/{post.id}')
        x = Vote.query.filter(Vote.post_id == post.id).first()
        x.number = x.number-1
        db.session.add(Vote(number=x.number, post_id=post.id, vote_id=current_user.id))
        db.session.commit()
        flash("Voted")
        return redirect(f'/post/{post.id}')

@app.route('/post/<int:post_id>/comment', methods=["GET", "POST"])
@login_required
def post_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        db.session.add(Comment(content=form.comment.data, post_id=post.id, author_id=current_user.id))
        db.session.commit()
        flash("Comment Posted")
        return redirect(f'/post/{post.id}')
    
    comments= Comment.query.filter(comment.post_id == post.id)
    return render_template('post.html', title=post.title, post=post, comments=comments, form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful...')
        return redirect(url_for('newuser'))
    return render_template('register.html', title="Register", form=form)

@app.route("/newuser")
def newuser():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    return render_template('newuser.html', title="Welcome!")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid email address or password...')
    return render_template('login.html', title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/profile/<username>", methods=["GET", "POST"])
@login_required
def profile(username):
    fave_form = FaveForm()
    user = User.query.filter_by(username=username).first()
    if user == None:
        flash('Error, this profile does not exit.')
        return render_template('home.html')
    favourites = Fave.query.filter(Fave.user_id == user.id)
    #favourites = Post.query.filter(Fave.post_id == post.id)
    return render_template('profile.html', user=user, favourites=favourites, fave_form=fave_form)

@app.route("/post/<int:post_id>/favourite/remove", methods=["GET", "POST"])
@login_required
def remove_fave_profile(post_id):
    post = Post.query.get_or_404(post_id)
    form = FaveForm()
    if form.validate_on_submit():
        if Fave.query.filter(Fave.user_id==current_user.id, Fave.favourite==post.id).first() != None:
            Fave.query.filter(Fave.user_id==current_user.id, Fave.favourite==post.id).delete()
            db.session.commit()
            flash("Removed %s from %s's favourites" %(post.title, current_user.username))
            return redirect(f'/profile/{current_user.username}')

@app.route("/post/<int:post_id>/favourite", methods=["GET", "POST"])
@login_required
def add_fave(post_id):
    post = Post.query.get_or_404(post_id)
    form = FaveForm()
    if form.validate_on_submit():
        if Fave.query.filter(Fave.user_id==current_user.id, Fave.favourite==post.id).first() != None:
            Fave.query.filter(Fave.user_id==current_user.id, Fave.favourite==post.id).delete()
            db.session.commit()
            flash("Removed %s from %s's favourites" %(post.title, current_user.username))
            return redirect(f'/post/{post.id}')
        db.session.add(Fave(user_id=current_user.id, favourite=post.id))
        db.session.commit()
        flash("Added %s to %s's favourites" %(post.title, current_user.username))
        return redirect(f'/post/{post.id}')

@app.route('/all-posts/newest', methods=['GET', 'POST'])
def newest_posts():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    posts= Post.query.all()
    return render_template('view-posts.html', posts=posts, form=search)

@app.route('/all-posts/oldest', methods=['GET', 'POST'])
def oldest_posts():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    posts = Post.query.order_by(desc(Post.date)).all()
    return render_template('view-posts-reverse.html', posts=posts, form=search)

# Error Page Handling
@app.errorhandler(401)
def error_401(error):
    flash("Guest accounts cannot access this feature. Please create an account or log-in.")
    return redirect(f'/login')

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html')