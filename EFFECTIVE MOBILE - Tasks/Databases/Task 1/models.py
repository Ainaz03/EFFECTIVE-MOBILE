from database import BaseModel
from sqlalchemy import  Column, Integer, String, Float, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Genre(BaseModel):
    __tablename__ = 'genre'

    genre_id = Column(Integer, primary_key=True, index=True)
    name_genre = Column(String)

    books = relationship("Book", back_populates="genre")

class Author(BaseModel):
    __tablename__ = 'author'

    author_id = Column(Integer, primary_key=True, index=True)
    name_author = Column(String)

    books = relationship("Book", back_populates="author")

class City(BaseModel):
    __tablename__ = 'city'

    city_id = Column(Integer, primary_key=True, index=True)
    days_delivery = Column(Float)

    clients = relationship("Client", back_populates="city")

class Book(BaseModel):
    __tablename__ = 'book'

    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    price = Column(Numeric(10, 2))
    amount = Column(Integer)

    author_id = Column(Integer, ForeignKey('author.author_id'))
    author = relationship("Author", back_populates="books")

    genre_id = Column(Integer, ForeignKey('genre.genre_id'))
    genre = relationship("Genre", back_populates="books")

class Client(BaseModel):
    __tablename__ = 'client'

    client_id = Column(Integer, primary_key=True, index=True)
    name_client = Column(String)
    email = Column(String)

    city_id = Column(Integer, ForeignKey('city.city_id'))
    city = relationship("City", back_populates="clients")

    buys = relationship("Buy", back_populates="client")

class Buy(BaseModel):
    __tablename__ = 'buy'

    buy_id = Column(Integer, primary_key=True, index=True)
    buy_description = Column(String)

    client_id = Column(Integer, ForeignKey('client.client_id'))
    client = relationship("Client", back_populates="buys")

class Step(BaseModel):
    __tablename__ = 'step'

    step_id = Column(Integer, primary_key=True, index=True)
    name_step = Column(String)

class Buy_book(BaseModel):
    __tablename__ = 'buy_book'

    buy_book_id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer)

    buy_id = Column(Integer, ForeignKey('buy.buy_id'))
    book_id = Column(Integer, ForeignKey('book.book_id'))

class Buy_step(BaseModel):
    __tablename__ = 'buy_step'

    buy_step_id = Column(Integer, primary_key=True, index=True)
    date_step_beg = Column(DateTime)
    date_step_end = Column(DateTime)

    buy_id = Column(Integer, ForeignKey('buy.buy_id'))
    step_id = Column(Integer, ForeignKey('step.step_id'))