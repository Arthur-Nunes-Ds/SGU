from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from urllib.parse import quote_plus
from os import getenv
from dotenv import load_dotenv

#leitura das ver de abiente
load_dotenv()
IP_DB = getenv("IP_DB")
SENHA_DB = quote_plus(str(getenv("SENHA_DB")))
USER_DB = getenv("USER_DB")
BANCO_DB = getenv("BANCO_DB")
#tratamento para o int já que as var de abiente são tratas com string automaticamente
PORTA_DB = int(getenv("PORTA_DB")) # type: ignore

#garente que a senha com caracter especial seja lido como senha não como parte do endereço
    #caso não tenha esse quote_plus o sqlalchemy vai entender que o @ é parte do endereço e não da senha
ENDERECO_DB = f"mysql+pymysql://{USER_DB}:{SENHA_DB}@{IP_DB}:{PORTA_DB}/{BANCO_DB}"

#criação da engine para conectar o "python com mysql"
engine = create_engine(ENDERECO_DB)

#classe base para os modelos
Base = declarative_base()

#cria a sesion para manipular a db
Session = sessionmaker(bind=engine)

#isso garante que toda fez que eu usar a orm na dependecia ele vai fechar sossinho
def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()