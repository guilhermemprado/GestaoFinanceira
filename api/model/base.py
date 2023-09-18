import requests
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy.ext.declarative import declarative_base


def exists_db(conn: object, name_db: str) -> bool:
    """Check if the database exists
    Param:
        conn: Database connection.
        name_db: Nome do banco que deverá ser verificado.
    return:
        db_exists: True exists db, False not exists db.
    """
    curr = conn.cursor()
    curr.execute("SELECT datname FROM pg_database")

    dbs = list(map(list, curr.fetchall()))
    db_exists = any(name_db in list for list in dbs)

    return db_exists


def create_data_base(conn: object):
    """create database
    Param:
        conn: Database connection.
    """
    # Enable auto commit (to create the database and necessary)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    curr = conn.cursor()
    # Create database gestao_financeira
    curr.execute("CREATE DATABASE gestao_financeira;")

    curr.close()


def create_table_data_base(conn: object):
    """
    Cria tabelas:
        person_physical: (id, person, cpf, birthdate)
        person: (id, name, email, phone_number)
        address: (id, person, city, cep, street, number, district, complement)
        city: (ibge_number, uf, name)
        uf: (ibge_number, name)
        bank: (bb_central_number, person)
        bank_agency: (id, bank, agency_number, name)
        bank_account: (id, person, agency, account_number)
        moviment: (id, bank_account, description, value, date)
    Param:
        conn: Database connection.
    """

    curr = conn.cursor()

    # Create a table: person_physical
    curr.execute(
        """
        CREATE TABLE IF NOT EXISTS person_physical 
            (id SERIAL PRIMARY KEY,
            person INTEGER NOT NULL,
            cpf VARCHAR(11),
            birthdate VARCHAR(8))
    """
    )

    # Create a table: uf
    curr.execute(
        """
        CREATE TABLE IF NOT EXISTS uf 
            (ibge_number INT PRIMARY KEY,
            acronym TEXT NOT NULL)
    """
    )

    # Create a table: city
    curr.execute(
        """
        CREATE TABLE IF NOT EXISTS city 
            (ibge_number SERIAL PRIMARY KEY,
            uf INTEGER NOT NULL,
            name TEXT NOT NULL,
            foreign key(uf) REFERENCES uf(ibge_number))
    """
    )

    # Create a table: address
    curr.execute(
        """
        CREATE TABLE IF NOT EXISTS address 
            (id SERIAL PRIMARY KEY,
            person INT NOT NULL,
            city INT NOT NULL,
            cep VARCHAR(9) NOT NULL,
            street VARCHAR(50) NOT NULL,
            number INT NOT NULL,
            district VARCHAR(50) NOT NULL,
            complement VARCHAR(100) NOT NULL,
            foreign key(city) REFERENCES city(ibge_number))
    """
    )

    # Create a table: person
    curr.execute(
        """
        CREATE TABLE IF NOT EXISTS person 
            (id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            phone_number VARCHAR(15))
    """
    )

    # Create a table: bank
    curr.execute(
        """
        CREATE TABLE IF NOT EXISTS bank 
            (bb_central_number INT PRIMARY KEY,
            person INTEGER NOT NULL,
            foreign key(person) REFERENCES person(id))
    """
    )

    # Create a table: bank_agency
    curr.execute(
        """
        CREATE TABLE IF NOT EXISTS bank_agency 
            (id SERIAL PRIMARY KEY,
            bank INT NOT NULL,
            agency_number INT NOT NULL,
            name TEXT NOT NULL,
            foreign key(bank) REFERENCES bank(bb_central_number))
    """
    )

    # Create a table: bank_account
    curr.execute(
        """
        CREATE TABLE IF NOT EXISTS bank_account 
            (id SERIAL PRIMARY KEY,
            person INT NOT NULL,
            agency INT NOT NULL,
            account_number INT NOT NULL,
            foreign key(person) REFERENCES person(id),
            foreign key(agency) REFERENCES bank_agency(id))
    """
    )

    # Create a table: moviment
    curr.execute(
        """
        CREATE TABLE IF NOT EXISTS moviment 
            (id SERIAL PRIMARY KEY,
            bank_account INT NOT NULL,
            description TEXT NOT NULL,
            value REAL NOT NULL,
            date VARCHAR(8) NOT NULL,
            foreign key(bank_account) REFERENCES bank_account(id))
    """
    )

    conn.commit()


def insert_default_datas(conn):
    """Consume api brasilapie to get the existing uf, and insert in the uf table.
        Consume the brasilapie api to get the existing cities, and insert them into the city table.
        Consume the brasilapie api to obtain the existing banks, and insert them into the person and bank tables.
    Param:
        conn: Database connection.
    """

    curr = conn.cursor()

    # Uf
    resultado = requests.get("https://brasilapi.com.br/api/ibge/uf/v1", verify=False).json()

    list_all_uf = []
    list_sigla = []
    for i in resultado:
        list_all_uf.append((i["id"], i["sigla"].upper()))
        list_sigla.append(i["sigla"].upper())

    sql = f"INSERT INTO uf (ibge_number, acronym) VALUES {str(list_all_uf)[1:-1]}"

    curr.execute(sql)

    conn.commit()

    # City
    list_all_uf = []
    for i in list_sigla:
        uf = i.replace("'", "")
        resultado = requests.get(
            f"https://brasilapi.com.br/api/ibge/municipios/v1/{uf}?providers=dados-abertos-br,gov,wikipedia",
            verify=False,
        ).json()
        for l in resultado:
            try:
                int(l["codigo_ibge"])
                flag = True
            except ValueError:
                flag = False

            if flag:
                list_all_uf.append((l["codigo_ibge"], (l["nome"].upper()).replace("'", ""), str(l["codigo_ibge"])[0:2]))

    sql = f"INSERT INTO city (ibge_number, name, uf) VALUES {str(list_all_uf)[1:-1]}"

    curr.execute(sql)

    conn.commit()

    resultado = requests.get("https://brasilapi.com.br/api/banks/v1", verify=False).json()

    for i in resultado:
        if (i["code"]) is not None:
            name_person = (i["fullName"].upper()).replace("'", "")

            sql = f"INSERT INTO person (name) VALUES ('{name_person}') RETURNING id"

            curr.execute(sql)

            conn.commit()

            # Armazena o id da ultima pessoa adicionada.
            last_person_id = curr.fetchone()

            # Bank
            sql = f"INSERT INTO bank (bb_central_number, person) VALUES {(i['code'], last_person_id[0])}"

            curr.execute(sql)

            conn.commit()

    arquivo_account = open("api/docs/insert_bank_account.txt", "r")
    arquivo_agency = open("api/docs/insert_bank_agency.txt", "r")
    arquivo_person = open("api/docs/insert_person.txt", "r")
    arquivo_person_physical = open("api/docs/insert_person_physical.txt", "r")

    for l_account in arquivo_account:
        sql = arquivo_agency.readline()

        curr.execute(sql)
        conn.commit()

        last_id_agency = curr.fetchone()

        sql = arquivo_person.readline()

        curr.execute(sql)
        conn.commit()

        last_id_person = curr.fetchone()

        sql = arquivo_person_physical.readline()

        sql = sql.replace("codigo_person_physical", str(last_id_person[0]))

        curr.execute(sql)
        conn.commit()

        sql_old = l_account

        sql_old = sql_old.replace("codigo_person", str(last_id_person[0]))
        sql_new = sql_old.replace("codigo_agency", str(last_id_agency[0]))

        curr.execute(sql_new)
        conn.commit()

    conn.close()


Base = declarative_base()
