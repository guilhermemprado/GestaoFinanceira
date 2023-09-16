from typing import List
from pydantic import BaseModel


class PersonIdSearchSchema(BaseModel):
    """Defines how the structure representing the search should be.
    What will be made only based on the person id.
    """

    id: int = 0


class PersonSearchSchema(BaseModel):
    """Defines how the structure representing the search should be.
    What will be made only based on the bank.
    """

    name: str = ""
    email: str = ""
    phone_number: str = ""


def show_person(persons: List):
    """Show representation of persons.
    Return: List of persons.
    """
    result = []
    for person in persons:
        result.append(
            {
                "Id": person[0],
                "Name": person[1],
                "Email": person[2],
                "Phone": person[3],
            }
        )

    return {"Persons": result} if len(result) > 1 else {"Person": result}
