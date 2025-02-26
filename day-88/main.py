import random
from flask import Flask, flash, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, select
import os

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass


path = os.path.abspath("day-88/instance/cafes.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path}'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    # Realizamos la consulta a la base de datos
    result = db.session.execute(select(Cafe))
    
    # Obtenemos todos los cafés
    all_cafes = result.scalars().all()
    
    # Seleccionamos un café aleatorio
    random_cafe = random.choice(all_cafes)
    
    # Formateamos la respuesta como HTML (o como prefieras)
    return jsonify(cafe={
        "id": random_cafe.id,
        "name": random_cafe.name,
        "map_url": random_cafe.map_url,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,
        "seats": random_cafe.seats,
        "has_toilet": random_cafe.has_toilet,
        "has_wifi": random_cafe.has_wifi,
        "has_sockets": random_cafe.has_sockets,
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price,
    })

@app.route("/all", methods = ['GET'])
def getAll():
    result = db.session.execute(select(Cafe))
    result = result.scalars().all()
    cafes = result
    print(cafes)
    return render_template('information.html', cafes = cafes)


@app.route("/search/<location>")
def find_coffee_by_location(location):
    result = db.session.execute(select(Cafe).filter(Cafe.location == str(location) ))    
    result = result.scalars().all()
    cafes ={cafe.id:
            {
                "id": cafe.id,
                "name": cafe.name,
                "map_url": cafe.map_url,
                "img_url": cafe.img_url,
                "location": cafe.location,
                "seats": cafe.seats,
                "has_toilet": cafe.has_toilet,
                "has_wifi": cafe.has_wifi,
                "has_sockets": cafe.has_sockets,
                "can_take_calls": cafe.can_take_calls,
                "coffee_price": cafe.coffee_price,
            }
        for cafe in result
    }
    return cafes



@app.route("/add", methods= ['POST', 'GET'])       
def post_new_cafe():
    if request.method == 'POST':
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        flash("Account created successfully!", "success")
        db.session.add(new_cafe)
        db.session.commit()
        return render_template('add.html')
    return render_template('add.html')


@app.route("/update-price/<cafe_id>/<new_price>")
def updatePrice(cafe_id, new_price):
    result = db.session.execute(select(Cafe).filter(Cafe.id == str(cafe_id) ))    
    result = result.scalars().first()
    result.coffee_price = (new_price)
    db.session.commit()
    
    return jsonify(response={"success": "Successfully uptaded the  cafe."})


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE", 'GET'])
def delete_cafe(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
    return redirect(url_for('getAll')) 
    

if __name__ == '__main__':
    app.run(debug=True)
