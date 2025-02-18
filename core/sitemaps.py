from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import BlogPost, BlogCategory
from news.models import News
from immigrationprograms.models import ImmigrationProgram
from faqs.models import FAQ
from testimonials.models import Testimonial

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

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return [
            'home',
            'about',
            'contact',
            'blog:blog_list',
            'news:news_list',
            'faqs:faq_list',
            'testimonials:testimonial_list',
            'immigrationprograms:program_list',
            'resume_builder:home',
            'customerSupport:contact',
        ]

    def location(self, item):
        return reverse(item)
