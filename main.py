from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Cafe TABLE Configuration


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

# db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/all')
def get_all():
    cafes = db.session.query(Cafe).all()
    # using list comprehension, karena kita mau return semua data dalam bentuk list
    return jsonify(cafe=[cafe.to_dict() for cafe in cafes])


# HTTP GET - Read Record
@app.route('/random')
def get_random():
    cafe = db.session.query(Cafe).all()
    random_cafe = random.choice(cafe)
    return jsonify(cafe=random_cafe.to_dict())



# HTTP GET - SEARCH RECORD
@app.route('/search')
def search_data():
    loc = request.args.get('loc')
    get_data = Cafe.query.filter_by(location=loc).first()
    if get_data:
        return jsonify(get_data.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, we can't find cafe at that location"})

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
