from conection import get_session
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException,status, Depends
from model.usarios import Usuario, BaseEditarUsuarioi
from .depeds import RolePermitidas

Rota_Usuario = APIRouter()

#a depends basicamente fala que depende o do verifica_toke ou seja executa a função
#e pega a resposta dela
@Rota_Usuario.delete('/dell_user')
def dell_user(id_user: int = Depends(RolePermitidas(['cliente','adm'])),session: Session = Depends(get_session)):
    query_u = session.query(Usuario).filter_by(id = id_user, role = 'cliente').delete()

    if query_u:
        session.commit()
        return {"mensagem": "user removido"}
    else:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="user não cadastrado/encontrado"
        )
    
@Rota_Usuario.post('/editar_user')
def editar_user(base : BaseEditarUsuarioi, id_user: int = Depends(RolePermitidas(['cliente','adm'])),session: Session = Depends(get_session)):
    '''caso não queira altera o dado do protudo basta só não pasa a chave'''
    query_u = session.query(Usuario).filter_by(id = id_user, role = 'cliente').first()
    if query_u:
        if base.senha != None :
            query_u.altera_senha(base.senha)
            
        if base.nome != None:
            query_u.nome = base.nome
            
        if base.nome == None and base.senha == None:
            raise HTTPException(
                status_code=status.HTTP_421_MISDIRECTED_REQUEST,
                detail='informe uma nova Nome ou uma nova Senha para editar o user'
            )

        session.commit()
        return {'mesagem': 'user editado com sucesso'}
    else:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="user não cadastrado/encontrado"
        )
    
@Rota_Usuario.get('/dados_user')
def dados_user(id_user: int = Depends(RolePermitidas(['cliente','adm'])),session: Session = Depends(get_session)):
    query_u = session.query(Usuario).filter_by(id = id_user).first()

    if query_u != None:
        return {
            'mesagem':{
                'nome' : query_u.nome,
                'email' : query_u.email
            }
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user não existe'
        )
    