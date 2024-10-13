from pydantic import BaseModel, Field
from typing import List, Optional

class ConstructorStanding(BaseModel):
    position: int
    points: float
    wins: int
    constructor_name: str
    year: int

class ConstructorResult(BaseModel):
    position: Optional[int]
    points: Optional[float]
    status: str
    year: int
    race_name: str
    driver_surname: str

class ConstructorStandingsResponse(BaseModel):
    data: List[ConstructorStanding]
    page: int
    page_size: int
    total_items: int
    total_pages: int

class ConstructorResultsResponse(BaseModel):
    constructor_results: List[ConstructorResult]