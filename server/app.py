#!/usr/bin/env python3

from flask import Flask, make_response,request,jsonify
from flask_migrate import Migrate
from flask_restful import Api,Resource
from models import db, Hero,Power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
api=Api(app)

class Heroes(Resource):
    def get(self):
        hero = [{"id":hero.id,"name":hero.name,"super_name":hero.super_name}for hero in Hero.query.all()]
        return make_response(jsonify(hero),200)
api.add_resource(Heroes,"/heroes")

class HeroesById(Resource):
    def get (self,id):
        hero = Hero.query.filter_by(id=id).first()

        if not hero:
            return make_response(jsonify({"message": "hero not found"}))
        hero_data={
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers":[]
        }

        for power in hero.powers:
            power_data={
                "id":power.id,
                "name":power.name,
                "description":power.description
            }
        hero_data["powers"].append(power_data)
        return make_response(jsonify(hero_data),200)
api.add_resource(HeroesById,"/heroes/<int:id>")

class powers(Resource):
    def get(self):
        power= [{"id":power.id,"name":power.name,"description":power.description} for power in Power.query.all()]
        return make_response(jsonify(power),200)
api.add_resource(powers,"/powers")
class powersById(Resource):
    def get(self,id):
        power =Power.query.filter_by(id=id).first()
        if not power:
            return make_response(jsonify({"message":"power not found"}))
        power_data={
            "id":power.id,
            "name":power.name,
            "description":power.description
        }
        return make_response(jsonify(power_data),200)
    def patch(self,id):
        power=Power.query.filter_by(id=id).first()

        if not power:
            return make_response(jsonify({"message":"power not found"}))
        if "description" in request.json:
            power.description = request.json["description"]
            db.session.commit()
            return make_response(jsonify({
                "id":power.id,
                "name":power.name,
                "description":power.description
            }),200)
        else:
            return make_response(jsonify({"errors":["description not provided"]}),400)

api.add_resource(powersById,"/powers/<int:id>")

if __name__ == '__main__':
    app.run(port=5555,debug=True)
