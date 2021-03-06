from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from bot.formatters import text, currency
from bot.settings import Settings

from .engine import engine

DeclarativeBase = declarative_base()
settings = Settings()


class LegoSet(DeclarativeBase):
    __tablename__ = 'sets'
    id = Column('id', Integer, primary_key=True)
    number = Column('number', String(20))
    name = Column('name', String(255))
    type = Column('type', String(255), nullable=True)
    theme_group = Column('theme_group', String(255), nullable=True)
    theme = Column('theme', String(255), nullable=True)
    subtheme = Column('subtheme', String(255), nullable=True)
    tags = Column('tags', String(1000), nullable=True)
    year = Column('year', Integer, nullable=True)
    pieces = Column('pieces', Integer, nullable=True)
    minifigs = Column('minifigs', Integer, nullable=True)
    uk_price = Column('uk_price', Float(5, 2), nullable=True, default=None)
    us_price = Column('us_price', Float(5, 2), nullable=True, default=None)
    eu_price = Column('eu_price', Float(5, 2), nullable=True, default=None)
    packaging = Column('packaging', String(255), nullable=True)
    dimensions = Column('dimensions', String(255), nullable=True)
    weight = Column('weight', String(255), nullable=True)
    barcodes = Column('barcodes', String(255), nullable=True)
    item_number = Column('item_number', String(255), nullable=True)
    image = Column('image', String(255), nullable=True)
    url = Column('url', String(255), nullable=True)
    created = Column('created', DateTime, default=datetime.now())
    updated = Column('updated', DateTime, nullable=True)

    def __repr__(self):
        return '<Id {} Name {} Number {}>'.format(self.id, self.name, self.number)

    def all():
        Session = sessionmaker(bind=engine)
        session = Session()

        return session.query(LegoSet).all()

    def search(text):
        Session = sessionmaker(bind=engine)
        session = Session()

        name_filter = LegoSet.name.like('%' + text + '%')
        number_filter = LegoSet.number.like('%' + text + '%')

        return session.query(LegoSet).filter(or_(name_filter, number_filter)).limit(10).all()

    def create(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(self)
        session.commit()
        session.close

    def set_info(self):
        template = "Set Number: {}\nName: {}\nParts: {}\nMinifigs: {}\nYear: {}\nUS Price: {}\nEU Price: {}\nUK Price: {}"

        return template.format(
            text.format(self.number),
            text.format(self.name),
            text.format(self.pieces),
            text.format(self.minifigs),
            text.format(self.year),
            currency.format(self.us_price, currency.USD),
            currency.format(self.eu_price, currency.EUR),
            currency.format(self.uk_price, currency.GBP)
        )

    def is_blocked(self):
        for blocked_set in settings.blocked_sets():
            if blocked_set in self.number:
                return True

        return False


def create_tables():
    DeclarativeBase.metadata.create_all(engine)


def drop_tables():
    DeclarativeBase.metadata.drop_all(engine)
