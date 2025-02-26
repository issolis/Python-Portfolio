import random
from flask import Flask, flash, jsonify, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, select
import os
from datetime import datetime

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass

path = os.path.abspath("day-89/instance/database.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "supersecretkey"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(db.Model): 
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    activities = relationship("Activity", back_populates="user")

class Activity(db.Model): 
    __tablename__ = "activities"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    activity: Mapped[str] = mapped_column(String(255), nullable=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False)

    user = relationship("User", back_populates="activities")

with app.app_context():
    db.create_all()

@app.route("/")
def home(): 
    return render_template('index.html')


@app.route("/signup", methods = ['GET', 'POST'])
def signUp():
    if request.method == 'POST': 
        email = request.form.get('email')
        password = request.form.get('password')

        result = db.session.execute(select(User).filter(User.email == str(email) )) 
        if (result.scalar_one_or_none()): 
              flash("Account already exists!", "danger") 
              return render_template('signup.html')

        newUser = User(
            email = email, 
            password = password
        )

        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('signup.html') 

@app.route('/login', methods = ['POST', 'GET'])
def login(): 
    if request.method == 'POST': 
        email = request.form.get('email')
        pasword = request.form.get('password')

        user = db.session.execute(select(User).filter(User.email == str(email) )).scalar_one_or_none()
        if not user: 
            flash("Your email doesn't exist! Sign-up!", "danger")
            return render_template('index.html')
        if user.password != pasword: 
            flash("Your password does not match your email", "danger")
            return render_template('index.html')
        
        session["user_email"] = email
        return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    if "user_email" not in session:
        flash("you must first log in", "danger")
        return redirect(url_for("home"))

    return render_template("dashboard.html", email=session["user_email"])


@app.route("/logout")
def logout():
    session.pop("user_email", None)
    flash("You have logged out", "info")
    return redirect(url_for("home"))
@app.route("/list", methods = ['POST', 'GET'])
def list(): 
    email = request.form.get("email")  
    selected_date = request.form.get("selected_date") 
    if not email: 
        email = request.args.get("email")  
        selected_date = request.args.get("date") 

    date = datetime.strptime(selected_date, "%Y-%m-%d")

    user = db.session.execute(select(User).filter(User.email == str(email) )).scalar_one_or_none()
    activities = db.session.execute(select(Activity).filter(Activity.user_id == user.id, Activity.date == date)).scalars().all()



    if "user_email" not in session:
        flash("Please, You must first log in", "warning")
        return redirect(url_for('home'))
    


    return render_template("activities.html", email = email, date = selected_date, activities = activities)

@app.route("/add", methods = ['POST'])
def add(): 
    if "user_email" not in session:
        flash("Please, You must first log in", "warning")
        return redirect(url_for('home'))
    
    email = request.form.get("email")  
    print(email)
    dateStr = request.form.get("date")
    date = datetime.strptime(dateStr, "%Y-%m-%d")
    activity = request.form.get("activity")

    user = db.session.execute(select(User).filter(User.email == str(email) )).scalar_one_or_none()
    newActivity =Activity(
        user_id = user.id, 
        date = date, 
        activity = activity, 
        done = False
    )



    activities = db.session.execute(select(Activity).filter(Activity.user_id == user.id)).scalars().all()
    db.session.add(newActivity)
    db.session.commit()

    return redirect(url_for("list", email=email, date=dateStr, activities = activities))

@app.route("/markDone/<id>")
def markDone(id):
    if "user_email" not in session:
        flash("Please, You must first log in", "warning")
        return redirect(url_for('home'))
    activity = db.session.execute(select(Activity).filter(Activity.id == int(id) )).scalar_one_or_none()
    activity.done = True 
    db.session.commit()

    user = db.session.execute(select(User).filter(User.id == str(activity.user_id) )).scalar_one_or_none()
    
   
    return redirect(url_for("list", email=user.email, date=activity.date.strftime("%Y-%m-%d")))


@app.route("/delete/<id>")
def delete(id):
    if "user_email" not in session:
        flash("Please, You must first log in", "warning")
        return redirect(url_for('home'))
    activity = db.session.execute(select(Activity).filter(Activity.id == int(id) )).scalar_one_or_none()
    db.session.delete(activity) 
    db.session.commit()

    user = db.session.execute(select(User).filter(User.id == str(activity.user_id) )).scalar_one_or_none()
    
   
    return redirect(url_for("list", email=user.email, date=activity.date.strftime("%Y-%m-%d")))






    



if __name__ == '__main__':
    app.run(debug=True)



