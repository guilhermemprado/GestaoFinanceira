from infra.config.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from model.base import (
    create_data_base,
    create_table_data_base,
    exists_db,
    insert_default_datas,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Connect_alchemy:
    """Database connection"""

    def postgres(self):
        """Database connection"""
        try:
            # cria a engine de conexão com o banco
            url_engine = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            engine = create_engine(url_engine, echo=False)

            return sessionmaker(bind=engine)

        except Exception as error:
            # caso um erro fora do previsto
            error = "Não foi possível conectar ao banco."
            return {"mesage": error}
