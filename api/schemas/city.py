from typing import List
from pydantic import BaseModel


class CitySearchSchema(BaseModel):
    """Defines how the structure representing the search should be.
    What will be made only based on the city id.
    """

    name: str = ""
    uf: str = ""


def show_cities(cities: List):
    """Show representation of cities.
    Return: List of cities.
    """
    result = []
    for city in cities:
        result.append(
            {
                "Number": city[0],
                "Name": city[1],
                "Acronym": city[2],
            }
        )

    return {"Cities": result} if len(result) > 1 else {"City": result}
