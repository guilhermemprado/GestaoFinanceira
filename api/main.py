from flask import redirect
from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI
from schemas.bank import BankSearchSchema, show_banks
from schemas.state import StateSearchSchema, show_states
from schemas.city import CitySearchSchema, show_cities
from schemas.bank_agency import BankAgencySearchSchema, BankAgencyIdSearchSchema, show_bank_agency
from schemas.bank_account import BankAccountSearchSchema, BankAccountIdSearchSchema, show_bank_account
from schemas.person import show_person, PersonSearchSchema, PersonIdSearchSchema
from schemas.moviment import show_moviments, MovimentSearchSchema, MovimentIdSearchSchema, MovimentAllSearchSchema
from schemas.person_address import (
    show_person_address,
    PersonAddressSearchSchema,
    PersonAddressIdSearchSchema,
    PersonAllAddressSearchSchema,
)
from schemas.person_physical import (
    show_person_physical,
    PersonPhysicalSearchSchema,
    PersonPhysicalIdSearchSchema,
    PersonAllPhysicalSearchSchema,
)
from model.bank import search_banks
from model.state import search_states
from model.city import search_cities
from model.bank_agency import search_banks_agencies, record_banks_agencies, delete_banks_agencies
from model.bank_account import search_banks_accounts, record_banks_accounts, delete_banks_accounts
from model.person import search_person, record_person, exclude_person
from model.person_address import search_person_address, record_person_address, exclude_person_address
from model.person_physical import search_person_physical, record_person_physical, exclude_person_physical_id
from model.moviment import search_moviments, record_moviment, exclude_moviment
from model.validations import (
    check_bank_exists,
    check_agency_exists,
    check_account_exists,
    check_account_number_exists,
    check_have_agency_in_account,
    check_person_exists,
    check_city_exists,
    valida_cpf,
)
from model.connection import Connect
from application.tags import (
    home_tag,
    state_tag,
    city_tag,
    bank_tag,
    bank_agencies_tag,
    bank_accounts_tag,
    people_tag,
    Adresses_tag,
    Physical_tag,
    Moviment_tag,
)
from infra.constants.texts import TITLE_APP
from infra.config.settings import APP_VERSION

info = Info(title=TITLE_APP, version=APP_VERSION)
app = OpenAPI(__name__, info=info)
CORS(app)

connect = Connect()
conn = connect.postgres()


# Documentation.
@app.get("/", tags=[home_tag])
def home():
    """Redirects to /openapi, screen that allows choosing the documentation style."""
    return redirect("/openapi")


# Bank.
# List all banks
@app.get("/banks", tags=[bank_tag])
def get_banks():
    """Search for all registered banks

    Return: Representation of the banks in listing.
    """

    banks = search_banks(conn)

    return show_banks(banks)


# List bank
@app.get("/bank", tags=[bank_tag])
def get_bank(query: BankSearchSchema):
    """Bank list by code

    Return: Representation of the bank in listing.
    """
    if query.number != 0:
        banks = search_banks(conn, query.number)
        return show_banks(banks)
    else:
        return "Informe o número do banco!"


# States.
# List all states
@app.get("/states", tags=[state_tag])
def get_states():
    """Search for all registered states

    Returns a representation of the states listing.
    """
    states = search_states(conn)

    return show_states(states)


# List states
@app.get("/state", tags=[state_tag])
def get_state(query: StateSearchSchema):
    """State list by uf

    Returns Representation of the states listing.
    """
    if query.state.upper() != "":
        states = search_states(conn, query.state.upper())
        return show_states(states)
    else:
        return "Infome a sigla do estado(UF)!"


# Cities
# List all cities
@app.get("/cities", tags=[city_tag])
def get_cities():
    """Search for all registered cities

    Returns a representation of the cities listing.
    """
    cities = search_cities(conn)

    return show_cities(cities)


