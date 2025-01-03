import aiohttp
from datetime import datetime
from typing import List
from .flight_interfaces import FlightSearchService, FlightSearchParams, FlightDestination
import os
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

class AmadeusFlightService(FlightSearchService):
    def __init__(self):
        # Get credentials from environment variables or settings
        self.client_id = os.getenv('AMADEUS_CLIENT_ID')
       
        self.client_secret = os.getenv('AMADEUS_CLIENT_SECRET')
      
        
        if not self.client_id or not self.client_secret:
            raise ValueError("Amadeus API credentials not configured")
            
        self.token = None
        self.token_expires = None
        self.base_url = 'https://test.api.amadeus.com/v1'

    async def get_access_token(self) -> str:
        """Get or refresh Amadeus API token"""
        try:
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
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Failed to get access token. Status: {response.status}, Response: {error_text}")
                        
                    result = await response.json()
                    if 'access_token' not in result:
                        raise Exception(f"Invalid token response: {result}")
                        
                    self.token = result['access_token']
                    return self.token
                    
        except Exception as e:
            raise Exception(f"Authentication failed: {str(e)}")

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