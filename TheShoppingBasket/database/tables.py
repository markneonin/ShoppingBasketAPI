from sqlalchemy import Column, Integer, DateTime, Text, String, ForeignKey, LargeBinary, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer,
                     primary_key=True,
                     index=True,
                     autoincrement=True)

    username = Column(String(100), unique=True)
    salt = Column(LargeBinary)
    password = Column(LargeBinary)
    api_secret = Column(LargeBinary)

    good = relationship('Good', back_populates='user', uselist=True)


class GoodStatus(enum.Enum):
    in_progress = 0
    complete = 1


class Good(Base):
    __tablename__ = 'good'

    good_id = Column(Integer,
                     primary_key=True,
                     autoincrement=True,
                     index=True)

    user_id = Column(Integer, ForeignKey('user.user_id'))
    text = Column(Text, nullable=False)
    created_date = Column(DateTime, server_default=func.now())
    status = Column(Enum(GoodStatus), default=GoodStatus.in_progress)

    complete_date = Column(DateTime, nullable=True)
    price = Column(Integer, nullable=True)

    user = relationship("User", back_populates="good")

    def as_dict(self):
        return {
                'good_id': self.good_id,
                'text': self.text,
                'created': str(self.created_date),
                'status': str(self.status.name),
                'completed': str(self.complete_date),
                'price': self.price/100 if self.price else None}


