def search_person_address(
    conn: object,
    person: int = 0,
    city: int = 0,
    district: str = "",
) -> list:
    """Searches the person adresses in the database.
    Parameter:
        conn (Database connection.)
        id (Enter id code to searching for a person.)
        person (Enter id person to searching for a adresses.)
        city (Enter id city to searching for a adresses.)
        district (Enter district to search for a adresses.)
    Return:
        List banks
    """
    curr = conn.cursor()

    sql = """
            SELECT person.id as id_person, person.name as person, 
                city.ibge_number as id_city, city.name as city,
                address.street, address.number, address.district, 
                address.complement, address.cep
            FROM address
            INNER JOIN person
            ON address.person = person.id
            INNER JOIN city
            ON address.city = city.ibge_number
        """
    if person > 0:
        if sql.find("WHERE") != -1:
            sql += f" AND person.id = {person}"
        else:
            sql += f" WHERE person.id = {person}"

    if city > 0:
        if sql.find("WHERE") != -1:
            sql += f" AND city.ibge_number = {city}"
        else:
            sql += f" WHERE city.ibge_number = {city}"

    if district != "":
        if sql.find("WHERE") != -1:
            sql += f" AND address.district LIKE '%{district}%'"
        else:
            sql += f" WHERE address.district LIKE '%{district}%'"

    curr.execute(sql)

    person = list(map(list, curr.fetchall()))

    curr.close()

    return person


def record_person_address(
    conn: object,
    tipo_operacao: bool = True,
    id: int = 0,
    person: int = 0,
    city: int = 0,
    cep: str = "",
    street: str = "",
    number: int = 0,
    district: str = "",
    complement: str = "",
) -> list:
    """Search address in the database.
    Parameter:
        conn (Database connection.)
        tipo_operacao (True = insert bank_account, False = update bank account.)
        id (id person.)
        person (Id person)
        city (Id city.)
        cep (Address cep.)
        number (Address number .)
        street (Address street.)
        complement (Address complement.)

    Return:
        List with the address.
    """
    curr = conn.cursor()

    if tipo_operacao:  # Insert
        sql = f"""
                INSERT INTO address(person, city, cep, street, number, district, complement)
                VALUES ({person}, {city}, {cep}, '{street}', {number}, '{district}', '{complement}')
                RETURNING id
            """
    else:  # update
        sql = f"""
                UPDATE address
                SET person = {person},
                    city = {city},
                    cep = {cep},
                    street = '{street}',
                    number = {number},
                    district = '{district}',
                    complement = '{complement}'
                WHERE id = {id}
                RETURNING id
            """

    curr.execute(sql)
    
    conn.commit()

    id_address = list(map(list, curr.fetchall()))

    sql = f"""
            SELECT address.id, person.name as person, city.name as city, address.cep,
                address.street, address.number, address.district, address.complement
            FROM address
            INNER JOIN person
            ON address.person = person.id
            INNER JOIN city
            ON address.city = city.ibge_number
            WHERE address.id = {id_address[0][0]}
        """
    curr.execute(sql)
    
    address = list(map(list, curr.fetchall()))

    curr.close()

    return address


def exclude_person_address(conn: object, id: int = 0) -> list:
    """Searches the address in the database.
    Parameter:
        conn (Database connection.)
        id (id address.)
    Return:
        List with the deleted address.
    """
    curr = conn.cursor()

    sql = f"DELETE from address WHERE id = {id} RETURNING id"
    curr.execute(sql)
    conn.commit()

    address = list(map(list, curr.fetchall()))

    curr.close()

    return address
