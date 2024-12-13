from pydantic import BaseModel


class Location(BaseModel):
    latitude: float
    longitude: float
    altitude: float
    timestamp: str


class Address(BaseModel):
    country: str
    administrative_area: str
    locality: str
    street_name: str
    street_address: str
    map_item_full_address: str
