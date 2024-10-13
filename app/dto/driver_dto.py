from pydantic import BaseModel, Field
from typing import List, Optional

class Driver(BaseModel):
    driver_id: int
    code: Optional[str]
    forename: str
    surname: str
    dob: str
    nationality: str

class DriverDetails(BaseModel):
    driverId: int
    driverRef: str
    number: Optional[str]
    code: Optional[str]
    forename: str
    surname: str
    dob: str
    nationality: str
    url: str
    total_races: int
    total_points: float
    wins: int

class DriverStanding(BaseModel):
    position: int
    points: float
    wins: int
    year: int
    race_name: str

class DriverResponse(BaseModel):
    data: List[Driver]
    page: int
    page_size: int
    total_items: int
    total_pages: int

class DriverDetailsResponse(BaseModel):
    driver_details: DriverDetails

class DriverStandingsResponse(BaseModel):
    driver_standings: List[DriverStanding]