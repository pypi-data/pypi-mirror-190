import os
import random

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from insecure_api.models import Product

db_uri = os.getenv("DB_URI")

assert db_uri is not None, "Need to provide DB_URI environment variable"

session_maker = sessionmaker(bind=create_engine(db_uri))

faker = Faker()

categories = [
    "pens", "cars", "beds", "cups", "lights", "screens", "windows", "shoes"
]

with session_maker() as session:
    products = [
        Product(
            name=faker.word(),
            price=random.randint(1, 100),
            category=random.choice(categories)
        ) for _ in range(500)
    ]

    for product in products:
        session.add(product)

    session.commit()