# List city
@app.get("/city", tags=[city_tag])
def get_city(query: CitySearchSchema):
    """City list by name or uf

    Returns a representation of the cities listing.
    """
    if query.name == "" and query.uf == "":
        return """
        Informe pelo menos um dos dados!\n
        - Nome da cidade.\n
        - Sigla do estado(UF).
        """

    cities = search_cities(conn, query.name.upper(), query.uf.upper())
    return show_cities(cities)


# Bank agency.
# List all bank agencies
@app.get("/bank_agencies", tags=[bank_agencies_tag])
def get_bank_agencies():
    """Search for all registered bank agencies

    Returns a representation of the bank agencies listing.
    """
    banks_agencies = search_banks_agencies(conn)

    return show_bank_agency(banks_agencies)


# List one bank agency
@app.get("/bank_agency", tags=[bank_agencies_tag])
def get_bank_agency(query: BankAgencySearchSchema):
    """Searches for a bank agency based on the agency based id

    Returns a representation of bank agency.
    """
    if query.number_agency == 0 and query.name_agency == "" and query.number_bank == 0:
        message = """
        Informe pelo menos um dos dados!\n
        - Número da agencia!\n
        - Número do bank!\n
        - Nome da agencia!\n
        """
        return message

    banks_agencies = search_banks_agencies(conn, query.number_agency, query.name_agency.upper(), query.number_bank)

    return show_bank_agency(banks_agencies)


# Add new bank agency
@app.post("/bank_agency", tags=[bank_agencies_tag])
def new_bank_agency(form: BankAgencySearchSchema):
    """Add a new bank agency to the database

    Returns a representation of bank agency.
    """
    try:
        if form.number_agency == 0 and form.name_agency == "" and form.number_bank == 0:
            message = """
            Informe os dos dados!
            - Número da agencia!
            - Número do bank!
            - Nome da agencia!
            """
            return message

        if check_bank_exists(conn, form.number_bank) == 0:
            return "Banco informado não consta na base de dados!"

        bank_agency = record_banks_agencies(
            conn, True, 0, form.number_agency, form.name_agency.upper(), form.number_bank
        )

        return show_bank_agency(bank_agency)

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível inserir o banco agência."
        return {"message": error_msg}


# Change bank agency
@app.put("/bank_agency", tags=[bank_agencies_tag])
def update_bank_agency(query: BankAgencyIdSearchSchema, form: BankAgencySearchSchema):
    """Change the selected bank agency

    Returns a representation of the bank agency.
    """
    try:
        if query.id == 0:
            return "Informe o id do banco agência!"

        if check_bank_exists(conn, form.number_bank) == 0:
            return "Banco informado não consta na base de dados!"

        if check_agency_exists(conn, query.id) == 0:
            return "Agência informada não consta na base de dados!"

        if form.number_agency == 0 and form.name_agency == "" and form.number_bank == 0:
            message = """
            Informe os dos dados!
            - Número da agência!
            - Número do bank!
            - Nome da agência!
            """
            return message

        if check_bank_exists(conn, form.number_bank) == 0:
            return "Banco informado não consta na base de dados!"

        if check_agency_exists(conn, query.id) == 0:
            return "Agência informada não consta na base de dados!"

        bank_agency = record_banks_agencies(
            conn, False, query.id, form.number_agency, form.name_agency.upper(), form.number_bank
        )

        return show_bank_agency(bank_agency)

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível alterar o banco agência."
        return {"message": error_msg}, 400


# Delete bank agency
@app.delete("/bank_agency", tags=[bank_agencies_tag])
def delete_bank_agency(query: BankAgencyIdSearchSchema):
    """Delete the reported bank agency

    Returns a removal confirmation message.
    """
    try:
        if query.id == 0:
            return "Informe o id do banco agência, que deseja deletar!"

        if check_have_agency_in_account(conn, query.id) > 0:
            return "Agência nao pode ser deletada, existem contas viculadas a agência!"

        if check_agency_exists(conn, query.id) == 0:
            return "Agência informada não consta na base de dados!"

        result = delete_banks_agencies(conn, query.id)

        return {"Banco agência deletado com sucesso, Id:": result[0][0]}

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível deletar a agência."
        return {"message": error_msg}, 400


