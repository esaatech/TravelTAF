from django.core.management.base import BaseCommand
from tools.models import School, ProgramLevel, FieldOfStudy, Country

class Command(BaseCommand):
    help = 'Populates the database with sample school data'

    def handle(self, *args, **kwargs):
        # Create Countries
        countries_data = [
            {'name': 'United States', 'code': 'usa'},
            {'name': 'United Kingdom', 'code': 'uk'},
            {'name': 'Canada', 'code': 'canada'},
            {'name': 'Germany', 'code': 'germany'},
            {'name': 'Norway', 'code': 'norway'},
        ]
        
        for country_data in countries_data:
            Country.objects.get_or_create(
                code=country_data['code'],
                defaults={'name': country_data['name']}
            )

        # Create Program Levels
        program_levels = {
            'Undergraduate': 'undergraduate',
            'Graduate': 'graduate',
            'Masters': 'masters',
            'PhD': 'phd'
        }
        
        created_programs = {}
        for name, value in program_levels.items():
            program, _ = ProgramLevel.objects.get_or_create(
                name=name, 
                value=value
            )
            created_programs[name] = program

        # Create Fields of Study
        fields_of_study = {
            'Business': 'business',
            'Engineering': 'engineering',
            'Computer Science': 'computer_science',
            'Medicine': 'medicine',
            'Law': 'law',
            'Arts': 'arts',
            'Sciences': 'sciences',
            'Mathematics': 'mathematics'
        }
        
        created_fields = {}
        for name, value in fields_of_study.items():
            field, _ = FieldOfStudy.objects.get_or_create(
                name=name,
                value=value
            )
            created_fields[name] = field

        # Sample Schools Data
        schools_data = [
            {
                'name': 'Harvard University',
                'location': 'Cambridge, Massachusetts',
                'country': 'usa',
                'website': 'https://www.harvard.edu',
                'ranking': '#2 National Universities (US News 2024)',
                'tuition': 57261.00,  # 2023-24 tuition
                'scholarships_available': True,
                'work_opportunities': True,
                'housing_available': True,
                'programs': ['Undergraduate', 'Graduate', 'Masters', 'PhD'],
                'fields': ['Business', 'Law', 'Medicine', 'Arts', 'Sciences']
            },
            {
                'name': 'Stanford University',
                'location': 'Stanford, California',
                'country': 'usa',
                'website': 'https://www.stanford.edu',
                'ranking': '#3 National Universities (US News 2024)',
                'tuition': 56169.00,  # 2023-24 tuition
                'scholarships_available': True,
                'work_opportunities': True,
                'housing_available': True,
                'programs': ['Undergraduate', 'Graduate', 'Masters', 'PhD'],
                'fields': ['Engineering', 'Computer Science', 'Business', 'Medicine']
            },
            {
                'name': 'University of Oxford',
                'location': 'Oxford, England',
                'country': 'uk',
                'website': 'https://www.ox.ac.uk',
                'ranking': '#1 World University Rankings 2024',
                'tuition': 39000.00,  # International student fees
                'scholarships_available': True,
                'work_opportunities': True,
                'housing_available': True,
                'programs': ['Undergraduate', 'Graduate', 'Masters', 'PhD'],
                'fields': ['Arts', 'Sciences', 'Medicine', 'Law']
            },
            {
                'name': 'University of Toronto',
                'location': 'Toronto, Ontario',
                'country': 'canada',
                'website': 'https://www.utoronto.ca',
                'ranking': '#1 in Canada',
                'tuition': 45900.00,  # International student fees
                'scholarships_available': True,
                'work_opportunities': True,
                'housing_available': True,
                'programs': ['Undergraduate', 'Graduate', 'Masters', 'PhD'],
                'fields': ['Business', 'Engineering', 'Medicine', 'Arts']
            },
            {
                'name': 'MIT',
                'location': 'Cambridge, Massachusetts',
                'country': 'usa',
                'website': 'https://www.mit.edu',
                'ranking': '#1 National Universities (US News 2024)',
                'tuition': 57986.00,  # 2023-24 tuition
                'scholarships_available': True,
                'work_opportunities': True,
                'housing_available': True,
                'programs': ['Undergraduate', 'Graduate', 'Masters', 'PhD'],
                'fields': ['Engineering', 'Computer Science', 'Sciences']
            },
            {
                'name': 'University of Cambridge',
                'location': 'Cambridge, England',
                'country': 'uk',
                'website': 'https://www.cam.ac.uk',
                'ranking': '#2 in UK, #3 World University Rankings 2024',
                'tuition': 35000.00,  # International student fees
                'scholarships_available': True,
                'work_opportunities': True,
                'housing_available': True,
                'programs': ['Undergraduate', 'Graduate', 'Masters', 'PhD'],
                'fields': ['Sciences', 'Engineering', 'Medicine', 'Arts']
            },
            {
                'name': 'Imperial College London',
                'location': 'London, England',
                'country': 'uk',
                'website': 'https://www.imperial.ac.uk',
                'ranking': '#3 in UK',
                'tuition': 38000.00,
                'scholarships_available': True,
                'work_opportunities': True,
                'housing_available': True,
                'programs': ['Undergraduate', 'Graduate', 'PhD'],
                'fields': ['Engineering', 'Medicine', 'Sciences']
            },
            {
                'name': 'University of Edinburgh',
                'location': 'Edinburgh, Scotland',
                'country': 'uk',
                'website': 'https://www.ed.ac.uk',
                'ranking': '#4 in UK',
                'tuition': 32000.00,
                'scholarships_available': True,
                'work_opportunities': True,
                'housing_available': True,
                'programs': ['Undergraduate', 'Graduate', 'Masters', 'PhD'],
                'fields': ['Arts', 'Sciences', 'Medicine', 'Engineering']
            },
            {
                'name': 'McGill University',
                'location': 'Montreal, Quebec',
                'country': 'canada',
                'website': 'https://www.mcgill.ca',
                'ranking': '#2 in Canada',
                'tuition': 41000.00,
                'scholarships_available': True,
                'work_opportunities': True,
                'housing_available': True,
                'programs': ['Undergraduate', 'Graduate', 'Masters', 'PhD'],
                'fields': ['Medicine', 'Engineering', 'Business', 'Arts']
            },
            {
                'name': 'University of British Columbia',
                'location': 'Vancouver, British Columbia',
                'country': 'canada',
                'website': 'https://www.ubc.ca',
                'ranking': '#3 in Canada',
                'tuition': 43000.00,
                'scholarships_available': True,
                'work_opportunities': True,
                'housing_available': True,
                'programs': ['Undergraduate', 'Graduate', 'Masters', 'PhD'],
                'fields': ['Sciences', 'Engineering', 'Business', 'Arts']
            },
            {
                'name': 'University of Waterloo',
                'location': 'Waterloo, Ontario',
                'country': 'canada',
                'website': 'https://uwaterloo.ca',
                'ranking': '#4 in Canada',
                'tuition': 40000.00,
                'scholarships_available': True,
                'work_opportunities': True,
                'housing_available': True,
                'programs': ['Undergraduate', 'Graduate', 'PhD'],
                'fields': ['Engineering', 'Computer Science', 'Mathematics']
            },
            {
                'name': 'University of Bergen',
                'location': 'Bergen, Norway',
                'country': 'norway',
                'website': 'https://www.uib.no/en',
                'ranking': 'Top 200 Globally',
                'tuition': 0.00,  # Free education for all students
                'scholarships_available': True,
                'work_opportunities': True,
                'housing_available': True,
                'programs': ['Undergraduate', 'Graduate', 'Masters', 'PhD'],
                'fields': ['Sciences', 'Medicine', 'Arts', 'Engineering']
            },
            {
                'name': 'Technical University of Munich',
                'location': 'Munich, Germany',
                'country': 'germany',
                'website': 'https://www.tum.de/en',
                'ranking': '#50 World University Rankings 2024',
                'tuition': 0.00,  # Only semester fees around 150 EUR
                'scholarships_available': True,
                'work_opportunities': True,
                'housing_available': True,
                'programs': ['Undergraduate', 'Graduate', 'Masters', 'PhD'],
                'fields': ['Engineering', 'Computer Science', 'Sciences']
            },
            {
                'name': 'Northeastern University',
                'location': 'Boston, Massachusetts',
                'country': 'usa',
                'website': 'https://www.northeastern.edu',
                'ranking': 'Top 50 National Universities',
                'tuition': 58000.00,
                'scholarships_available': True,
                'work_opportunities': True,  # Famous for co-op program
                'housing_available': True,
                'programs': ['Undergraduate', 'Graduate', 'PhD'],
                'fields': ['Business', 'Engineering', 'Computer Science', 'Arts']
            },
            {
                'name': 'University of Waterloo',
                'location': 'Waterloo, Ontario',
                'country': 'canada',
                'website': 'https://uwaterloo.ca',
                'ranking': 'Top Canadian University for Co-op',
                'tuition': 40000.00,
                'scholarships_available': True,
                'work_opportunities': True,  # Largest co-op program in the world
                'housing_available': True,
                'programs': ['Undergraduate', 'Graduate', 'PhD'],
                'fields': ['Engineering', 'Computer Science', 'Mathematics']
            },
            {
                'name': 'Curtis Institute of Music',
                'location': 'Philadelphia, Pennsylvania',
                'country': 'usa',
                'website': 'https://www.curtis.edu',
                'ranking': 'Top Music Conservatory',
                'tuition': 0.00,  # All students receive full-tuition scholarships
                'scholarships_available': True,
                'work_opportunities': True,
                'housing_available': True,
                'programs': ['Undergraduate', 'Graduate'],
                'fields': ['Arts']
            },
            {
                'name': 'Webb Institute',
                'location': 'Glen Cove, New York',
                'country': 'usa',
                'website': 'https://www.webb.edu',
                'ranking': 'Top Engineering Institution',
                'tuition': 0.00,  # Full-tuition scholarship for all US students
                'scholarships_available': True,
                'work_opportunities': True,
                'housing_available': True,
                'programs': ['Undergraduate'],
                'fields': ['Engineering']
            }
        ]

        for school_data in schools_data:
            try:
                # Get country
                country = Country.objects.get(code=school_data['country'])
                
                # Get or create the school
                school, created = School.objects.get_or_create(
                    name=school_data['name'],
                    defaults={
                        'location': school_data['location'],
                        'country': country,
                        'website': school_data['website'],
                        'ranking': school_data['ranking'],
                        'tuition': school_data['tuition'],
                        'scholarships_available': school_data['scholarships_available'],
                        'work_opportunities': school_data['work_opportunities'],
                        'housing_available': school_data['housing_available'],
                    }
                )

                # Add programs
                for program_name in school_data['programs']:
                    if program_name in created_programs:
                        school.programs.add(created_programs[program_name])

                # Add fields of study
                for field_name in school_data['fields']:
                    if field_name in created_fields:
                        school.fields_of_study.add(created_fields[field_name])

                status = 'Created' if created else 'Updated'
                self.stdout.write(
                    self.style.SUCCESS(
                        f'{status} school: {school.name} ({school.country.name})'
                    )
                )
            
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error processing {school_data["name"]}: {str(e)}'
                    )
                )