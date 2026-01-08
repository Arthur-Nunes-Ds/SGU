from conection import engine,Base
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Numeric
from pydantic import BaseModel
from typing import Optional

#cria a base da tabela
class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False, unique=True)
    qnt = Column(Integer,nullable=False)
    '''permite cadastra numero com virgula sendo que ele no todo pode
        conter até 11 números contandos com os dois reservados para
        os números após a virgulas'''
    prc = Column(Numeric(precision=11, scale=2))

    def __init__(self, nome, qnt, prc):
        self.nome = nome
        self.qnt = qnt
        #já converte direitinho para o Numeric da db evitanto erro
        self.prc = Decimal(prc)

#cria a tabela na paratica
Base.metadata.create_all(engine)

class BaseCadastraProtudo(BaseModel):
    nome: str 
    qnt: int
    prc: int | float | str

class BaseVenderProtudo(BaseModel):
    qnt_removida_db : int
    id: int | None = None
    nome: str | None =  None

class BaseEditarProtudo(BaseModel):
    id: int
    qnt: int | None = None
    prc: int | float | str | None = None