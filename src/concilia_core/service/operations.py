from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.concilia_core.service.models import Base, Transaction


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
