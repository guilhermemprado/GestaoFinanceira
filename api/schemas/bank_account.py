from typing import List
from pydantic import BaseModel


class BankAccountIdSearchSchema(BaseModel):
    """Defines how the structure representing the search should be.
    What will be made only based on the bank id.
    """

    id: int = 0


class BankAccountSearchSchema(BaseModel):
    """Defines how the structure representing the search should be.
    What will be made only based on the bank.
    """

    id_person: int = 0
    account_number: int = 0
    agency_number: int = 0


def show_bank_account(banks_accounts: List):
    """Show representation of banks accounts.
    Return: List of banks accounts.
    """
    result = []
    for bank_account in banks_accounts:
        result.append(
            {
                "Id": bank_account[0],
                "Account": bank_account[1],
                "Person": bank_account[2],
                "Name_person": bank_account[3],
                "Agency_number": bank_account[4],
            }
        )

    return {"Banks accounts": result} if len(result) > 1 else {"Bank accont": result}
