from flask import redirect
from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI, Tag
from schemas.bank import BankSearchSchema, show_banks
from schemas.state import StateSearchSchema, show_states
from schemas.city import CitySearchSchema, show_cities
from schemas.bank_agency import BankAgencySearchSchema, show_bank_agency
from model.bank import search_banks
from model.state import search_states
from model.city import search_cities
from model.bank_agency import search_banks_agencies
from model.connection import Connect
from infra.constants.texts import (
    TITLE_APP,
    NAME_TAG_DOCUMENTATION,
    NAME_STATE_TAG,
    NAME_CITY_TAG,
    NAME_BANK_TAG,
    NAME_BANK_AGENCIES_TAG,
    NAME_BANK_ACCOUNTS_TAG,
    NAME_PEOPLE_TAG,
    NAME_ADRESSES_TAG,
    DESCRIPTION_TAG_DOCUMENTATION,
    DESCRIPTION_STATE_TAG,
    DESCRIPTION_CITY_TAG,
    DESCRIPTION_BANK_TAG,
    DESCRIPTION_BANK_AGENCIES_TAG,
    DESCRIPTION_BANK_ACCOUNTS_TAG,
    DESCRIPTION_PEOPLE_TAG,
    DESCRIPTION_ADRESSES_TAG,
)
from infra.config.settings import APP_VERSION

info = Info(title=TITLE_APP, version=APP_VERSION)
app = OpenAPI(__name__, info=info)
CORS(app)

connect = Connect()
conn = connect.postgres()

# Defining tags
home_tag = Tag(
    name=NAME_TAG_DOCUMENTATION,
    description=DESCRIPTION_TAG_DOCUMENTATION,
)
state_tag = Tag(name=NAME_STATE_TAG, description=DESCRIPTION_STATE_TAG)
city_tag = Tag(name=NAME_CITY_TAG, description=DESCRIPTION_CITY_TAG)
bank_tag = Tag(name=NAME_BANK_TAG, description=DESCRIPTION_BANK_TAG)
bank_agencies_tag = Tag(
    name=NAME_BANK_AGENCIES_TAG,
    description=DESCRIPTION_BANK_AGENCIES_TAG,
)
bank_accounts_tag = Tag(
    name=NAME_BANK_ACCOUNTS_TAG,
    description=DESCRIPTION_BANK_ACCOUNTS_TAG,
)
people_tag = Tag(name=NAME_PEOPLE_TAG, description=DESCRIPTION_PEOPLE_TAG)
Adresses_tag = Tag(name=NAME_ADRESSES_TAG, description=DESCRIPTION_ADRESSES_TAG)


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
    bank_agencies = search_banks_agencies(conn)

    return show_bank_agency(bank_agencies)


# List one bank agency
@app.get("/bank_agency", tags=[bank_agencies_tag])
def get_bank_agency(query: BankAgencySearchSchema):
    """Searches for a bank agency based on the agency based id

    Returns a representation of bank agency.
    """
    if query.number_agency == 0 and query.name_agency == "" and query.name_person == "":
        return """
        Informe pelo menos um dos dados!\n
        - Número da agencia!\n
        - Nome da agencia!\n
        - Nome do cliente!
        """

    banks_agencies = search_banks_agencies(
        conn, query.number_agency, query.name_agency.upper(), query.name_person.upper()
    )
    return show_bank_agency(banks_agencies)


# Add new bank agency
@app.post("/bank_agency", tags=[bank_agencies_tag])
def new_bank_agency():
    """Add a new bank agency to the database

    Returns a representation of bank agency.
    """
    return "Bank agency saved successfully"


# Change bank agency
@app.post("/bank_agency", tags=[bank_agencies_tag])
def update_bank_agency():
    """Change the selected bank agency

    Returns a representation of the bank agency.
    """
    return "Bank agency changed successfully"


# Delete bank agency
@app.delete("/bank_agency", tags=[bank_agencies_tag])
def delete_bank_agency():
    """Delete the reported bank agency

    Returns a removal confirmation message.
    """
    return "Bank agency delete successfully"


# Bank account.
# List all bank_account
@app.get("/bank_accounts", tags=[bank_accounts_tag])
def get_bank_accounts():
    """Search for all registered bank accounts

    Returns a representation of the bank accounts listing.
    """

    return "....................."


# List one bank account
@app.get("/bank_account", tags=[bank_accounts_tag])
def get_bank_account():
    """Searches for a bank account based on the bank account id

    Returns a representation of bank account.
    """
    return "Bank account does not exist"


# Add new bank account
@app.post("/bank_account", tags=[bank_accounts_tag])
def new_bank_account():
    """Add a new bank account to the database

    Returns a representation of bank account.
    """
    return "Bank account saved successfully"


# Change bank account
@app.post("/bank_account", tags=[bank_accounts_tag])
def update_bank_account():
    """Change the selected bank account

    Returns a representation of the bank account.
    """
    return "Bank account changed successfully"


# Delete bank account
@app.delete("/bank_account", tags=[bank_accounts_tag])
def delete_bank_account():
    """Delete the reported bank account

    Returns a removal confirmation message.
    """
    return "Bank account delete successfully"


# person.
# List all people
@app.get("/people", tags=[people_tag])
def get_people():
    """Search for all registered people

    Returns a representation of the people listing.
    """
    return "No registered people"


# List one person
@app.get("/person", tags=[people_tag])
def get_person():
    """Searches for a person based on the person id

    Returns a representation of person.
    """
    return "Person does not exist"


# Add new person
@app.post("/person", tags=[people_tag])
def new_person():
    """Add a new person to the database

    Returns a representation of person.
    """
    return "Person saved successfully"


# Change person
@app.post("/update_person", tags=[people_tag])
def update_person():
    """Altera o person selecionado

    Returns a representation of the person.
    """
    return "Person changed successfully"


# Delete person
@app.delete("/person", tags=[people_tag])
def delete_person():
    """Delete the reported person

    Returns a removal confirmation message.
    """
    return "Person delete successfully"


# Address.
# List all Adresses
@app.get("/Adresses", tags=[Adresses_tag])
def get_adresses():
    """Search for all registered Adresses

    Returns a representation of the Adresses listing.
    """
    return "No registered Adresses"


# List one address
@app.get("/address", tags=[Adresses_tag])
def get_address():
    """Searches for a address based on the address id

    Returns a representation of address.
    """
    return "Address does not exist"


# Add new address
@app.post("/address", tags=[Adresses_tag])
def new_address():
    """Add a new address to the database

    Returns a representation of address.
    """
    return "Address saved successfully"


# Change address
@app.post("/update_address", tags=[Adresses_tag])
def update_address():
    """Altera o address selecionado

    Returns a representation of the address.
    """
    return "Address changed successfully"


# Delete address
@app.delete("/address", tags=[Adresses_tag])
def delete_address():
    """Delete the reported address

    Returns a removal confirmation message.
    """
    return "Address delete successfully"
