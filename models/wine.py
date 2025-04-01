from pydantic import BaseModel
from decimal import Decimal


class Wine(BaseModel):
    """
    Represents the data structure of a Wine.
    """
    name: str
    year: int
    region: str
    type: str
    price: int
    abv: Decimal
    ph: Decimal
    ta: Decimal
    rs: Decimal
    aging_notes: str
    # winery: str


class Winery(BaseModel):
    """
    Represents the data structure of a Winery.
    """
    name: str
    region: str
    website: str
    contact: str
    established: str
    # wines: list[Wine]
    # description: str


