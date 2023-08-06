import os

from flask import Flask, request
from flask_smorest import Api, Blueprint
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from insecure_api.models import Product

db_uri = os.getenv("DB_URI")

assert db_uri is not None, "Need to provide DB_URI environment variable"

session_maker = sessionmaker(bind=create_engine(db_uri))


server = Flask(__name__)
api = Api(server, spec_kwargs={"title": "Products API", "version": "v1", "openapi_version": "3.1"})

bp = Blueprint("products", __name__)


@server.get("/categories")
def list_categories():
    with session_maker() as session:
        categories = session.query(Product.category).distinct()
    return {
        "categories": [category[0] for category in categories]
    }  # "1' OR 1=1 --"


@server.get("/products")
def list_products_without_validating_query_params_and_no_sql_parametrization():
    with session_maker() as session:
        products = session.execute(
            text(f"select * from product where category = '{request.args.get('category', 'shoes')}'")
        )
    return {
        "products": [{
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "category": product.category
        } for product in products]
    }


@server.post("/categories")
def create_category_without_validating_payload():
    """
    schema for the payload:
    Category:
      name:
        type: string
      products:
        type: array
        items:
          $ref: '#/components/schemas/Product'
    Product:
      name:
        type: string
      price:
        type: number
    """

    payload = request.json
    with session_maker() as session:
        pass





# BAD ONES:
# - non-robust validation of query params:
#   > not checking for ony-allowed parameters
#   > not validating their types strictly
#   > not validating their possible values
# - non-validated payloads
# - non-robust validation of payloads
# - payloads with bad design
# - undocumented endpoints
# - too much exposure of IDs through payloads allowing to explore for undocumented resource URLs
# - allow editing resources that I haven't created
# - sql injection
# - unauthenticated endpoints when it should
# - not validating token's signature
# - allow client to set token's signature to None, noNe, none, False, etc.
# - using token signatures
# - no rate limiting