# Bank account.
# List all bank_account
@app.get("/bank_accounts", tags=[bank_accounts_tag])
def get_bank_accounts():
    """Search for all registered bank account

    Returns a representation of the bank account listing.
    """
    bank_account = search_banks_accounts(conn)

    return show_bank_account(bank_account)


# List one bank account
@app.get("/bank_account", tags=[bank_accounts_tag])
def get_bank_account(query: BankAccountSearchSchema):
    """Searches for a bank account based on the account based id

    Returns a representation of bank account.
    """
    if query.account_number == 0 and query.id_person == 0 and query.agency_number == 0:
        message = """
        Informe pelo menos um dos dados!\n
        - Número da conta!\n
        - Número da agência!\n
        - Id da pessoa/empresa!\n
        """
        return message

    banks_acconts = search_banks_accounts(conn, 0, query.account_number, query.id_person, query.agency_number)

    return show_bank_account(banks_acconts)


# Add new bank account
@app.post("/bank_account", tags=[bank_accounts_tag])
def new_bank_account(form: BankAccountSearchSchema):
    """Add a new bank account to the database

    Returns a representation of bank account.
    """
    try:
        if form.account_number == 0 and form.id_person == 0 and form.agency_number == 0:
            message = """
            Informe os dos dados!
            - Número da conta!\n
            - Número da agência!\n
            - Id da pessoa/empresa!\n
            """
            return message

        if check_agency_exists(conn, form.agency_number) == 0:
            return "Agência informada não consta na base de dados!"

        if check_bank_exists(conn, form.id_person) == 0:
            return "Banco informado não consta na base de dados!"

        bank_account = record_banks_accounts(conn, True, 0, form.account_number, form.id_person, form.agency_number)

        return show_bank_account(bank_account)

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível inserir a conta no banco."
        return {"message": error_msg}


# Change bank account
@app.put("/bank_account", tags=[bank_accounts_tag])
def update_bank_account(query: BankAccountIdSearchSchema, form: BankAccountSearchSchema):
    """Change the selected bank account

    Returns a representation of the bank account.
    """
    try:
        if query.id == 0:
            return "Informe o id do banco account!"

        if check_account_exists(conn, query.id) == 0:
            return "Conta informada não consta na base de dados!"

        if check_agency_exists(conn, form.agency_number) == 0:
            return "Agência informada não consta na base de dados!"

        if check_bank_exists(conn, form.id_person) == 0:
            return "Banco informado não consta na base de dados!"

        if form.account_number == 0 and form.id_person == 0 and form.agency_number == 0:
            message = """
            Informe os dos dados!
            - Número da conta!\n
            - Número da agência!\n
            - Id da pessoa/empresa!\n
            """
            return message

        bank_agency = record_banks_accounts(
            conn, False, query.id, form.account_number, form.id_person, form.agency_number
        )

        return show_bank_account(bank_agency)

    except Exception as error:
        # caso um erro fora do previsto
        error_msg = "Não foi possível alterar a conta do banco."
        return {"message": error_msg}, error


# Delete bank account
@app.delete("/bank_account", tags=[bank_accounts_tag])
def delete_bank_account(query: BankAccountIdSearchSchema):
    """Delete the reported bank agency

    Returns a removal confirmation message.
    """
    try:
        if query.id == 0:
            return "Informe o id da conta banco, que deseja deletar!"

        if check_account_exists(conn, query.id) == 0:
            return "Conta informada, não existe na base de dados!"

        result = delete_banks_accounts(conn, query.id)

        return {"Conta banco deletado com sucesso, Id:": result[0][0]}

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível deletar o banco agência."
        return {"message": error_msg}, 400


# person.
# List all people
@app.get("/people", tags=[people_tag])
def get_people():
    """Search for all registered people

    Returns a representation of the people listing.
    """
    person = search_person(conn)

    return show_person(person)


