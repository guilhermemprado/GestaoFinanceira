def search_cities(conn: object, name: str = "", uf: str = "") -> list:
    """Searches the cities in the database.
    Parameter: conn (Database connection.)
                name (Enter the city name to search for the city.)
                uf (Enter the state acronym to search for the city.)
    Return: List cities
    """
    curr = conn.cursor()

    sql = """
            SELECT city.ibge_number, uf.acronym, city.name
            FROM city
            INNER JOIN uf ON city.uf = uf.ibge_number
        """

    if name != "":
        sql += f" WHERE city.name like '%{name}%'"

    if uf != "":
        if sql.find("WHERE"):
            sql += f" AND uf.acronym = '{uf}'"
        else:
            sql += f" WHERE uf.acronym = '{uf}'"

    curr.execute(sql)

    cities = list(map(list, curr.fetchall()))

    curr.close()

    return cities
