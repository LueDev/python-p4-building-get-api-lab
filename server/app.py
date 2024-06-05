#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/', methods=['GET'])
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods=['GET'])
def bakeries():
    bakeries = Bakery.query.all()
    body = jsonify([bakery.to_dict() for bakery in bakeries])
    return make_response(body, 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    
    if bakery:
        body = bakery.to_dict()
        status = 200
    else:
        body = {'message': f'Bakery {id} not found.'}
        status = 404

    # body = jsonify([bakery.to_dict() for bakery in bakery])
    return make_response(body, status)
    

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = db.session.query(BakedGood).join(Bakery).order_by(desc(BakedGood.price)).all()
    body = jsonify([bg.to_dict() for bg in baked_goods])
    return make_response(body, 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_baked_good = db.session.query(BakedGood).order_by(desc(BakedGood.price)).first()
    if most_expensive_baked_good:
        body = jsonify(most_expensive_baked_good.to_dict())
        return make_response(body, 200)
    else:
        return make_response(jsonify({"error": "No baked goods found"}), 404)
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)
