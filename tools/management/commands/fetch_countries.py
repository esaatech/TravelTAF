import requests
from django.core.management.base import BaseCommand
from tools.models import Countries

class Command(BaseCommand):
    help = 'Fetch and populate country data from an external API'

    def handle(self, *args, **kwargs):
        # URL for the REST Countries API
        api_url = 'https://restcountries.com/v3.1/all'

        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an error for bad responses
            countries_data = response.json()

            for country in countries_data:
                name = country.get('name', {}).get('common', '')
                iso_code_2 = country.get('cca2', '')
                iso_code_3 = country.get('cca3', '')
                region = country.get('region', '')
                continent = country.get('continents', [None])[0]

                # Update or create the country record
                Countries.objects.update_or_create(
                    iso_code_2=iso_code_2,
                    defaults={
                        'name': name,
                        'iso_code_3': iso_code_3,
                        'region': region,
                        'continent': continent,
                    }
                )

            self.stdout.write(self.style.SUCCESS('Successfully fetched and populated country data'))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Error fetching data: {e}')) 