from typing import List
from pydantic import BaseModel


class PersonAddressIdSearchSchema(BaseModel):
    """Defines how the structure representing the search should be.
    What will be made only based on the person id.
    """

    id: int = 0


class PersonAddressSearchSchema(BaseModel):
    """Defines how the structure representing the search should be.
    What will be made only based on the bank.
    """

    person: int = 0
    city: int = 0
    # cep: str = ""
    # street: str = ""
    # number: int = 0
    district: str = ""
    # complement: str = ""


class PersonAllAddressSearchSchema(BaseModel):
    """Defines how the structure representing the search should be.
    What will be made only based on the bank.
    """

    person: int = 0
    city: int = 0
    cep: str = ""
    street: str = ""
    number: int = 0
    district: str = ""
    complement: str = ""


def show_person_address(adresses: List):
    """Show representation of address.
    Return: List of address.
    """
    result = []
    for address in adresses:
        result.append(
            {
                "id": address[0],
                "person": address[1],
                "city": address[2],
                "cep": address[3],
                "street": address[4],
                "number": address[5],
                "district": address[6],
                "complement": address[7],
            }
        )

    return {"Adresses": result} if len(result) > 1 else {"Address": result}