# List one person
@app.get("/person", tags=[people_tag])
def get_person(query: PersonSearchSchema):
    """Searches for a person based on the person id

    Returns a representation of person.
    """
    if query.name == "" and query.email == "" and query.phone_number == "":
        message = """
        Informe pelo menos um dos dados!\n
        - Nome!\n
        - E-mail!\n
        - Número do telefone!
        """
        return message

    person = search_person(conn, 0, query.name.upper(), query.email.upper(), query.phone_number)

    return show_person(person)


# Add new person
@app.post("/person", tags=[people_tag])
def new_person(form: PersonSearchSchema):
    """Add a new person to the database

    Returns a representation of person.
    """
    try:
        if form.name == "" and form.email == "" and form.phone_number == "":
            message = """
            Informe os dos dados!
            - Nome!\n
            - Email!\n
            - Número do telefone!\n
            """
            return message

        person = record_person(conn, True, 0, form.name.upper(), form.email.upper(), form.phone_number)

        return show_person(person)

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível inserir a conta no banco."
        return {"message": error_msg}


# Change person
@app.post("/update_person", tags=[people_tag])
def update_person(query: PersonIdSearchSchema, form: PersonSearchSchema):
    """Update person select

    Returns a representation of the person.
    """
    try:
        if query.id == 0:
            return "Informe o id da pessoa/empresa!"

        if form.name == "" and form.email == "" and form.phone_number == "":
            message = """
            Informe os dos dados!
            - Nome pessoa/empresa!\n
            - E-mail!\n
            - Número telefone!\n
            """
            return message

        person = record_person(conn, 0, query.id, form.name.upper(), form.email.upper(), form.phone_number)

        return show_person(person)

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível alterar os dados da pessoa."
        return {"message": error_msg}


# Delete person
@app.delete("/person", tags=[people_tag])
def delete_person(query: BankAccountIdSearchSchema):
    """Delete the reported person

    Returns a removal confirmation message.
    """
    try:
        if query.id == 0:
            return "Informe o id da pessoa/empresa, que deseja deletar!"

        if check_person_exists(conn, query.id) == 0:
            return "Pessoa/Empresa, não existe na base de dados!"

        result = exclude_person(conn, query.id)

        return {"Pessoa/Empresa deletada com sucesso, Id:": result[0][0]}

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível deletar a pessoa/empresa."
        return {"message": error_msg}, 400


# Address.
# List all Adresses
@app.get("/Adresses", tags=[Adresses_tag])
def get_adresses():
    """Search for all registered Adresses

    Returns a representation of the Adresses listing.
    """
    person_address = search_person_address(conn)

    return show_person_address(person_address)


# List one address
@app.get("/address", tags=[Adresses_tag])
def get_address(query: PersonAddressSearchSchema):
    """Searches for a address based on the address id

    Returns a representation of address.
    """
    if (
        query.person == 0
        and query.city == 0
        and query.cep == ""
        and query.street == ""
        and query.number == 0
        and query.district == ""
        and query.complement == ""
    ):
        message = """
        Informe pelo menos um dos dados!\n
        - Pessoa/Empresa
        - Cidade!\n
        - Cep!\n
        - Rua
        - Número
        - Bairro
        - Complemento
        """
        return message

    person = search_person_address(conn, query.person, query.city, query.district.upper())

    return show_person_address(person)


# Add new address
@app.post("/address", tags=[Adresses_tag])
def new_address(form: PersonAllAddressSearchSchema):
    """Add a new address to the database

    Returns a representation of address.
    """
    try:
        if (
            form.person == 0
            and form.city == 0
            and form.cep == ""
            and form.street == ""
            and form.number == 0
            and form.district == ""
            and form.complement == ""
        ):
            message = """
            Informe pelo menos um dos dados!\n
            - Pessoa/Empresa
            - Cidade!\n
            - Cep!\n
            - Rua
            - Número
            - Bairro
            - Complemento
            """
            return message

        if check_person_exists(conn, form.person) == 0:
            return "Pessoa/Empresa, não existe na base de dados!"

        if check_city_exists(conn, form.city) == 0:
            return "Cidade, não existe na base de dados!"

        address = record_person_address(
            conn, True, 0, form.person, form.city, form.cep, form.street, form.number, form.district, form.complement
        )

        return show_person_address(address)

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível inserir a conta no banco."
        return {"message": error_msg}


