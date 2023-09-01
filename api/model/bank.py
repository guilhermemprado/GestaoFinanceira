def search_banks(conn: object, code_bank: int = 0) -> list:
    """Searches the banks in the database.
    Parameter: conn (Database connection.)
                code_bank (Enter the bank code when searching for a bank.)
    Return: List banks
    """
    curr = conn.cursor()

    sql = """
            SELECT bank.bb_central_number, person.name
            FROM bank
            INNER JOIN person ON bank.person = person.id
        """

    if code_bank > 0:
        sql += f" WHERE bank.bb_central_number = {code_bank}"

    curr.execute(sql)

    banks = list(map(list, curr.fetchall()))

    curr.close()

    return banks
