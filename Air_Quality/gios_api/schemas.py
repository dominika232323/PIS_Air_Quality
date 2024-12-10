from dataclasses import dataclass

@dataclass
class Location:
    commune: str
    district: str
    voivodeship: str
    city: str
    street: str


@dataclass
class StationData:
    id: int
    name: str
    location: Location
