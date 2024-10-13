from pydantic import BaseModel, Field
from typing import List, Optional

class Circuit(BaseModel):
    circuit_id: int
    name: str
    location: str
    country: str
    lat: float
    lng: float

class CircuitInfo(Circuit):
    total_races: int
    avg_round: float
    circuitRef: str
    alt: Optional[float]
    url: Optional[str]

class CircuitRace(BaseModel):
    race_id: int
    year: int
    round: int
    name: str
    date: str
    winner_surname: str
    constructor_name: str
    winning_time: Optional[str]

class CircuitRaceResponse(BaseModel):
    circuit_races: List[CircuitRace]


class CircuitResponse(BaseModel):
    data: List[Circuit]
    page: int
    page_size: int
    total_items: int
    total_pages: int

class CircuitInfoResponse(BaseModel):
    circuit_info: CircuitInfo
    races: List[CircuitRace]