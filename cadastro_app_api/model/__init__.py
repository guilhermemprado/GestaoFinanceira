"""
    Imports
"""
import os

from model.base import Base, create_data_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists

caminho = os.getcwd()
PATH_BD = caminho.replace('/meu_app_api', '') + "/database"
NAME_DB = "/gestao_financeira.db"
# Verifica se o diretorio não existe.
if not os.path.exists(PATH_BD):
    # Cria o diretorio.
    os.makedirs(PATH_BD)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = f"sqlite:///%s/{NAME_DB}" % PATH_BD

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir
if not database_exists(engine.url):
    # Cria banco de dados.
    create_data_base(PATH_BD, NAME_DB)

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)
