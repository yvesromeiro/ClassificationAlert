import json
import random
import string
import uuid
from dataclasses import dataclass
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

# Sessão de banco de dados para 'marketingdb'
def get_marketing_database_session():
    engine = create_engine(get_connection_string("marketingdb"))
    session = sessionmaker(bind=engine)
    return session()

### POPULAR BANCO USERSDB ###

def populate_users_database():
    session = get_users_database_session()
    users = [generate_fake_user() for _ in range(1000)]
    try:
        session.bulk_save_objects(users)
        session.commit()
        session.close()
    except DBAPIError as e:
        print(e)
    except Exception as e:
        print(e)

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

if __name__ == "__main__":
    main()
