def search_person(
    conn: object,
    id: int = 0,
    name: str = "",
    email: str = "",
    phone: str = "",
) -> list:
    """Searches the banks accounts in the database.
    Parameter:
        conn (Database connection.)
        id (Enter id code to searching for a person.)
        name (Enter name to searching for a person.)
        email (Enter email to searching for a person.)
        phone (Enter phone number to search for a person.)
    Return:
        List banks
    """
    curr = conn.cursor()

    sql = """
            SELECT person.id, person.name, person.email, person.phone_number FROM person
            INNER JOIN person_physical
            ON person_physical.person = person.id
        """

    if id > 0:
        sql += f" WHERE person.id = {id}"

    if name != "":
        if sql.find("WHERE"):
            sql += f" WHERE person.name LIKE '%{name}%'"
        else:
            sql += f" AND person.name LIKE '%{name}%'"

    if email != "":
        if sql.find("WHERE"):
            sql += f" WHERE person.email LIKE '%{email}%'"
        else:
            sql += f" AND person.email LIKE '%{email}%'"

    if phone != "":
        if sql.find("WHERE"):
            sql += f" WHERE person.phone_number LIKE '%{phone}%'"
        else:
            sql += f" AND person.phone_number LIKE '%{phone}%'"
        sql += " LIMIT 1"

    curr.execute(sql)

    person = list(map(list, curr.fetchall()))

    curr.close()

    return person


def record_person(
    conn: object,
    tipo_operacao: bool = True,
    id: int = 0,
    name: str = "",
    email: str = "",
    phone_number: str = "",
) -> list:
    """Search people in the database.
    Parameter:
        conn (Database connection.)
        tipo_operacao (True = insert bank_account, False = update bank account.)
        id (id bank account.)
        name (Persons name.)
        email (person's email.)
        phone_number (person's phone.)
    Return:
        List with the person.
    """
    curr = conn.cursor()

    if phone_number == "":
        phone_number = "Null"

    if tipo_operacao:  # Insert
        sql = f"""
                INSERT INTO person(name, email, phone_number)
                VALUES ('{name}', '{email}', {phone_number})
                RETURNING id, name, email, phone_number
            """
    else:  # update
        sql = f"""
                UPDATE person
                SET name = '{name}',
                    email = '{email}',
                    phone_number = {phone_number}
                WHERE id = {id}
                RETURNING id, name, email, phone_number
            """
    curr.execute(sql)
    conn.commit()

    person = list(map(list, curr.fetchall()))

    curr.close()

    return person


def exclude_person(conn: object, id: int = 0) -> list:
    """Searches the person in the database.
    Parameter:
        conn (Database connection.)
        id (id person.)
    Return:
        List with the deleted person.
    """
    curr = conn.cursor()

    sql = f"DELETE from person WHERE id = {id} RETURNING id"
    curr.execute(sql)
    conn.commit()

    bank_agency = list(map(list, curr.fetchall()))

    curr.close()

    return bank_agency
