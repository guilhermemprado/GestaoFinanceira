from typing import List
from pydantic import BaseModel


class StateSearchSchema(BaseModel):
    """Defines how the structure representing the search should be.
    What will be made only based on the uf state.
    """

    state: str = ""


def show_states(states: List):
    """Show representation of state.
    Return: List of state.
    """
    result = []
    for state in states:
        result.append(
            {
                "Number": state[0],
                "Acronym": state[1],
            }
        )

    return {"States": result} if len(result) > 1 else {"State": result}