# Change address
@app.post("/update_address", tags=[Adresses_tag])
def update_address(query: PersonAddressIdSearchSchema, form: PersonAllAddressSearchSchema):
    """Altera o address selecionado

    Returns a representation of the address.
    """
    try:
        if (
            form.person == 0
            and form.city == 0
            and form.cep == ""
            and form.street == ""
            and form.number == 0
            and form.district == ""
            and form.complement == ""
        ):
            message = """
            Informe pelo menos um dos dados!\n
            - Pessoa/Empresa
            - Cidade!\n
            - Cep!\n
            - Rua
            - Número
            - Bairro
            - Complemento
            """

            return message

        if check_person_exists(conn, form.person) == 0:
            return "Pessoa/Empresa, não existe na base de dados!"

        if check_city_exists(conn, form.city) == 0:
            return "Cidade, não existe na base de dados!"

        address = record_person_address(
            conn,
            False,
            query.id,
            form.person,
            form.city,
            form.cep,
            form.street,
            form.number,
            form.district,
            form.complement,
        )

        return show_person_address(address)

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível inserir a conta no banco."
        return {"message": error_msg}


# Delete address
@app.delete("/address", tags=[Adresses_tag])
def delete_address(query: PersonAddressIdSearchSchema):
    """Delete the reported address

    Returns a removal confirmation message.
    """
    try:
        if query.id == 0:
            return "Informe o id do endereço, que deseja deletar!"

        if check_person_exists(conn, query.id) == 0:
            return "Endereço, não existe na base de dados!"

        result = exclude_person_address(conn, query.id)

        return {"Endereço deletado com sucesso, Id:": result[0][0]}

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível deletar o endereço."
        return {"message": error_msg}, 400


# physical.
# List all physical
@app.get("/physics", tags=[Physical_tag])
def get_physics():
    """Search for all registered physical

    Returns a representation of the physical listing.
    """
    person_physical = search_person_physical(conn)

    return show_person_physical(person_physical)


# List one physical
@app.get("/physicals", tags=[Physical_tag])
def get_physicals(query: PersonPhysicalSearchSchema):
    """Searches for a physical based on the address id

    Returns a representation of physical.
    """
    if query.person == 0 and query.cpf == 0:
        message = """
        Informe pelo menos um dos dados!\n
        - Pessoa
        - cpf!\n
        """
        return message

    physical = search_person_physical(conn, query.person, query.cpf)

    return show_person_physical(physical)


# Add new physical
@app.post("/physical", tags=[Physical_tag])
def new_physical(form: PersonAllPhysicalSearchSchema):
    """Add a new address to the physical

    Returns a representation of physical.
    """
    try:
        if form.person == 0 and form.cpf == 0:
            message = """
            Informe pelo menos um dos dados!\n
            - Pessoa
            - cpf
            """
            return message

        if check_person_exists(conn, form.person) == 0:
            return "Pessoa, não existe na base de dados!"

        if not valida_cpf(str(form.cpf)):
            message = "Cpf informado não e válido!"
            return message

        physical = record_person_physical(conn, True, 0, form.person, form.cpf)

        return show_person_physical(physical)

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível inserir o person physical."
        return {"message": error_msg}


# Change physical
@app.post("/update_physical", tags=[Physical_tag])
def update_physical(query: PersonPhysicalIdSearchSchema, form: PersonAllPhysicalSearchSchema):
    """Altera o physical selecionado

    Returns a representation of the address.
    """
    try:
        if form.person == 0 and form.cpf == 0:
            message = """
            Informe pelo menos um dos dados!\n
            - Pessoa
            - Cpf
            """
            return message

        if check_person_exists(conn, form.person) == 0:
            return "Pessoa, não existe na base de dados!"

        if not valida_cpf(str(query.cpf)):
            message = "Cpf informado não e válido!"
            return message

        address = record_person_physical(
            conn,
            False,
            query.id,
            form.person,
            form.cpf,
        )

        return show_person_physical(address)

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível inserir a person physical."
        return {"message": error_msg}


