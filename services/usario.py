from conection import session
from fastapi import APIRouter, HTTPException,status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from model.usarios import Usuario, BaseCriarUsuario, BaseLogarUsuario
from sqlalchemy.exc import IntegrityError
from jose import jwt
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from os import getenv
from .depeds import verificar_toke

load_dotenv()
SECRETES_KEY = getenv('SECRETES_KEY')
ALG = getenv('ALG')
EXPIRATION_TIMER_MINUTES = int(getenv('EXPIRATION_TIMER_MINUTES')) # type: ignore

def criar_token(id_user):
    #vai pega o tempo de agora e soma mas o tempo de EXPIRATION_TIMER_MINUTES
    dt_expi = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_TIMER_MINUTES)
    #o sub é o id. esse nome peguei com base no : https://www.jwt.io/
    dic_info = {'sub': id_user, 'exp': dt_expi}
    #isso cria o jwt 
    jwt_codificado = jwt.encode(dic_info, SECRETES_KEY, ALG) # type: ignore
    return jwt_codificado

Rota_Usuario = APIRouter()

@Rota_Usuario.post('/criar_usuario')
def criar_usario(base:BaseCriarUsuario):
    try:
        user = Usuario(base.nome, base.email,base.senha)
        session.add(user)
        session.commit()
        return {'mesagem': 'user criado com sucesso'}
    except IntegrityError:
        #restar a sessação da orm se não a proxima requizição feita vai usar 
        #o resto da sessação quebrada
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='já há um usuario com esse email'
        )

@Rota_Usuario.post('/logar_usuario')
def logar_usario(base: OAuth2PasswordRequestForm = Depends()):
    query_u = session.query(Usuario).filter_by(email = base.username).first()
    if query_u != None:
        if query_u.verificar_senha(base.password):
            _jwt = criar_token(query_u.id)
            # O retorno precisa ser assim para o /docs funcionar:
            return {
                "access_token": _jwt, 
                "token_type": "bearer"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='senha invalida'
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user não encontrado/cadastrado'
        )

#a depends basicamente fala que depende o do verifica_toke ou seja executa a função
#e pega a resposta dela
@Rota_Usuario.delete('/dell_user')
def dell_user(id_user: int = Depends(verificar_toke)):
    query_u = session.query(Usuario).filter_by(id = id_user).delete()

    if query_u:
        session.commit()
        return {"mensagem": "user removido"}
    else:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="user não cadastrado/encontrado"
        )
    
