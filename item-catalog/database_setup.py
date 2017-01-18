import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Restaurant(Base):

    # representation of our table inside the database
    __tablename__ = 'restaurant'

    # maps python objects to columns in our database
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'name': self.name,
            'id': self.id,
            'user_id': self.user_id,
        }

class MenuItem(Base):

    # representation of our table inside the database
    __tablename__ = 'menu_item'

    # maps python objects to columns in our database
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        #Returns object data in easily serializeable format
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,

        }

class Employee(Base):

    __tablename__ = 'employee'

    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)


class Address(Base):

    __tablename__ = 'address'

    street = Column(String(80), nullable=False)
    zip = Column(String(5), nullable=False)
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    employee = relationship(Employee)


####### insert at end of file #######

engine = create_engine('sqlite:///restaurantmenuwithusers.db')


Base.metadata.create_all(engine)
