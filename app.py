from flask import Flask, render_template, request, redirect, flash, url_for, jsonify, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from dotenv import load_dotenv


# ✅ Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# ✅ Use secret key from .env
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "fallback-secret-key")

# ✅ Use database URL from .env

basedir = os.path.abspath(os.path.dirname(__file__))  # Get absolute project path
db_path = os.path.join(basedir, "instance", "site.db")  # Set full DB path
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"  # Use absolute path


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


# ✅ Create directories if they don't exist
if not os.path.exists("static/assets"):
    os.makedirs("static/assets")


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(10), nullable=False, default="other")
    avatar = db.Column(db.String(300), nullable=True)


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(300), nullable=True)


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# 📌 Home Page
@app.route("/")
def home():
    return render_template("index.html")


# 📌 Topic Page
@app.route("/topic/<int:topic_id>")
def topic_page(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    return render_template("topic.html", topic=topic)


# 📌 Profile Page
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_user.full_name = request.form["full_name"]
        current_user.gender = request.form["gender"]

        if current_user.gender == "male":
            current_user.avatar = "/static/assets/default_avatar_male.png"
        elif current_user.gender == "female":
            current_user.avatar = "/static/assets/default_avatar_female.png"
        else:
            current_user.avatar = "/static/assets/default_avatar_other.png"

        if request.form["password"]:
            current_user.password = generate_password_hash(request.form["password"])

        db.session.commit()

        session["profile_success"] = "✅ Промените са запазени!"

        return redirect(url_for("profile"))

    success_message = session.pop("profile_success", None)

    favorite_topics = Favorite.query.filter_by(user_id=current_user.id).all()
    topics = [Topic.query.get(fav.topic_id) for fav in favorite_topics]

    return render_template("profile.html", user=current_user, topics=topics, success_message=success_message)


@app.route('/profile', methods=['POST'])
def update_profile():
    # ... код за обработка на профила
    flash('✅ Промените са запазени!', 'profile')
    return redirect('/profile')


# 📌 Registration
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        gender = request.form["gender"]

        # ✅ Проверка дали имейлът вече съществува
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("❌ Акаунт с този имейл вече съществува!", "danger")  # ЧЕРВЕНО
            return redirect(request.referrer)

        # ✅ Автоматично задаване на аватар
        avatar = f"/static/assets/default_avatar_{gender}.png"

        # ✅ Създаване на нов потребител
        new_user = User(full_name=full_name, email=email, password=password, gender=gender, avatar=avatar)
        db.session.add(new_user)
        db.session.commit()

        # ✅ Flash съобщение за успешна регистрация
        flash("✅ Регистрацията е успешна! Влезте в профила си.", "success")  # ЗЕЛЕНО
        return redirect(url_for("login"))

    return render_template("signup.html")


# 📌 Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect("/")

        flash("❌ Невалиден имейл или парола!", "danger")

    return render_template("login.html")


# 📌 Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


# 📌 Add to Favorites
@app.route("/favorite/<int:topic_id>", methods=["POST"])
@login_required
def add_favorite(topic_id):
    existing_fav = Favorite.query.filter_by(user_id=current_user.id, topic_id=topic_id).first()
    if existing_fav:
        return jsonify({"message": "❗ Вече е в любими!"})

    favorite = Favorite(user_id=current_user.id, topic_id=topic_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "✅ Добавено в любими!"})


# 📌 Remove from Favorites
@app.route("/favorite/remove/<int:topic_id>", methods=["POST"])
@login_required
def remove_favorite(topic_id):
    favorite = Favorite.query.filter_by(user_id=current_user.id, topic_id=topic_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "❌ Премахнато от любими!"})
    return jsonify({"message": "❗ Темата не беше намерена в любими!"})


# 📌 Contact Form
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        new_message = ContactMessage(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()

        # ✅ Use a category "success" instead of "contact"
        flash("✅ Вашето съобщение е изпратено успешно!", "success")
        return redirect(url_for("contact"))  # Use url_for() to prevent hardcoded URLs

    return render_template("contact.html", messages=get_flashed_messages(with_categories=True))




# 📌 About Page
@app.route("/about")
def about():
    return render_template("about.html")


# 📌 404 Error Page
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


# 📌 Initialize Database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
