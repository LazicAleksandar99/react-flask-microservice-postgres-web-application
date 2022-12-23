from app.extensions import db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from app.models.product import Product, ProductSchema
from app.models.user import User, UserSchema
from flask_cors import cross_origin

bp_products = Blueprint('products', __name__, url_prefix='/product')

product_schema = ProductSchema
products_schema = ProductSchema(many=True)

@bp_products.route('/add', methods=['POST'])
@cross_origin()
@jwt_required()
def add_product():

    current_user = get_jwt_identity()
    #provjera da li je ROLE ADMIN
    name = request.json['name']
    description = request.json['description']
    picture = request.json['picture']
    price = request.json['price']
    #owner_id = request.json['owner_id']

    user = User.query.filter_by(email=current_user).first()
    
    new_product = Product(name, description, picture, price, user.account_id)

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"created": "New product succesfuly created"}, 201)


@bp_products.route('/all', methods=['GET'])
@cross_origin()
@jwt_required()
def get_all_products():

    current_user = get_jwt_identity()
    #dalje s ovim treba provjera da li customer ili admin.... 
    products = Product.query.all()
    all_products = products_schema.dump(products) # mora shema jer preko query.all ne moze jesinify
    return jsonify(products = all_products)