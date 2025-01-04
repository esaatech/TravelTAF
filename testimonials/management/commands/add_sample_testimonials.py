from django.core.management.base import BaseCommand
from testimonials.models import Testimonial

class Command(BaseCommand):
    help = 'Adds sample testimonials to the database'

    def handle(self, *args, **kwargs):
        testimonials_data = [
            {
                'name': 'Nicholas ',
                'initials': 'NC',
                'location': 'Relocated to Canada',
                'rating': 5,
                'testimonial_text': "TravelTAF made my dream of moving to Canada a reality. Their expertise in Express Entry was invaluable, and they guided me through every step with precision.",
                'testimonial_type': 'Express Entry PR',
                'duration': '6 months'
            },
            {
                'name': 'Elvis ',
                'initials': 'EO',
                'location': 'Studying in UK',
                'rating': 5,
                'testimonial_text': "Outstanding support throughout my UK student visa application. They helped me secure admission to my dream university and handled the visa process flawlessly.",
                'testimonial_type': 'Student Visa',
                'duration': '3 months'
            },
            {
                'name': 'Esther ',
                'initials': 'EK',
                'location': 'Working in Australia',
                'rating': 5,
                'testimonial_text': "The team's knowledge of Australian skilled migration was exceptional. They helped me navigate the points system and secure my skilled visa successfully.",
                'testimonial_type': 'Skilled Migration',
                'duration': '5 months'
            },
            {
                'name': 'Henry ',
                'initials': 'HM',
                'location': 'Relocated to Mexico',
                'rating': 5,
                'testimonial_text': "Professional service from start to finish. Their expertise made the complex New Zealand immigration process feel straightforward and manageable.",
                'testimonial_type': 'Skilled Migration',
                'duration': '4 months'
            },
            {
                'name': 'Sarah ',
                'initials': 'SW',
                'location': 'Studying in Canada',
                'rating': 5,
                'testimonial_text': "TravelTAF's university placement service was fantastic. They helped me get into a top Canadian university and sorted out my study permit quickly.",
                'testimonial_type': 'Study Permit',
                'duration': '2 months'
            },
            {
                'name': 'David ',
                'initials': 'DP',
                'location': 'Working in UK',
                'rating': 5,
                'testimonial_text': "Their guidance through the UK Skilled Worker visa process was excellent. They handled everything professionally and kept me informed at every stage.",
                'testimonial_type': 'Work Visa',
                'duration': '3 months'
            }
        ]

        for data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                name=data['name'],
                defaults={
                    'initials': data['initials'],
                    'location': data['location'],
                    'rating': data['rating'],
                    'testimonial_text': data['testimonial_text'],
                    'testimonial_type': data['testimonial_type'],
                    'duration': data['duration']
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created testimonial for {data["name"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Testimonial for {data["name"]} already exists')
                ) 