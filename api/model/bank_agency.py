def search_bank_agency(conn: object, id: int) -> list:
    """Searche the banks agency in the database.
    Parameter:
        conn (Database connection.)
        id (Agency bank code when searching for a bank agency.)
    Return:
        List banks
    """
    curr = conn.cursor()

    sql = f"""
            SELECT *
            FROM bank_agency
            WHERE id = {id}
            LIMIT 1
        """

    curr.execute(sql)

    id_bank_agency = list(map(list, curr.fetchall()))

    curr.close()

    return id_bank_agency


def search_banks_agencies(conn: object, number_agency: int = 0, name_agency: str = "", number_bank: int = 0) -> list:
    """Searches the banks agencies in the database.
    Parameter:
        conn (Database connection.)
        number_agency (Enter the angency code when searching for a bank agency.)
        name_agency (Enter the name angency when searching for a bank agency.)
        number_bank (Enter the bank code when searching for a bank agency.)
    Return:
        List banks
    """
    curr = conn.cursor()

    sql = """
            SELECT bank_agency.id, bank_agency.agency_number, 
                bank_agency.name as agency_name, bank.bb_central_number as number_bank
            FROM bank_agency
            INNER JOIN bank ON bank_agency.bank = bank.bb_central_number
            INNER JOIN person ON bank.person = person.id
        """

    if number_agency > 0:
        sql += f" WHERE bank_agency.agency_number = {number_agency}"

    if name_agency != "":
        if sql.find("WHERE"):
            sql += f" WHERE bank_agency.name LIKE '%{name_agency}%'"
        else:
            sql += f" AND bank_agency.name LIKE '%{name_agency}%'"

    if number_bank > 0:
        if sql.find("WHERE"):
            sql += f" WHERE bank.bb_central_number = {number_bank}"
        else:
            sql += f" AND bank.bb_central_number = {number_bank}"

    curr.execute(sql)

    banks_agencies = list(map(list, curr.fetchall()))

    curr.close()

    return banks_agencies


def record_banks_agencies(
    conn: object,
    tipo_operacao: bool = True,
    id: int = 0,
    number_agency: int = 0,
    name_agency: str = "",
    number_bank: int = 0,
) -> list:
    """Searches the banks agencies in the database.
    Parameter:
        conn (Database connection.)
        tipo_operacao (True = insert bank_agency, False = update bank agency.)
        id (id bank agency.)
        number_agency (Agency number that will be inserted into the database.)
        name_agency (Name of the agency that will be inserted into the database.)
        number_bank (Número do banco que vai inserir no banco de dados.)
    Return:
        List with the added bank.
    """
    curr = conn.cursor()

    if tipo_operacao:  # Insert
        sql = f"""
                INSERT INTO bank_agency(bank, agency_number, name)
                VALUES ({number_bank}, {number_agency}, '{name_agency}')
                RETURNING id, agency_number, name, bank
            """
    else:  # update
        sql = f"""
                UPDATE bank_agency
                SET bank = {number_bank}, agency_number = {number_agency}, name = '{name_agency}'
                WHERE id = {id}
                RETURNING id, agency_number, name, bank
            """
    curr.execute(sql)
    conn.commit()

    bank_agency = list(map(list, curr.fetchall()))

    curr.close()

    return bank_agency


def delete_banks_agencies(conn: object, id: int = 0) -> list:
    """Searches the banks agencies in the database.
    Parameter:
        conn (Database connection.)
        id (id bank agency.)
    Return:
        List with the deleted bank.
    """
    curr = conn.cursor()

    sql = f"DELETE from bank_agency WHERE id = {id} RETURNING id"
    curr.execute(sql)
    conn.commit()

    bank_agency = list(map(list, curr.fetchall()))

    curr.close()

    return bank_agency
