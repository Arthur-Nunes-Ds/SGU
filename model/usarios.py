from conection import engine,Base
from sqlalchemy import Column, Integer, String
from passlib.hash import sha256_crypt as sha256

#cria a base da tabela
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = sha256.encrypt(senha)
    

#cria a tabela na paratica
Base.metadata.create_all(engine)





