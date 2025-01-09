from django.core.management.base import BaseCommand
from tools.models import Countries, VisaType, VisaRelationship

class Command(BaseCommand):
    help = 'Populate visa relationships from Nigeria to specified countries one by one'

    def handle(self, *args, **kwargs):
        # Define the countries
        nigeria = Countries.objects.get(iso_code_2='NG')
        france = Countries.objects.get(iso_code_2='FR')
        mexico = Countries.objects.get(iso_code_2='MX')
        usa = Countries.objects.get(iso_code_2='US')
        uk = Countries.objects.get(iso_code_2='GB')
        ecuador = Countries.objects.get(iso_code_2='EC')
        el_salvador = Countries.objects.get(iso_code_2='SV')

        # Define visa types
        visa_types = [
            {'name': 'Tourist Visa', 'description': 'Visa for tourism purposes'},
            {'name': 'Business Visa', 'description': 'Visa for business purposes'},
            {'name': 'Student Visa', 'description': 'Visa for educational purposes'},
        ]

        # Create or update visa types
        for visa_type in visa_types:
            VisaType.objects.update_or_create(
                name=visa_type['name'],
                defaults=visa_type
            )

        # Fetch visa types from the database
        tourist_visa = VisaType.objects.get(name='Tourist Visa')
        business_visa = VisaType.objects.get(name='Business Visa')
        student_visa = VisaType.objects.get(name='Student Visa')

        # Create visa relationships one by one
        self.create_visa_relationship(nigeria, france, tourist_visa)
        self.create_visa_relationship(nigeria, mexico, business_visa)
        self.create_visa_relationship(nigeria, usa, student_visa)
        self.create_visa_relationship(nigeria, uk, tourist_visa)
        self.create_visa_relationship(nigeria, ecuador, business_visa)
        self.create_visa_relationship(nigeria, el_salvador, student_visa)

    def create_visa_relationship(self, from_country, to_country, visa_type):
        try:
            VisaRelationship.objects.update_or_create(
                citizenship_country=from_country,
                destination_country=to_country,
                visa_type=visa_type,
                defaults={
                    'max_stay_days': 90,
                    'multiple_entry': True,
                    'processing_time_days': 15,
                    'fee_amount': 100.00,
                    'fee_currency': 'USD',
                    'notes': 'Visa required for entry',
                    'documents_required': 'Passport, Visa Application, Proof of Funds',
                    'is_active': True,
                }
            )
            self.stdout.write(self.style.SUCCESS(
                f'Successfully populated visa relationship from {from_country.name} to {to_country.name} for {visa_type.name}'
            ))
        except Exception as e:
            self.stderr.write(self.style.ERROR(
                f'Error populating visa relationship from {from_country.name} to {to_country.name} for {visa_type.name}: {e}'
            ))
