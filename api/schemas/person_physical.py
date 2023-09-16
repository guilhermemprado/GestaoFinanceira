from typing import List
from pydantic import BaseModel


class PersonPhysicalIdSearchSchema(BaseModel):
    """Defines how the structure representing the search should be.
    What will be made only based on the physical id.
    """

    id: int = 0


class PersonPhysicalSearchSchema(BaseModel):
    """Defines how the structure representing the search should be.
    What will be made only based on the physical.
    """

    person: int = 0
    cpf: int = 0


class PersonAllPhysicalSearchSchema(BaseModel):
    """Defines how the structure representing the search should be.
    What will be made only based on the bank.
    """

    person: int = 0
    cpf: int = 0


def show_person_physical(adresses: List):
    """Show representation of address.
    Return: List of address.
    """
    result = []
    for address in adresses:
        result.append(
            {
                "id": address[0],
                "Nome": address[1],
                "Cpf": address[2],
            }
        )

    return {"Person physics": result} if len(result) > 1 else {"Person physical": result}
