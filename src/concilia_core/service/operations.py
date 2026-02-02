from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    description = Column(String)
    amount = Column(Float)
    status = Column(String, default="PENDING")


def verificar_conciliacao(valor_banco: float, valor_sistema: float):
    if valor_banco == valor_sistema:
        return "MATCH"
    return "DIVERGENTE"


class ConciliaService:
    def __init__(self, db_url="sqlite:///:memory:"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_transaction(self, desc: str, value: float):
        with self.Session() as session:
            tx = Transaction(description=desc, amount=value)
            session.add(tx)
            session.commit()
            return tx.id

    def get_transaction_status(self, tx_id: int):
        with self.Session() as session:
            tx = session.query(Transaction).filter_by(id=tx_id).first()
            return tx.status if tx else None
