def check_bank_exists(conn: object, id_bank: int) -> int:
    """Checks if the bank exists in the database.
    Parameter:
        conn (Database connection.)
        id_bank (Id bank.)
    Return:
        Bank number registered in the database.
    """
    curr = conn.cursor()

    sql = f"SELECT bb_central_number FROM bank WHERE bb_central_number = {id_bank}"

    curr.execute(sql)

    result = list(map(list, curr.fetchall()))

    curr.close()

    return len(result)


def check_agency_exists(conn, id_agency: int) -> int:
    """Checks if the agency exists in the database.
    Parameter:
        conn (Database connection.)
        id_agency (Id agency.)
    Return:
        Agency number registered in the database.
    """
    curr = conn.cursor()

    sql = f"SELECT id FROM bank_agency WHERE id = {id_agency}"

    curr.execute(sql)

    result = list(map(list, curr.fetchall()))

    curr.close()

    return len(result)


def check_have_agency_in_account(conn, agency: int) -> int:
    """Check if you have accounts linked to the agency in the database.
    Parameter:
        conn (Database connection.)
        id (Id agency.)
    Return:
        Agency number registered in the database.
    """
    curr = conn.cursor()

    sql = f"SELECT agency FROM bank_account WHERE agency = {agency}"

    curr.execute(sql)

    result = list(map(list, curr.fetchall()))

    curr.close()

    return len(result)


def check_account_exists(conn, id_account: int) -> int:
    """Check if you have accounts linked to the agency in the database.
    Parameter:
        conn (Database connection.)
        id_account (Id agency.)
    Return:
        Agency number registered in the database.
    """
    curr = conn.cursor()

    sql = f"SELECT id FROM bank_account WHERE id = {id_account}"

    curr.execute(sql)

    result = list(map(list, curr.fetchall()))

    curr.close()

    return len(result)


def check_account_number_exists(conn, account_number: int) -> int:
    """Check if you have accounts linked to the agency in the database.
    Parameter:
        conn (Database connection.)
        account_number (Number account.)
    Return:
        Bank account table ID.
    """
    curr = conn.cursor()

    sql = f"SELECT id FROM bank_account WHERE account_number = {account_number} ORDER BY id DESC LIMIT 1"

    curr.execute(sql)

    result = list(map(list, curr.fetchall()))

    if len(result) > 0:
        id_account = result[0][0]
    else:
        id_account = 0

    curr.close()

    return id_account


def check_person_exists(conn, id_person: int) -> int:
    """Check if you have accounts linked to the person in the database.
    Parameter:
        conn (Database connection.)
        id_person (Id person.)
    Return:
        Person number registered in the database.
    """
    curr = conn.cursor()

    sql = f"SELECT id FROM person WHERE id = {id_person}"

    curr.execute(sql)

    result = list(map(list, curr.fetchall()))

    curr.close()

    return len(result)


def check_city_exists(conn, id_city: int) -> int:
    """Check if you have accounts linked to the city in the database.
    Parameter:
        conn (Database connection.)
        id_city (Id city.)
    Return:
        City ibge_number registered in the database.
    """
    curr = conn.cursor()

    sql = f"SELECT ibge_number FROM city WHERE ibge_number = {id_city}"

    curr.execute(sql)

    result = list(map(list, curr.fetchall()))

    curr.close()

    return len(result)


def valida_cpf(cpf):
    cpf = cpf.replace(".", "").replace("-", "")

    if len(cpf) == 11:
        validar = True
        digitos_verificadores = cpf[9:]
    else:
        validar = False

    cpf = cpf[:9]

    try:
        dig_1 = int(cpf[0]) * 1
        dig_2 = int(cpf[1]) * 2
        dig_3 = int(cpf[2]) * 3
        dig_4 = int(cpf[3]) * 4
        dig_5 = int(cpf[4]) * 5
        dig_6 = int(cpf[5]) * 6
        dig_7 = int(cpf[6]) * 7
        dig_8 = int(cpf[7]) * 8
        dig_9 = int(cpf[8]) * 9
    except IndexError:
        print()
        print("Quantidade de caracteres incorreto.", end="\n\n")
        exit()

    dig_1_ao_9_somados = dig_1 + dig_2 + dig_3 + dig_4 + dig_5 + dig_6 + dig_7 + dig_8 + dig_9

    dig_10 = dig_1_ao_9_somados % 11

    if dig_10 > 9:
        dig_10 = 0

    cpf += str(dig_10)

    dig_1 = int(cpf[0]) * 0
    dig_2 = int(cpf[1]) * 1
    dig_3 = int(cpf[2]) * 2
    dig_4 = int(cpf[3]) * 3
    dig_5 = int(cpf[4]) * 4
    dig_6 = int(cpf[5]) * 5
    dig_7 = int(cpf[6]) * 6
    dig_8 = int(cpf[7]) * 7
    dig_9 = int(cpf[8]) * 8
    dig_10 = int(cpf[9]) * 9

    dig_1_ao_10_somados = dig_1 + dig_2 + dig_3 + dig_4 + dig_5 + dig_6 + dig_7 + dig_8 + dig_9 + dig_10

    dig_11 = dig_1_ao_10_somados % 11

    if dig_11 > 9:
        dig_11 = 0

    cpf_validado = cpf + str(dig_11)

    cpf = cpf_validado[:3] + "." + cpf_validado[3:6] + "." + cpf_validado[6:9] + "-" + cpf_validado[9:]

    if validar:
        if digitos_verificadores == cpf_validado[9:]:
            return True
        else:
            return False
    else:
        return False
