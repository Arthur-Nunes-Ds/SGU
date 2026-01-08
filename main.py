from fastapi import FastAPI
from services import Rota_Produto

#comando para iniciar o servidor da api: uvicorn main:app --reload

app = FastAPI()

app.include_router(
    Rota_Produto,
    #todas as rotas de produtos.py começarão com /usuarios
    prefix="/produtos", 
    #organiza as rotas sob este grupo no /docs   
    tags=["Produtos"]      
)

