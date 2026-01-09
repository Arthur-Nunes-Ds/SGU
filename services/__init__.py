#isso fala o que pode ser impordado se escrevr o código da seguinte forma:
    #impor services #<- assim eu sou pode usar o que está no __all__
from .porduto import Rota_Produto
from .usario import Rota_Usuario
from .admin import Rota_Adm
from .publics import Rota_Publics
__all__ = ['Rota_Produto','Rota_Usuario','Rota_Adm','Rota_Publics']