from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import BlogPost
from news.models import News
from immigrationprograms.models import ImmigrationProgram
from faqs.models import FAQ
from testimonials.models import Testimonial
from tools.models import School, VisaRelationship

class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return BlogPost.objects.filter(status='PUBLISHED')

    def lastmod(self, obj):
        return obj.updated_at or obj.published_at

class NewsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return News.objects.filter(status='PUBLISHED', is_published=True)

    def lastmod(self, obj):
        return obj.updated_date

class ImmigrationProgramsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return ImmigrationProgram.objects.filter(status='APPROVED')

    def lastmod(self, obj):
        return obj.updated_at

class FAQSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return FAQ.objects.filter(is_active=True)

class TestimonialsSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Testimonial.objects.filter(is_active=True)

class SchoolSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return School.objects.all()

class VisaSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return VisaRelationship.objects.filter(is_active=True)

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return [
            'main:home',
            'main:about',
            'main:contact',
            'main:compare_countries',
            'main:get_started',
            'main:learn_more',
            'main:privacypolicy',
            'main:terms',
            'main:cookies',
            
            'blog:post_list',
            'news:list',
            'faqs:faq_list',
            'testimonials:testimonial_list',
            
            'service_offerings:services',
            'service_offerings:study_abroad',
            'service_offerings:work_visas',
            'service_offerings:permanent_residency',
            'service_offerings:family_sponsorship',
            'service_offerings:moving_abroad',
            'service_offerings:travel_planning',
            'service_offerings:travel_tours',
            
            'tools:all_tools',
            'tools:visa_checker',
            'tools:flight_search',
            'tools:cost_estimator',
            'tools:school_finder',
            'tools:language_test',
            'tools:job_search',
            'tools:resume_builder',
            'tools:cover_letters',
            'tools:points_calculator',
            'tools:timeline_planner',
            'tools:document_checker',
            
            'immigration:program_list',
        ]

    def location(self, item):
        return reverse(item)
