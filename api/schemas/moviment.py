from typing import List
from pydantic import BaseModel


class MovimentIdSearchSchema(BaseModel):
    """Defines how the structure representing the search should be.
    What will be made only based on the physical id.
    """

    id: int = 0


class MovimentSearchSchema(BaseModel):
    """Defines how the structure representing the search should be.
    What will be made only based on the physical.
    """

    account_number: int = 0
    description: str = ""
    date: str = ""


class MovimentAllSearchSchema(BaseModel):
    """Defines how the structure representing the search should be.
    What will be made only based on the bank.
    """

    account_number: int = 0
    description: str = ""
    value: float = 0
    date: str = ""


def show_moviments(moviments: List):
    """Show representation of address.
    Return: List of address.
    """
    result = []
    for moviment in moviments:
        result.append(
            {
                "Account number": moviment[0],
                "Description": moviment[1],
                "Date": moviment[2],
            }
        )

    return {"Moviments": result} if len(result) > 1 else {"Moviment": result}
