from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import date

@dataclass
class FlightSearchParams:
    origin: str
    max_price: Optional[float] = None
    currency: str = 'EUR'
    departure_date: Optional[date] = None

@dataclass
class FlightDestination:
    destination: str
    price: float
    departure_date: Optional[date]
    return_date: Optional[date]
    airline: Optional[str]

class FlightSearchService(ABC):
    @abstractmethod
    async def get_access_token(self) -> str:
        """Get authentication token from the service"""
        pass

    @abstractmethod
    async def search_destinations(self, params: FlightSearchParams) -> List[FlightDestination]:
        """Search for flight destinations based on parameters"""
        pass