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
                'title': 'H1B Visa Updates for 2024',
                'content': '''The U.S. Citizenship and Immigration Services (USCIS) has announced important changes to the H1B visa program for 2024. 
                            Key updates include modifications to the registration process, new wage level requirements, and changes to the selection process. 
                            Employers and potential applicants should be aware of these significant modifications to the program.''',
                'category_slug': 'usa',
                'author': 'Immigration Team',
                'is_featured': True
            },
            {
                'title': 'Skilled Migration Program Changes',
                'content': '''Australia's Department of Home Affairs has announced major updates to its Skilled Migration Program. 
                            The changes include revisions to the points test, updates to the skilled occupation lists, and new pathways for permanent residency. 
                            These modifications aim to better address Australia's skills shortages and economic needs.''',
                'category_slug': 'aus',
                'author': 'Immigration Team',
                'is_featured': True
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
