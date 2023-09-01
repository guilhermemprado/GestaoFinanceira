import psycopg2
from model.base import create_data_base, create_table_data_base, exists_db, insert_default_datas

from infra.config.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


class Connect:
    """Database connection"""

    def postgres(self):
        """Database connection"""
        try:
            conn = self.connect_db(set_user=False)

            # Verifica se existe a base de dados, se tiver armazena o nome.
            if not exists_db(conn, DB_NAME):
                create_data_base(conn)

                conn = self.connect_db(set_user=True)
                create_table_data_base(conn)
                insert_default_datas(conn)
            else:
                conexao_string = (
                    f"host='{DB_HOST}' dbname='{DB_NAME}' user='{DB_USER}' password='{DB_PASSWORD}' port={DB_PORT}"
                )
                conn = psycopg2.connect(conexao_string)
            return conn

        except psycopg2.DatabaseError as error:
            # como a duplicidade do nome é a provável razão do IntegrityError
            error_msg = f"Erro na conexão com banco de dados PostgreSql: {error.args[0]}"
            return {"mesage": error_msg}

        except Exception as error:
            # caso um erro fora do previsto
            error_msg = "Não foi possível conectar ao banco."
            return {"mesage": error}

    def connect_db(self, set_user=False):
        """Cria conexão com o banco de dados"""
        conexao_string = f"host='{DB_HOST}' user='{DB_USER}' password='{DB_PASSWORD}'"
        if set_user:
            conexao_string = f"{conexao_string} dbname='{DB_NAME}' port={DB_PORT}"

        return psycopg2.connect(conexao_string)
