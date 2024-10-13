from pydantic import BaseModel, Field
from typing import List, Optional

class Race(BaseModel):
    race_id: int
    year: int
    round: int
    name: str
    date: str

class RaceDetails(Race):
    circuit_name: str
    location: str
    country: str

class RaceResult(BaseModel):
    position: Optional[int]
    driver_name: str
    constructor_name: str
    status: str
    points: float
    fastest_lap_time: Optional[str]
    fastest_lap_speed: Optional[float]

class FastestLap(BaseModel):
    position: int
    driver_name: str
    fastest_lap_time: str
    fastest_lap_speed: Optional[float]

class RaceResponse(BaseModel):
    data: List[Race]
    page: int
    page_size: int
    total_items: int
    total_pages: int

class RaceDetailsResponse(BaseModel):
    race_details: RaceDetails
    results: List[RaceResult]
    fastest_laps: List[FastestLap]

class RaceResultsResponse(BaseModel):
    race_results: List[RaceResult]

class FastestLapsResponse(BaseModel):
    fastest_laps: List[FastestLap]