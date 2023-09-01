def search_banks_agencies(conn: object, number_agency: int = 0, name_agency: str = "", name_person: str = "") -> list:
    """Searches the banks agencies in the database.
    Parameter: conn (Database connection.)
                code_bank (Enter the bank code when searching for a bank.)
    Return: List banks
    """
    curr = conn.cursor()

    sql = """
            SELECT bank_agency.agency_number, 
                bank_agency.name as agency_name, person.name as name_bank
            FROM bank_agency
            INNER JOIN bank ON bank_agency.bank = bank.bb_central_number
            INNER JOIN person ON bank.person = person.id
        """

    if number_agency > 0:
        sql += f" WHERE bank_agency.agency_number = {number_agency}"

    if name_agency != "":
        if sql.find("WHERE"):
            sql += f" AND bank_agency.name LIKE '%{name_agency}%'"
        else:
            sql += f" WHERE bank_agency.name LIKE '%{name_agency}%'"

    if name_person != "":
        if sql.find("WHERE"):
            sql += f" AND person.name LIKE '%{name_person}%'"
        else:
            sql +=  f" WHERE person.name LIKE '%{name_person}%'"

    curr.execute(sql)

    banks_agencies = list(map(list, curr.fetchall()))

    curr.close()

    return banks_agencies
