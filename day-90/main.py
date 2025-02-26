from flask import Flask, render_template, redirect, url_for, request, session, flash
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('home.html')

@app.route("/activity", methods=["GET", "POST"])
def activity():
    if 'last_activity' in session:
        current_time = time.time()
        if current_time - session['last_activity'] > 30:  
            session.clear()  
            flash("has been inactive for a long time, redirecting to startup...", "warning")
            return redirect(url_for('home'))  
        

    return render_template('activity.html')

@app.before_request
def update_last_activity():
    session['last_activity'] = time.time()

if __name__ == "__main__":
    app.run(debug=True)
