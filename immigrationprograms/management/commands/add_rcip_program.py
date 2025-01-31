from django.core.management.base import BaseCommand
from immigrationprograms.models import ImmigrationProgram
from tools.models import Countries
from django.utils import timezone
from datetime import date

class Command(BaseCommand):
    help = 'Adds the Rural Community Immigration Pilot (RCIP) program for Canada'

    def handle(self, *args, **kwargs):
        try:
            # Get Canada from Countries model
            canada = Countries.objects.get(iso_code_2='CA')

            # Program content
            program_data = {
                'name': 'Rural Community Immigration Pilot (RCIP)',
                'description': """
                The Rural Community Immigration Pilot (RCIP) is a new initiative by the Government of Canada 
                that ensures rural communities have access to programs that address labour shortages and help 
                local businesses find the workers they need. This pilot provides a permanent residence pathway 
                to attract and retain newcomers who can fill key jobs in rural communities.
                """,
                'eligibility_criteria': """
                • Must have a job offer from a designated employer in one of the participating communities:
                  - Pictou County, NS
                  - North Bay, ON
                  - Sudbury, ON
                  - Timmins, ON
                  - Sault Ste. Marie, ON
                  - Thunder Bay, ON
                  - Steinbach, MB
                  - Altona/Rhineland, MB
                  - Brandon, MB
                  - Moose Jaw, SK
                  - Claresholm, AB
                  - West Kootenay, BC
                  - North Okanagan Shuswap, BC
                  - Peace Liard, BC
                
                • Must meet language requirements
                • Must have relevant work experience
                • Must have sufficient settlement funds
                • Must intend to live in the community long-term
                """,
                'benefits': """
                • Permanent residence pathway
                • Support from local economic development organizations
                • Access to job opportunities in rural communities
                • Community integration support
                • Opportunity to contribute to rural economic development
                • High retention rate (87% of participants stay in their communities)
                """,
                'application_process': """
                1. Choose a participating community from the list
                2. Find a designated employer in that community
                3. Get a job offer
                4. Work with the local economic development organization
                5. Get community recommendation
                6. Apply for permanent residence through IRCC
                
                Note: Each community will provide specific details and timelines for when employers and 
                prospective permanent residence candidates can expect to have a chance to apply.
                """,
                'country': canada,
                'status': 'APPROVED',
                'featured': True,
                'deadline': date(2025, 12, 31),
                'official_link': 'https://www.canada.ca/en/immigration-refugees-citizenship/news/2025/01/canada-launches-rural-and-francophone-community-immigration-pilots.html',
                'chat_enabled': True
            }

            # Create or update the program
            program, created = ImmigrationProgram.objects.update_or_create(
                name=program_data['name'],
                defaults=program_data
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created RCIP program')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully updated RCIP program')
                )

        except Countries.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Canada not found in Countries table')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            ) 