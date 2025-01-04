from django.core.management.base import BaseCommand
from faqs.models import Category, FAQ

class Command(BaseCommand):
    help = 'Adds sample FAQs for travel, tourism, and immigration'

    def handle(self, *args, **kwargs):
        # Create Categories
        categories_data = [
            {
                'name': 'Immigration & Visas',
                'icon': 'fas fa-passport',
                'faqs': [
                    {
                        'question': 'What are the main pathways for immigrating to Canada?',
                        'answer': 'The main pathways include:\n\n'
                                '• Express Entry (Federal Skilled Worker, Canadian Experience Class, Federal Skilled Trades)\n'
                                '• Provincial Nominee Program (PNP)\n'
                                '• Study Permit followed by Post-Graduate Work Permit\n'
                                '• Family Sponsorship\n'
                                '• Start-up Visa Program\n\n'
                                'Each pathway has specific eligibility requirements and processing times.'
                    },
                    {
                        'question': 'How long does it take to process a UK Student Visa?',
                        'answer': 'UK Student Visa (Tier 4) processing typically takes 15 working days for standard applications. Priority service can reduce this to 5 working days. You can apply up to 6 months before your course starts. Remember to factor in time for gathering documents and attending biometrics appointments.'
                    },
                    {
                        'question': 'What is the minimum score required for IELTS?',
                        'answer': 'Required IELTS scores vary by program and country:\n\n'
                                '• Canada Express Entry: CLB 7 (typically 6.0-7.0)\n'
                                '• UK Student Visa: Usually 5.5-6.5\n'
                                '• USA Student Visa: Typically 6.0-7.0\n'
                                '• Australia Skilled Migration: At least 6.0 in each band\n\n'
                                'Some programs may require higher scores.'
                    }
                ]
            },
            {
                'name': 'Travel & Tourism',
                'icon': 'fas fa-plane-departure',
                'faqs': [
                    {
                        'question': 'What is the best time to visit Mexico?',
                        'answer': 'The best time to visit Mexico is during the dry season (December to April). The weather is pleasant with less rainfall. However, different regions have varying climates:\n\n'
                                '• Beach Destinations: November to April\n'
                                '• Mexico City: March to May\n'
                                '• Cancun: December to April\n\n'
                                'Peak tourist season is during winter months and prices may be higher.'
                    },
                    {
                        'question': 'Do I need a visa to visit the USA for tourism?',
                        'answer': 'Visa requirements depend on your nationality. Many countries participate in the Visa Waiver Program (ESTA) allowing visits up to 90 days. If your country isn\'t eligible for ESTA, you\'ll need to apply for a B1/B2 visitor visa. Processing times vary by location.'
                    },
                    {
                        'question': 'What travel insurance is recommended for international trips?',
                        'answer': 'We recommend comprehensive travel insurance that covers:\n\n'
                                '• Medical emergencies and evacuation\n'
                                '• Trip cancellation/interruption\n'
                                '• Lost/delayed baggage\n'
                                '• Flight delays\n'
                                '• COVID-19 related issues\n\n'
                                'Coverage amounts should be adequate for your destination.'
                    }
                ]
            },
            {
                'name': 'Study Abroad',
                'icon': 'fas fa-graduation-cap',
                'faqs': [
                    {
                        'question': 'What are the costs of studying in Canada?',
                        'answer': 'Costs for international students in Canada include:\n\n'
                                '• Tuition: CAD 20,000-30,000/year\n'
                                '• Living expenses: CAD 15,000-20,000/year\n'
                                '• Health insurance: CAD 600-800/year\n'
                                '• Books and supplies: CAD 1,000-2,000/year\n\n'
                                'Costs vary by location and program.'
                    },
                    {
                        'question': 'Can I work while studying in the UK?',
                        'answer': 'Yes, international students can typically work up to 20 hours per week during term time and full-time during holidays. However, work restrictions vary based on your course type and level. Always check your visa conditions.'
                    },
                    {
                        'question': 'What are the post-study work options in the USA?',
                        'answer': 'After completing studies in the USA:\n\n'
                                '• OPT (Optional Practical Training): 12 months\n'
                                '• STEM OPT Extension: Additional 24 months\n'
                                '• H-1B Visa application\n'
                                '• Other work visa options based on qualifications'
                    }
                ]
            },
            {
                'name': 'Tours & Packages',
                'icon': 'fas fa-map-marked-alt',
                'faqs': [
                    {
                        'question': 'What types of tour packages do you offer?',
                        'answer': 'We offer various tour packages including:\n\n'
                                '• City exploration tours\n'
                                '• Cultural heritage tours\n'
                                '• Adventure tourism packages\n'
                                '• Educational tours\n'
                                '• Customized group tours\n'
                                '• Luxury travel experiences\n\n'
                                'All packages can be customized to your preferences.'
                    },
                    {
                        'question': 'How far in advance should I book a tour?',
                        'answer': 'Booking recommendations:\n\n'
                                '• Peak season tours: 6-12 months ahead\n'
                                '• Regular season: 3-6 months ahead\n'
                                '• Custom tours: At least 2-3 months\n'
                                '• Last-minute bookings possible but subject to availability'
                    },
                    {
                        'question': 'Are meals included in tour packages?',
                        'answer': 'Meal inclusions vary by package type:\n\n'
                                '• Standard tours: Usually breakfast only\n'
                                '• Premium tours: Most meals included\n'
                                '• Luxury packages: All meals with special dining experiences\n\n'
                                'Specific inclusions are listed in each tour itinerary.'
                    }
                ]
            }
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'icon': cat_data['icon']
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            
            for index, faq_data in enumerate(cat_data['faqs']):
                faq, created = FAQ.objects.get_or_create(
                    category=category,
                    question=faq_data['question'],
                    defaults={
                        'answer': faq_data['answer'],
                        'order': index
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created FAQ: {faq.question}')
                    )

        self.stdout.write(self.style.SUCCESS('Successfully added sample FAQs')) 