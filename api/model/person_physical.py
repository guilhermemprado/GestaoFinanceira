def search_person_physical(
    conn: object,
    person: int = 0,
    cpf: int = 0,
) -> list:
    """Searches the person adresses in the database.
    Parameter:
        conn (Database connection.)
        person (Enter id person to searching for a person_physical.)
        cpf (Enter cpf to searching for a person_physical.)
    Return:
        List physical
    """
    curr = conn.cursor()

    sql = """
            SELECT person_physical.person as id_person, person.name, person_physical.cpf
            FROM person_physical
            INNER JOIN person
            ON person_physical.person = person.id
        """
    if person > 0:
        if sql.find("WHERE") != -1:
            sql += f" AND person_physical.person = {person}"
        else:
            sql += f" WHERE person_physical.person = {person}"

    if cpf > 0:
        if sql.find("WHERE") != -1:
            sql += f" AND person_physical.cpf = '{cpf}'"
        else:
            sql += f" WHERE person_physical.cpf = '{cpf}'"

    curr.execute(sql)

    physical = list(map(list, curr.fetchall()))

    curr.close()

    return physical


def record_person_physical(
    conn: object,
    tipo_operacao: bool = True,
    id_physical: int = 0,
    person: int = 0,
    cpf: str = "",
) -> list:
    """Search address in the database.
    Parameter:
        conn (Database connection.)
        tipo_operacao (True = insert bank_account, False = update bank account.)
        id_physical (id physical.)
        person (id person)
        cpf (cpf person.)

    Return:
        List with the physical.
    """
    curr = conn.cursor()

    if tipo_operacao:  # Insert
        sql = f"""
                INSERT INTO person_physical(person, cpf)
                VALUES ({person}, '{cpf}')
                RETURNING id
            """
    else:  # update
        sql = f"""
                UPDATE person_physical
                SET person = {person},
                    cpf = '{cpf}'
                WHERE id = {id_physical}
                RETURNING id
            """

    curr.execute(sql)

    conn.commit()

    id_physical = list(map(list, curr.fetchall()))

    sql = f"""
            SELECT person_physical.person as id_person, person.name, person_physical.cpf
            FROM person_physical
            INNER JOIN person
            ON person_physical.person = person.id
            WHERE person_physical.id = {id_physical[0][0]}
        """
    curr.execute(sql)

    physical = list(map(list, curr.fetchall()))

    curr.close()

    return physical


def exclude_person_physical_id(conn: object, id_physical: int = 0) -> list:
    """Searches the address in the database.
    Parameter:
        conn (Database connection.)
        id_physical (id physical.)
    Return:
        List with the deleted physical.
    """
    curr = conn.cursor()

    sql = f"DELETE from person_physical WHERE id = {id_physical} RETURNING id"
    curr.execute(sql)
    conn.commit()

    physical = list(map(list, curr.fetchall()))

    curr.close()

    return physical
