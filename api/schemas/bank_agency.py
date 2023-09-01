from typing import List
from pydantic import BaseModel


class BankAgencySearchSchema(BaseModel):
    """Defines how the structure representing the search should be.
    What will be made only based on the bank id.
    """

    number_agency: int = 0
    name_person: str = ""
    name_agency: str = ""


def show_bank_agency(banks_agencies: List):
    """Show representation of banks agencies.
    Return: List of banks agencies.
    """
    result = []
    for bank_agency in banks_agencies:
        result.append(
            {
                "Number agency": bank_agency[0],
                "Name agency": bank_agency[1],
                "Name bank": bank_agency[2],
            }
        )

    return {"Banks agencies": result} if len(result) > 1 else {"Bank agency": result}
