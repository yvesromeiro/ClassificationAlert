import json
import os
import random
import string
import uuid
from dataclasses import dataclass
<<<<<<< Updated upstream

from faker import Faker
=======
from faker import Faker
import os
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Date, Float
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Base para SQLAlchemy
Base = declarative_base()

### FUNÇÃO GERAR ID DE DOCUMENTO ###

def generate_document_id(length=12, prefix="", suffix=""):
    characters = string.digits + string.ascii_uppercase
    random_part = ''.join(random.choice(characters) for _ in range(length))
    return prefix + random_part + suffix

### MODELO DO BANCO USERSDB ###

# Modelo de Tabela: Usuários
class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    birthdate = Column(Date)
    document = Column(String)
    gender = Column(String)
    telephone = Column(String)
    is_active = Column(Boolean)
    yearly_income = Column(Float)

# Função para gerar um usuário falso para o 'usersdb'
def generate_fake_user():
    fake = Faker('en-US')
    return User(
        id=str(uuid.uuid4()),
        name=fake.name(),
        email=fake.email(),
        birthdate=fake.date_of_birth(),
        document=generate_document_id(length=15, prefix="DOC-", suffix=""),
        gender=random.choice(["Male", "Female"]),
        telephone=fake.phone_number(),
        is_active=fake.boolean(chance_of_getting_true=50),
        yearly_income=round(random.uniform(50000, 320000), 2)
    )

### MODELO DO BANCO MARKETINGDB ###

# Modelo de Tabela: Campanhas de Marketing
class MarketingCampaign(Base):
    __tablename__ = 'marketing_campaigns'

    id = Column(String, primary_key=True)
    name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    channel = Column(String)  # Ex: email, social media, search engine, etc.
    budget = Column(Float)
    target_audience = Column(String)

# Função para gerar uma campanha de marketing falsa para o 'marketingdb'
def generate_fake_marketing_campaign():
    fake = Faker('en-US')
    return MarketingCampaign(
        id=str(uuid.uuid4()),
        name=fake.bs().title(),
        start_date=fake.date_this_year(),
        end_date=fake.date_this_year(),
        channel=random.choice(["email", "social media", "SMS", "search engine"]),
        budget=round(random.uniform(1000, 50000), 2),
        target_audience=random.choice(["Teens", "Adults", "Seniors"])
    )

# Função para obter a string de conexão do banco de dados
def get_connection_string(database):
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    database_name = database
    return f'postgresql://{user}:{password}@{host}:{port}/{database_name}'

# Preparar o banco de dados 'usersdb'
def prepare_users_database():
    engine = create_engine(get_connection_string("usersdb"))
    Base.metadata.create_all(engine)

# Preparar o banco de dados 'marketingdb'
def prepare_marketing_database():
    engine = create_engine(get_connection_string("marketingdb"))
    Base.metadata.create_all(engine)

# Sessão de banco de dados para 'usersdb'
def get_users_database_session():
    engine = create_engine(get_connection_string("usersdb"))
    session = sessionmaker(bind=engine)
    return session()
>>>>>>> Stashed changes

# Sessão de banco de dados para 'marketingdb'
def get_marketing_database_session():
    engine = create_engine(get_connection_string("marketingdb"))
    session = sessionmaker(bind=engine)
    return session()

<<<<<<< Updated upstream
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
    document: int
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

    def __repr__(self):
        return f'User(id={self._id}, name={self._name}, email={self._email}, birthdate={self._birthdate}, document={self._document}, gender={self._gender}, telephone={self._telephone}, is_active={self._is_active}, yearly_income={self._yearly_income})'

def generate_fake_user():
    fake = Faker('en-US')
    return User(
        id = str(uuid.uuid4()),
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
=======
### POPULAR BANCO USERSDB ###

def populate_users_database():
    session = get_users_database_session()
>>>>>>> Stashed changes
    users = [generate_fake_user() for _ in range(1000)]
    try:
        session.bulk_save_objects(users)
        session.commit()
        session.close()
    except DBAPIError as e:
        print(e)
    except Exception as e:
        print(e)

<<<<<<< Updated upstream
def main():
    generate_fake_users_to_file()
=======
### POPULAR BANCO MARKETINGDB ###

def populate_marketing_database():
    session = get_marketing_database_session()
    campaigns = [generate_fake_marketing_campaign() for _ in range(1000)]
    try:
        session.bulk_save_objects(campaigns)
        session.commit()
        session.close()
    except DBAPIError as e:
        print(e)
    except Exception as e:
        print(e)

### FUNÇÃO PRINCIPAL ###

def main():
    load_dotenv()  # Carregar variáveis de ambiente

    # Preparar e popular 'usersdb'
    prepare_users_database()
    populate_users_database()

    # Preparar e popular 'marketingdb'
    prepare_marketing_database()
    populate_marketing_database()
>>>>>>> Stashed changes

if __name__ == "__main__":
    main()
