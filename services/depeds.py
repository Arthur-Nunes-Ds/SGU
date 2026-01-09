from jose import jwt, JWTError
from fastapi import HTTPException,status, Depends
from dotenv import load_dotenv
from os import getenv
from fastapi.security import OAuth2PasswordBearer
from conection import get_session
from model.usarios import Usuario
from sqlalchemy.orm import Session

load_dotenv()
SECRETES_KEY = getenv('SECRETES_KEY')
ALG = getenv('ALG')

#base para tranca rota
oauth_schema = OAuth2PasswordBearer('/public/logar_usuario/')

def verificar_toke(token: str = Depends(oauth_schema)):
    try:
        dic_info_u = jwt.decode(token, str(SECRETES_KEY), ALG)
        
        return dic_info_u 
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Acesso Negado'
        )
    
class RolePermitidas:
    def __init__(self, roles: list):
        self.roles_depedecia = roles
    
    # o call me permite eu só meceiona o objto como se ele foce uma func
    def __call__(self, user=Depends(verificar_toke), session: Session = Depends(get_session)): 
        query = session.query(Usuario).filter_by(role = 'adm').all()
        #o len vai garantir que seja possivel só cadastra uma adm
        if len(query) <= 1:
            if user['role'] not in self.roles_depedecia :
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="você não tem permissão para acessar este recurso"
                )
            else:
                return int(user['sub'])
        else:
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail='não pode der 2 user com a role de adm'
            )
        
       
