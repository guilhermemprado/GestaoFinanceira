def search_moviments(
    conn: object,
    account_number: int = 0,
    description: str = "",
    date: str = "",
) -> list:
    """Searches the moviment in the database.
    Parameter:
        conn (Database connection.)
        account_number (Account number relating to moviment.)
        description (Description of the moviment.)
        value (Value of the moviment.)
        date (Date of the moviment.)
    Return:
        List moviment
    """
    curr = conn.cursor()

    sql = """
            SELECT moviment.id as id_moviment, 
                bank_account.person as id_person,
                (SELECT name FROM person WHERE person.id = bank_account.person) as name_person,
                bank_agency.bank as id_bank,
                (SELECT name FROM person WHERE person.id = bank_agency.bank) as name_bank,
                bank_agency.name as name_agency,
                bank_account.account_number,
                moviment.description,
                moviment.value,
                moviment.date
            FROM moviment
            INNER JOIN bank_account
            ON moviment.bank_account = bank_account.id
            INNER JOIN bank_agency
            ON bank_account.agency = bank_agency.id
        """
    if account_number > 0:
        if sql.find("WHERE") != -1:
            sql += f" AND bank_account.account_number = {account_number}"
        else:
            sql += f" WHERE bank_account.account_number = {account_number}"

    if description != "":
        if sql.find("WHERE") != -1:
            sql += f" AND moviment.description = '{description}'"
        else:
            sql += f" WHERE moviment.description = '{description}'"

    if date != "":
        if sql.find("WHERE") != -1:
            sql += f" AND moviment.date = '{description}'"
        else:
            sql += f" WHERE moviment.date = '{description}'"

    curr.execute(sql)

    moviments = list(map(list, curr.fetchall()))

    curr.close()

    return moviments


def record_moviment(
    conn: object,
    tipo_operacao: bool = True,
    id_moviment: int = 0,
    id_account: int = 0,
    description: str = "",
    value: float = 0,
    date: str = "",
) -> list:
    """Search address in the database.
    Parameter:
        conn (Database connection.)
        tipo_operacao (True = insert moviment, False = update moviment.)
        id_moviment (Numero identificador do movimento.)
        account_number (Account number relating to moviment.)
        description (Description of the moviment.)
        value (Value of the moviment.)
        date (Date of the moviment.)

    Return:
        List with the moviment.
    """
    curr = conn.cursor()

    if tipo_operacao:  # Insert
        sql = f"""
                INSERT INTO moviment(bank_account, description, value, date)
                VALUES ({id_account}, '{description}', {value}, '{date}')
                RETURNING id
            """
    else:  # update
        sql = f"""
                UPDATE moviment
                SET bank_account = {id_account},
                    description = '{description}',
                    value = {value},
                    date = '{date}'
                WHERE id = {id_moviment}
                RETURNING id
            """

    curr.execute(sql)

    conn.commit()

    id_moviment = list(map(list, curr.fetchall()))

    sql = f"""
            SELECT moviment.id as id_moviment,
                bank_account.person as id_person,
                (SELECT name FROM person WHERE person.id = bank_account.person) as name_person,
                bank_agency.bank as id_bank,
                (SELECT name FROM person WHERE person.id = bank_agency.bank) as name_bank,
                bank_agency.name as name_agency,
                bank_account.account_number,
                moviment.description,
                moviment.value,
                moviment.date
            FROM moviment
            INNER JOIN bank_account
            ON moviment.bank_account = bank_account.id
            INNER JOIN bank_agency
            ON bank_account.agency = bank_agency.id
            WHERE moviment.id = {id_moviment[0][0]}
        """
    curr.execute(sql)

    moviment = list(map(list, curr.fetchall()))

    curr.close()

    return moviment


def exclude_moviment(conn: object, id_moviment: int = 0) -> list:
    """Searches the moviment in the database.
    Parameter:
        conn (Database connection.)
        id_moviment (id moviment.)
    Return:
        List with the deleted moviment.
    """
    curr = conn.cursor()

    sql = f"DELETE from moviment WHERE id = {id_moviment} RETURNING id"
    curr.execute(sql)
    conn.commit()

    moviment = list(map(list, curr.fetchall()))

    curr.close()

    return moviment
