from django.core.management.base import BaseCommand
from django.utils import timezone
from news.models import News, NewsCategory

class Command(BaseCommand):
    help = 'Creates sample news articles'

    def handle(self, *args, **kwargs):
        # Create categories first
        categories_data = [
            {
                'name': 'Canada',
                'slug': 'can',
                'description': 'News about Canadian immigration'
            },
            {
                'name': 'USA',
                'slug': 'usa',
                'description': 'News about USA immigration'
            },
            {
                'name': 'Australia',
                'slug': 'aus',
                'description': 'News about Australian immigration'
            }
        ]

        # Create categories
        for cat_data in categories_data:
            NewsCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )

        # Sample news articles
        news_articles = [
            # Canada News
            {
                'title': 'New Express Entry Draw Announced',
                'content': '''Canada has announced its latest Express Entry draw, inviting 3,500 candidates to apply for permanent residence. 
                            The minimum Comprehensive Ranking System (CRS) score in this draw was 485 points. 
                            This draw represents a significant opportunity for skilled workers looking to immigrate to Canada.
                            Immigration, Refugees and Citizenship Canada (IRCC) continues to work towards its ambitious immigration targets.''',
                'category_slug': 'can',
                'author': 'Immigration Team',
                'is_featured': True
            },
            {
                'title': 'Canada Introduces New Rural Immigration Pilot',
                'content': '''The Canadian government has launched a new pilot program aimed at attracting immigrants to rural communities. 
                            The program offers a pathway to permanent residence for skilled workers who want to live and work in participating rural communities.
                            This initiative aims to address labor shortages and boost economic growth in rural areas.''',
                'category_slug': 'can',
                'author': 'Immigration Team',
                'is_featured': False
            },
            {
                'title': 'Updates to Canadian Study Permit Requirements',
                'content': '''IRCC has announced significant changes to study permit requirements for international students. 
                            The updates include new financial proof requirements and changes to the application process. 
                            These modifications aim to ensure genuine students have the necessary resources to study in Canada.''',
                'category_slug': 'can',
                'author': 'Education Team',
                'is_featured': False
            },
            {
                'title': 'Provincial Nominee Program Expansion',
                'content': '''Several Canadian provinces have announced expansions to their Provincial Nominee Programs (PNP). 
                            New occupation streams and pathways have been added to address regional labor market needs. 
                            These changes provide more opportunities for skilled workers to immigrate to specific provinces.''',
                'category_slug': 'can',
                'author': 'Regional Team',
                'is_featured': False
            },

            # USA News
            {
                'title': 'H1B Visa Updates for 2024',
                'content': '''The U.S. Citizenship and Immigration Services (USCIS) has announced important changes to the H1B visa program for 2024. 
                            Key updates include modifications to the registration process, new wage level requirements, and changes to the selection process. 
                            Employers and potential applicants should be aware of these significant modifications to the program.''',
                'category_slug': 'usa',
                'author': 'Immigration Team',
                'is_featured': True
            },
            {
                'title': 'STEM OPT Extension Program Changes',
                'content': '''USCIS has implemented new guidelines for the STEM OPT extension program. 
                            The changes affect eligibility criteria and employer requirements. 
                            International students in STEM fields should review these important updates.''',
                'category_slug': 'usa',
                'author': 'Education Team',
                'is_featured': False
            },
            {
                'title': 'Green Card Processing Time Improvements',
                'content': '''USCIS announces initiatives to reduce processing times for employment-based green cards. 
                            New streamlined procedures and additional resources have been allocated to address backlogs. 
                            These changes aim to improve the immigration experience for skilled workers.''',
                'category_slug': 'usa',
                'author': 'Processing Team',
                'is_featured': False
            },

            # Australia News
            {
                'title': 'Skilled Migration Program Changes',
                'content': '''Australia's Department of Home Affairs has announced major updates to its Skilled Migration Program. 
                            The changes include revisions to the points test, updates to the skilled occupation lists, and new pathways for permanent residency. 
                            These modifications aim to better address Australia's skills shortages and economic needs.''',
                'category_slug': 'aus',
                'author': 'Immigration Team',
                'is_featured': True
            },
            {
                'title': 'New Regional Visas Introduced',
                'content': '''Australia launches new regional visas to promote migration to regional areas. 
                            These visas offer pathways to permanent residence for skilled workers willing to live and work in regional Australia. 
                            Additional points and processing priorities are available for regional applicants.''',
                'category_slug': 'aus',
                'author': 'Regional Team',
                'is_featured': False
            },
            {
                'title': 'Changes to Student Visa Framework',
                'content': '''The Australian government announces reforms to the student visa framework. 
                            New measures include updated financial requirements and post-study work rights. 
                            These changes aim to maintain Australia's position as a leading education destination.''',
                'category_slug': 'aus',
                'author': 'Education Team',
                'is_featured': False
            },
            {
                'title': 'Employer Sponsored Visa Updates',
                'content': '''Major changes announced for employer-sponsored visa programs in Australia. 
                            Updates include new occupation lists, salary thresholds, and sponsorship requirements. 
                            These changes affect both temporary and permanent employer-sponsored visas.''',
                'category_slug': 'aus',
                'author': 'Employment Team',
                'is_featured': False
            }
        ]

        # Create news articles
        for article in news_articles:
            category = NewsCategory.objects.get(slug=article['category_slug'])
            News.objects.get_or_create(
                title=article['title'],
                defaults={
                    'content': article['content'],
                    'category': category,
                    'author': article['author'],
                    'is_featured': article['is_featured'],
                    'is_published': True,
                    'slug': None  # This will be auto-generated
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully created sample news articles'))
