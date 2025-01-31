from django.core.management.base import BaseCommand
from immigrationprograms.models import ImmigrationProgram
from tools.models import Countries
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Adds the REDI (Rural and Northern Immigration Pilot) program for Canada'

    def handle(self, *args, **kwargs):
        try:
            # Get Canada from Countries model
            canada = Countries.objects.get(iso_code_2='CA')

            # Program content
            program_data = {
                'name': 'Rural and Northern Immigration Pilot (REDI)',
                'description': """
                The Rural and Northern Immigration Pilot (RNIP) is a community-driven program that helps smaller 
                communities benefit from the economic immigration of skilled workers to meet their labor market needs.
                """,
                'eligibility_criteria': """
                • Work experience
                • Language ability (CLB/NCLC 6)
                • Educational credentials
                • Settlement funds
                • Intent to live in the community
                • Job offer from a local employer
                """,
                'benefits': """
                • Pathway to permanent residence
                • Work in smaller communities
                • Community support
                • Faster processing
                • Family inclusion
                """,
                'application_process': """
                1. Check your eligibility
                2. Get a job offer from a designated employer
                3. Submit application to the community
                4. Get community recommendation
                5. Apply for permanent residence
                """,
                'country': canada,
                'status': 'APPROVED',
                'featured': True,
                'official_link': 'https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/rural-northern-immigration-pilot.html'
            }

            # Create or update the program
            program, created = ImmigrationProgram.objects.update_or_create(
                name=program_data['name'],
                defaults=program_data
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created REDI program')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully updated REDI program')
                )

        except Countries.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Canada not found in Countries table')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            ) 