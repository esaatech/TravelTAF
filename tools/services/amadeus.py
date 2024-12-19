import aiohttp
from datetime import datetime
from typing import List
from .flight_interfaces import FlightSearchService, FlightSearchParams, FlightDestination

class AmadeusFlightService(FlightSearchService):
    def __init__(self):
        self.client_id = 'ldVOG4IqYVNgHM2fLkH5dvqxQbs7LtOV'
        self.client_secret = 'EMTXJAqssGmfvOK7'
        self.token = None
        self.token_expires = None
        self.base_url = 'https://test.api.amadeus.com/v1'

    async def get_access_token(self) -> str:
        """Get or refresh Amadeus API token"""
        if self.token and self.token_expires and datetime.now() < self.token_expires:
            return self.token

        async with aiohttp.ClientSession() as session:
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            
            async with session.post(
                f'{self.base_url}/security/oauth2/token',
                data=data,
                headers=headers
            ) as response:
                result = await response.json()
                self.token = result['access_token']
                self.token_expires = datetime.now().timestamp() + result['expires_in']
                return self.token

    async def search_destinations(self, params: FlightSearchParams) -> List[FlightDestination]:
        """Search flight destinations using Amadeus API"""
        token = await self.get_access_token()
        
        query_params = {
            'origin': params.origin,
            'maxPrice': params.max_price if params.max_price else None
        }
        # Remove None values
        query_params = {k: v for k, v in query_params.items() if v is not None}
        
        headers = {'Authorization': f'Bearer {token}'}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{self.base_url}/shopping/flight-destinations',
                params=query_params,
                headers=headers
            ) as response:
                data = await response.json()
                
                results = []
                for item in data.get('data', []):
                    results.append(FlightDestination(
                        destination=item['destination'],
                        price=float(item['price']['total']),
                        departure_date=datetime.strptime(item['departureDate'], '%Y-%m-%d').date() if 'departureDate' in item else None,
                        return_date=datetime.strptime(item['returnDate'], '%Y-%m-%d').date() if 'returnDate' in item else None,
                        airline=item.get('airline')
                    ))
                return results