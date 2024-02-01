from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from random import choice

fake = Faker()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import your models after creating the Flask app and SQLAlchemy instance
from models import Power, Hero, HeroPower

fake = Faker()

def generate_fake_powers(num_powers=10):
    powers = []
    for _ in range(num_powers):
        power = Power(
            name=fake.word(),
            description=fake.sentence()
        )
        powers.append(power)
    db.session.add_all(powers)
    db.session.commit()

def generate_fake_heroes(num_heroes=10):
    heroes = []
    for _ in range(num_heroes):
        hero = Hero(
            name=fake.first_name(),
            super_name=fake.word()
        )
        heroes.append(hero)
    db.session.add_all(heroes)
    db.session.commit()

def generate_fake_hero_powers(num_connections=20):
    hero_powers = []
    for _ in range(num_connections):
        hero_id = choice(db.session.query(Hero.id).all())[0]
        power_id = choice(db.session.query(Power.id).all())[0]
        strength = fake.word()
        hero_power = HeroPower(
            hero_id=hero_id,
            power_id=power_id,
            strength=strength
        )
        hero_powers.append(hero_power)
    db.session.add_all(hero_powers)
    db.session.commit()

if __name__ == '__main__':

# Create tables
    with app.app_context():
        db.create_all()

        # Generate fake data
        generate_fake_powers()
        generate_fake_heroes()
        generate_fake_hero_powers()