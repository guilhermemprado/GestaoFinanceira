def search_bank_account(conn: object, id: int) -> list:
    """Searche the banks accounts in the database.
    Parameter:
        conn (Database connection.)
        id (Account bank code when searching for a bank account.)
    Return:
        List banks
    """
    curr = conn.cursor()

    sql = f"""
            SELECT *
            FROM bank_account
            WHERE id = {id}
            LIMIT 1
        """

    curr.execute(sql)

    id_bank_account = list(map(list, curr.fetchall()))

    curr.close()

    return id_bank_account


def search_banks_accounts(
    conn: object,
    id: int = 0,
    account_number: int = 0,
    id_person: int = 0,
    agency_number: int = 0,
) -> list:
    """Searches the banks accounts in the database.
    Parameter:
        conn (Database connection.)
        id (Enter the account number when searching for a bank account.)
        account_number (Enter the account number when searching for a bank account.)
        name_person (Enter the name person when searching for a bank account.)
        agency_number (Enter the agency number when searching for a bank account.)
    Return:
        List banks
    """
    curr = conn.cursor()

    sql = """
            SELECT bank_account.id, bank_account.account_number,
                bank_account.person AS id_person, person.name AS name_person, 
                bank_account.agency AS id_agency, bank_agency.agency_number
            FROM bank_account
            INNER JOIN person
            ON bank_account.person = person.id
            INNER JOIN bank_agency
            ON bank_account.agency = bank_agency.id
        """

    if account_number > 0:
        sql += f" WHERE bank_account.account_number = {account_number}"

    if agency_number > 0:
        if sql.find("WHERE"):
            sql += f" WHERE bank_agency.agency_number = {agency_number}"
        else:
            sql += f" AND bank_agency.agency_number = {agency_number}"

    if id_person > 0:
        if sql.find("WHERE"):
            sql += f" WHERE bank_account.person = {id_person}"
        else:
            sql += f" AND bank_account.person = {id_person}"

    if id > 0:
        if sql.find("WHERE"):
            sql += f" WHERE bank_account.id = {id}"
        else:
            sql += f" AND bank_account.id = {id}"
        sql += " LIMIT 1"

    curr.execute(sql)

    banks_accounts = list(map(list, curr.fetchall()))

    curr.close()

    return banks_accounts


def record_banks_accounts(
    conn: object,
    tipo_operacao: bool = True,
    id: int = 0,
    account_number: int = 0,
    person: int = 0,
    agency_number: int = 0,
) -> list:
    """Searches the banks account in the database.
    Parameter:
        conn (Database connection.)
        tipo_operacao (True = insert bank_account, False = update bank account.)
        id (id bank account.)
        account_number (account number that will be inserted into the database.)
        person (Name of person the account that will be inserted into the database.)
        agency_number (Número do banco que vai inserir no banco de dados.)
    Return:
        List with the added bank account.
    """
    curr = conn.cursor()

    if tipo_operacao:  # Insert
        sql = f"""
                INSERT INTO bank_account(account_number, agency, person)
                VALUES ({account_number}, {agency_number}, {person})
                RETURNING id
            """
    else:  # update
        sql = f"""
                UPDATE bank_account
                SET account_number = {account_number},
                    agency = {agency_number},
                    person = {person}
                WHERE id = {id}
                RETURNING id
            """
    curr.execute(sql)
    conn.commit()

    id_bank_account = list(map(list, curr.fetchall()))

    sql = f"""
        SELECT bank_account.id, bank_account.account_number,
            bank_account.person, person.name, bank_account.agency
        FROM bank_account
        INNER JOIN person
        ON bank_account.person = person.id
        WHERE bank_account.id = {id_bank_account[0][0]}
    """
    curr.execute(sql)

    bank_account = list(map(list, curr.fetchall()))

    curr.close()

    return bank_account


def delete_banks_accounts(conn: object, id: int = 0) -> list:
    """Searches the accounts banks in the database.
    Parameter:
        conn (Database connection.)
        id (id bank account.)
    Return:
        List with the deleted account.
    """
    curr = conn.cursor()

    sql = f"DELETE from bank_account WHERE id = {id} RETURNING id"
    curr.execute(sql)
    conn.commit()

    bank_account = list(map(list, curr.fetchall()))

    curr.close()

    return bank_account