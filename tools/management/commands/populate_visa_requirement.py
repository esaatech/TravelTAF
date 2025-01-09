from django.core.management.base import BaseCommand
from tools.models import Countries, VisaType, VisaRelationship

class Command(BaseCommand):
    help = 'Populate the database with sample country and visa data'

    def handle(self, *args, **kwargs):
        # Countries in North America, Nigeria, and the UK
      

       

        # Visa relationships from Nigeria to other countries
        nigeria = Countries.objects.get(iso_code_2='NG')
        usa = Countries.objects.get(iso_code_2='US')
        canada = Countries.objects.get(iso_code_2='CA')
        mexico = Countries.objects.get(iso_code_2='MX')
        uk = Countries.objects.get(iso_code_2='GB')
        tourist_visa = VisaType.objects.get(name='Tourist Visa')

        # Nigeria to USA
        VisaRelationship.objects.update_or_create(
            from_country=nigeria,
            to_country=usa,
            visa_type=tourist_visa,
            defaults={
                'max_stay_days': 90,
                'multiple_entry': False,
                'processing_time_days': 15,
                'fee_amount': 160.00,
                'fee_currency': 'USD',
                'notes': 'Visa required for entry',
                'documents_required': 'Passport, Visa Application, Proof of Funds',
                'is_active': True,
            }
        )

        # Nigeria to Canada
        VisaRelationship.objects.update_or_create(
            from_country=nigeria,
            to_country=canada,
            visa_type=tourist_visa,
            defaults={
                'max_stay_days': 180,
                'multiple_entry': True,
                'processing_time_days': 20,
                'fee_amount': 100.00,
                'fee_currency': 'CAD',
                'notes': 'Visa required for entry',
                'documents_required': 'Passport, Visa Application, Proof of Funds',
                'is_active': True,
            }
        )

        # Nigeria to Mexico
        VisaRelationship.objects.update_or_create(
            from_country=nigeria,
            to_country=mexico,
            visa_type=tourist_visa,
            defaults={
                'max_stay_days': 180,
                'multiple_entry': True,
                'processing_time_days': 10,
                'fee_amount': 36.00,
                'fee_currency': 'USD',
                'notes': 'Visa required for entry',
                'documents_required': 'Passport, Visa Application, Proof of Funds',
                'is_active': True,
            }
        )

        # Nigeria to UK
        VisaRelationship.objects.update_or_create(
            from_country=nigeria,
            to_country=uk,
            visa_type=tourist_visa,
            defaults={
                'max_stay_days': 180,
                'multiple_entry': True,
                'processing_time_days': 15,
                'fee_amount': 95.00,
                'fee_currency': 'GBP',
                'notes': 'Visa required for entry',
                'documents_required': 'Passport, Visa Application, Proof of Funds',
                'is_active': True,
            }
        )

        self.stdout.write(self.style.SUCCESS('Successfully populated visa relationships from Nigeria'))