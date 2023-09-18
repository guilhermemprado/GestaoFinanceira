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
                "Id_moviment": moviment[0],
                "Id_person": moviment[1],
                "Name_person": moviment[2],
                "Id_bank": moviment[3],
                "Name_bank": moviment[4],
                "Name_agency": moviment[5],
                "Account_number": moviment[6],
                "Description": moviment[7],
                "Value": moviment[8],
                "Date": moviment[9],
            }
        )

    return {"Moviments": result} if len(result) > 1 else {"Moviment": result}
