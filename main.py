import json
import random
import string
import uuid

from dataclasses import dataclass
from faker import Faker

import os
from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import sessionmaker

from model.UserModel import Base, UserModel
from dotenv import load_dotenv


def get_connection_string(database):
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    database_name = database

    return f'postgresql://{user}:{password}@{host}:{port}/{database_name}'

def prepare_database():
    engine = create_engine(get_connection_string("usersdb"))
    Base.metadata.create_all(engine)

def get_database_session():
    engine = create_engine(get_connection_string("usersdb"))
    session = sessionmaker(bind=engine)
    return session()

def get_random_gender():
    gender_identities = [
        "Male", "Female", "Cis Male", "Cis Female"
    ]
    return random.choice(gender_identities)

def generate_document_id(length=12, prefix="", suffix=""):
    characters = string.digits + string.ascii_uppercase
    random_part = ''.join(random.choice(characters) for _ in range(length))
    return prefix + random_part + suffix

def export_users_to_json(users, filename="fake_users.json", root_dir=""):
    file_path = os.path.join(root_dir, "files", filename)
    with open(file_path, "w") as f:
        json.dump(users, f, default=lambda o: o.__dict__, indent=4)

@dataclass
class User:
    id: str
    name: str
    email: str
    birthdate: str
    document: str
    gender: str
    telephone: str
    is_active: bool
    yearly_income: int

    def __init__(self, id, name, email, birthdate, document, gender, telephone, is_active, yearly_income):
        self._id = id
        self._name = name
        self._email = email
        self._birthdate = birthdate
        self._document = document
        self._gender = gender
        self._telephone = telephone
        self._is_active = is_active
        self._yearly_income = yearly_income

    def to_dict(self):
        return {
            "id": self._id,
            "name": self._name,
            "email": self._email,
            "birthdate": self._birthdate,
            "document": self._document,
            "gender": self._gender,
            "telephone": self._telephone,
            "is_active": self._is_active,
            "yearly_income": self._yearly_income
        }

    def __repr__(self):
        return f'User(id={self._id}, name={self._name}, email={self._email}, birthdate={self._birthdate}, document={self._document}, gender={self._gender}, telephone={self._telephone}, is_active={self._is_active}, yearly_income={self._yearly_income})'

def generate_fake_user():
    fake = Faker('en-US')
    return User(
        id = uuid.uuid4(),
        name = fake.name(),
        email = fake.email(),
        birthdate = str(fake.date_of_birth()),
        document = generate_document_id(length=15, prefix="DOC-", suffix=""),
        gender = get_random_gender(),
        telephone = fake.phone_number(),
        is_active = fake.boolean(chance_of_getting_true=50),
        yearly_income = fake.random_int(min=50000, max=320000)
    )

def generate_fake_users_to_file():
    root_dir = os.getcwd()
    users = [generate_fake_user() for _ in range(1000)]
    export_users_to_json(users=users, root_dir=root_dir)

def populate_user_database():
    session = get_database_session()
    users = [generate_fake_user() for user in range(1000)]
    users_dict = [user.to_dict() for user in users]
    users_model = [UserModel(**user) for user in users_dict]

    try:
        session.bulk_save_objects(users_model)
        session.commit()
        session.close()
    except DBAPIError as e:
        print(e)
    except Exception as e:
        print(e)

def main():
    load_dotenv()
    prepare_database()

    populate_user_database()

    #generate_fake_users_to_file()

if __name__ == "__main__":
  main()