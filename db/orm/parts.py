from sqlalchemy import orm, Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from db.orm.db_sessions import Base_orm


class Profile(Base_orm, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer,
                primary_key=True,
                autoincrement=True)
    login = Column(String,
                   nullable=False,
                   unique=True)
    password = Column(String,
                             nullable=False)

    pet_name = Column(String,
                      nullable=False)

    type = Column(String,
                  nullable=False)

    age = Column(Integer,
                 nullable=False)

    poroda = Column(String,
                    nullable=False)

    def __init__(self, login, password, pet_name, type, age, poroda):
        self.login = login
        self.hashed_password = generate_password_hash(password)
        self.pet_name = pet_name
        self.type = type
        self.age = age
        self.poroda = poroda

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

