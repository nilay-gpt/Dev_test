from sqlalchemy import Column, Index

from sqlalchemy.dialects.sqlite import CHAR, FLOAT, TEXT, INTEGER

from models.base import Base


class Customers(Base):
    __tablename__ = 'customers'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name =  Column(CHAR(50))
    address = Column(CHAR(50))
    dob = Column(TEXT)
    email = Column(CHAR(50), unique=True)


    __table_args__ = (
        Index('id_index', 'id'),
        Index('email_index', 'email')
    )

    def __init__(self, name, address, dob, email):
        self.name = name
        self.address = address
        self.dob = dob
        self.email = email

    def __repr__(self):
        return "Customer Name={} email={}".format(self.name, self.email)
