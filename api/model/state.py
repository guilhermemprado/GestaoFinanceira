def search_states(conn: object, state: str = "") -> list:
    """Searches the states in the database.
    Parameter: conn (Database connection.)
                state (Enter the state code when searching for a state.)
    Return: List states
    """
    curr = conn.cursor()

    sql = """
            SELECT ibge_number, acronym
            FROM uf
        """

    if state != "":
        sql += f" WHERE acronym = '{state}'"

    curr.execute(sql)

    states = list(map(list, curr.fetchall()))

    curr.close()

    return states