# Delete physical
@app.delete("/physical", tags=[Physical_tag])
def delete_physical(query: PersonPhysicalIdSearchSchema):
    """Delete the reported physical

    Returns a removal confirmation message.
    """
    try:
        if query.id == 0:
            return "Informe o id da pessoa fisica, que deseja deletar!"

        if check_person_exists(conn, query.id) == 0:
            return "Pessoa fisica, não existe na base de dados!"

        result = exclude_person_physical_id(conn, query.id)

        return {"Pessoa fisica deletada com sucesso, Id:": result[0][0]}

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível deletar a pessoa fisica."
        return {"message": error_msg}, 400


# moviment.
# List all moviments
@app.get("/moviments", tags=[Moviment_tag])
def get_moviments():
    """Search for all registered moviments

    Returns a representation of the moviments listing.
    """
    moviments = search_moviments(conn)

    return show_moviments(moviments)


# List one moviment
@app.get("/moviment", tags=[Moviment_tag])
def get_moviment(query: MovimentSearchSchema):
    """Search for registered moviment

    Returns a representation of the moviment listing.
    """
    if query.account_number == 0 and query.description == "" and query.date == "":
        message = """
        Informe pelo menos um dos dados!\n
        - Número da conta
        - Descrição do movimento!\n
        - Data do movimento
        """
        return message

    moviment = search_moviments(conn, query.account_number, query.description, query.date)

    return show_moviments(moviment)


# Add new moviment
@app.post("/moviment", tags=[Moviment_tag])
def new_moviment(form: MovimentAllSearchSchema):
    """Add a new moviment to the moviment

    Returns a representation of moviment.
    """
    try:
        if form.account_number == 0 and form.description.upper() == "" and form.date == "":
            message = """
            Informe pelo menos um dos dados!\n
            - Número da conta.
            - Descrição do movimento.
            - Data do movimento.
            """
            return message

        id_account = check_account_number_exists(conn, form.account_number)
        if id_account == 0:
            return "Conta informada não consta na base de dados!"

        date = form.date.replace("/", "")
        date = date.replace("-", "")

        if len(date) != 8:
            return "Data deve ter o formato de dd/mm/yyyy."

        moviment = record_moviment(conn, True, 0, id_account, form.description, form.value, date)

        return show_moviments(moviment)

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível inserir o person physical."
        return {"message": error_msg}


# Change moviment
@app.post("/update_moviment", tags=[Moviment_tag])
def update_moviment(query: MovimentIdSearchSchema, form: MovimentAllSearchSchema):
    """Aler moviment selected.

    Returns a representation of the moviment.
    """
    try:
        if form.account_number == 0 and form.description == "" and form.value == 0 and form.date == "":
            message = """
            Informe pelo menos um dos dados!\n
            - Número da conta.
            - Descrição do movimento.
            - Valor do movimento.
            - Data do movimento.
            """
            return message

        date = form.date.replace("/", "")
        date = date.replace("-", "")

        if len(date) != 8:
            return "Data deve ter o formato de dd/mm/yyyy."

        id_account = check_account_number_exists(conn, form.account_number)
        if id_account == 0:
            return "Conta informada não consta na base de dados!"

        moviment = record_moviment(conn, False, query.id, id_account, form.description.upper(), form.value, date)

        return show_moviments(moviment)

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível inserir o movimento."
        return {"message": error_msg}


# Delete moviment
@app.delete("/moviment", tags=[Moviment_tag])
def delete_moviment(query: MovimentIdSearchSchema):
    """Delete the reported physical

    Returns a removal confirmation message.
    """
    try:
        if query.id == 0:
            return "Informe o id da pessoa fisica, que deseja deletar!"

        result = exclude_moviment(conn, query.id)

        return {"Movimento deletada com sucesso, Id:": result[0][0]}

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível deletar o movimento."
        return {"message": error_msg}, 400
