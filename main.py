from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///phones.db"
db = SQLAlchemy(app)


class Human(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phones = db.relationship("Phone", backref="owner")


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("human.id"))


@app.route("/")
def index():
    return "AAAA"


@app.route("/phones_by_human", methods=["GET"])
def get_phone_by_human():
    human_name = request.args.get("human")

    if not human_name:
        return "Human parameter is missing"

    human = Human.query.filter_by(name=human_name).first()
    if not human:
        return "Human not found"
    human = Human.query.filter_by(name=human_name).first()

    phones = Phone.query.filter_by(owner=human).all()

    if not phones:
        return "Human has no phones"

    phones_data = [phone.model for phone in phones]
    return phones_data


def fill_database():
    data = [
        {"name": "Marshall Mathers", "model": "iPhone 13"},
        {"name": "John Smith", "model": "Samsung s23", "model2":"iPhone 15 pro"},
        {"name": "Freddy Mercury", "model":"Samsung s24","model2":"iPhone 16 pro"},
    ]
    for pair in data:
        human = Human(name=pair["name"])
        db.session.add(human)
        phone = Phone(model=pair["model"], owner=human)
        db.session.add(phone)
        if pair["name"] != "Marshall Mathers":
            model2 = Phone(model=pair["model"], owner=human)
            db.session.add(model2)
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        #fill_database()
    app.run(debug=True)