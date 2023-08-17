"""
    Imports
"""
from urllib.parse import unquote

from flask import redirect
from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI, Tag

info = Info(title="Gestão financeira", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(
    name="Documentation",
    description="Documentation selection: Swagger, Redoc or RapiDoc.",
)
state_tag = Tag(name="State", description="Create, Change, delete and view states based.")
city_tag = Tag(name="City", description="Create, Change, delete and view cities based.")

# Documentação.
@app.get("/", tags=[home_tag])
def home():
    """ Redirects to /openapi, screen that allows choosing the documentation style. """
    return redirect("/openapi")

### States. ###
# List all states.
@app.get("/states", tags=[state_tag])
def get_states():
    """ Search for all registered states

    Returns a representation of the states listing.
    """
    return "No registered states"

# List one state.
@app.get("/state", tags=[state_tag])
def get_state():
    """ Searches for a state based on the state id

    Returns a representation of state.
    """
    return "State does not exist"

# Add new state.
@app.post("/state", tags=[state_tag])
def new_state():
    """ Add a new state to the database

    Returns a representation of state.
    """
    return "State saved successfully"

# Change state
@app.post("/update_state", tags=[state_tag])
def update_state():
    """ Change the selected state

    Returns a representation of the state.
    """
    return "State changed successfully"

# Delete state
@app.delete("/state", tags=[state_tag])
def delete_state():
    """ Delete the reported state

    Returns a removal confirmation message.
    """
    return "State delete successfully"


### Cities ###
# List all cities.
@app.get("/cities", tags=[city_tag])
def get_cities():
    """ Search for all registered cities

    Returns a representation of the cities listing.
    """
    return "No registered cities"

# List one city.
@app.get("/city", tags=[city_tag])
def get_city():
    """ Searches for a city based on the city id

    Returns a representation of city.
    """
    return "City does not exist"

# Add new city.
@app.post("/city", tags=[city_tag])
def new_city():
    """ Add a new city to the database

    Returns a representation of city.
    """
    return "City saved successfully"

# Change city
@app.post("/update_city", tags=[city_tag])
def update_city():
    """ Altera o city selecionado

    Returns a representation of the city.
    """
    return "City changed successfully"

# Delete city
@app.delete("/city", tags=[city_tag])
def delete_city():
    """ Delete the reported city

    Returns a removal confirmation message.
    """
    return "City delete successfully"