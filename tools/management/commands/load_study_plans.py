from django.core.management.base import BaseCommand
from tools.models import StudyServicePlan, StudyPlanFeature, StudyPlanService

class Command(BaseCommand):
    help = 'Loads initial study service plans data'

    def handle(self, *args, **kwargs):
        # Program Support Plan
        program_plan = StudyServicePlan.objects.create(
            name='Program Application Support',
            plan_type='program_support',
            description='Complete support for applying to your chosen program',
            price=199.00,
            timeline='4-6 weeks',
            button_text='Start Application',
            button_url='tools:start_program_application',
            order=1
        )

        # Program Support Features
        features = [
            'Document preparation assistance',
            'Personal Statement/SOP writing',
            'Application form filling guidance',
            'Document review & verification',
            'Application submission support',
            'Interview preparation (if required)',
            'Admission status tracking',
            'Email templates for communication',
        ]
        
        for index, feature in enumerate(features, 1):
            StudyPlanFeature.objects.create(
                plan=program_plan,
                feature=feature,
                order=index
            )

        # Program Support Services
        services = [
            'One program application',
            '3 rounds of document review',
            '2 SOP/Essay revisions',
            '1 mock interview session',
        ]

        for index, service in enumerate(services, 1):
            StudyPlanService.objects.create(
                plan=program_plan,
                service=service,
                order=index
            )

        # Study Abroad Plan
        abroad_plan = StudyServicePlan.objects.create(
            name='Complete Study Abroad Service',
            plan_type='study_abroad',
            description='End-to-end support for your entire study abroad journey',
            price=999.00,
            timeline='3-6 months',
            button_text='Get Complete Support',
            button_url='tools:start_abroad_service',
            order=2
        )

        # Study Abroad Features
        features = [
            'All Program Application Support features',
            'Multiple program applications',
            'Visa application assistance',
            'Pre-departure guidance',
            'Accommodation search support',
            'Bank account setup assistance',
            'Travel insurance guidance',
            'Airport pickup arrangement',
        ]

        for index, feature in enumerate(features, 1):
            StudyPlanFeature.objects.create(
                plan=abroad_plan,
                feature=feature,
                order=index
            )

        # Study Abroad Services
        services = [
            'Up to 3 program applications',
            'Unlimited document reviews',
            'Complete visa application support',
            'Accommodation shortlisting',
            '24/7 support until arrival',
            '3-month post-arrival support',
        ]

        for index, service in enumerate(services, 1):
            StudyPlanService.objects.create(
                plan=abroad_plan,
                service=service,
                order=index
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded study service plans')) 