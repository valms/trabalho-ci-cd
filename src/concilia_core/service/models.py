from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Transaction(Base):
    # irra
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    description = Column(String)
    amount = Column(Float)
    status = Column(String, default="PENDING")
