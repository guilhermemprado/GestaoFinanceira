from typing import List
from pydantic import BaseModel


class BankSearchSchema(BaseModel):
    """Defines how the structure representing the search should be.
    What will be made only based on the bank id.
    """

    number: int = 0


def show_banks(banks: List):
    """Show representation of banks.
    Return: List of banks.
    """
    result = []
    for bank in banks:
        result.append(
            {
                "Number": bank[0],
                "Name": bank[1],
            }
        )

    return {"Banks": result} if len(result) > 1 else {"Bank": result}
