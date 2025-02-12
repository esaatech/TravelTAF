from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.models import BlogPost, BlogCategory
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a sample blog post about cheap universities in Canada'

    def handle(self, *args, **kwargs):
        # Get or create the category
        category, _ = BlogCategory.objects.get_or_create(
            slug='study-abroad-essentials',
        )

        # Get the first superuser
        author = User.objects.filter(is_superuser=True).first()
        
        if not author:
            self.stdout.write(self.style.ERROR('No superuser found. Please create one first.'))
            return

        content = '''
        <div class="space-y-8">
            <h2 class="text-2xl font-bold">5 Most Affordable Universities in Canada for International Students</h2>

            <p class="text-gray-600">Canada is renowned for its high-quality education, but studying abroad can be expensive. Here are five universities that offer quality education at more affordable rates:</p>

            <div class="space-y-6">
                <div class="university-item">
                    <h3 class="text-xl font-semibold text-[#22C55E]">1. Memorial University of Newfoundland</h3>
                    <ul class="list-disc pl-6 space-y-2 mt-2">
                        <li><strong>Location:</strong> St. John's, Newfoundland</li>
                        <li><strong>Annual Tuition:</strong> $11,460 - $11,460 CAD</li>
                        <li><strong>Known for:</strong> Marine and Ocean Engineering programs</li>
                        <li><strong>Notable:</strong> Lowest tuition fees among major Canadian universities</li>
                    </ul>
                </div>

                <div class="university-item">
                    <h3 class="text-xl font-semibold text-[#22C55E]">2. University of Regina</h3>
                    <ul class="list-disc pl-6 space-y-2 mt-2">
                        <li><strong>Location:</strong> Regina, Saskatchewan</li>
                        <li><strong>Annual Tuition:</strong> $14,000 - $17,500 CAD</li>
                        <li><strong>Known for:</strong> Energy and Environmental studies</li>
                        <li><strong>Notable:</strong> Offers numerous scholarships for international students</li>
                    </ul>
                </div>

                <div class="university-item">
                    <h3 class="text-xl font-semibold text-[#22C55E]">3. Brandon University</h3>
                    <ul class="list-disc pl-6 space-y-2 mt-2">
                        <li><strong>Location:</strong> Brandon, Manitoba</li>
                        <li><strong>Annual Tuition:</strong> $14,500 - $16,000 CAD</li>
                        <li><strong>Known for:</strong> Music and Education programs</li>
                        <li><strong>Notable:</strong> Small class sizes and personalized attention</li>
                    </ul>
                </div>

                <div class="university-item">
                    <h3 class="text-xl font-semibold text-[#22C55E]">4. University of Northern British Columbia</h3>
                    <ul class="list-disc pl-6 space-y-2 mt-2">
                        <li><strong>Location:</strong> Prince George, British Columbia</li>
                        <li><strong>Annual Tuition:</strong> $17,000 - $19,000 CAD</li>
                        <li><strong>Known for:</strong> Environmental and Natural Resource programs</li>
                        <li><strong>Notable:</strong> Beautiful campus and strong research focus</li>
                    </ul>
                </div>

                <div class="university-item">
                    <h3 class="text-xl font-semibold text-[#22C55E]">5. Cape Breton University</h3>
                    <ul class="list-disc pl-6 space-y-2 mt-2">
                        <li><strong>Location:</strong> Sydney, Nova Scotia</li>
                        <li><strong>Annual Tuition:</strong> $17,700 - $18,900 CAD</li>
                        <li><strong>Known for:</strong> Business and Engineering Technology</li>
                        <li><strong>Notable:</strong> Strong support system for international students</li>
                    </ul>
                </div>
            </div>

            <div class="mt-8">
                <h3 class="text-xl font-semibold mb-4">Additional Cost Considerations</h3>
                <p class="mb-4">When planning your budget, remember to account for:</p>
                <ul class="list-disc pl-6 space-y-2">
                    <li>Living expenses (accommodation, food, transportation)</li>
                    <li>Health insurance</li>
                    <li>Study permits and visa fees</li>
                    <li>Books and supplies</li>
                    <li>Emergency funds</li>
                </ul>
            </div>

            <div class="mt-8">
                <h3 class="text-xl font-semibold mb-4">Scholarship Opportunities</h3>
                <p class="mb-4">Many of these universities offer scholarships specifically for international students. It's recommended to:</p>
                <ul class="list-disc pl-6 space-y-2">
                    <li>Apply early for entrance scholarships</li>
                    <li>Check both university and external scholarship options</li>
                    <li>Contact the international student office for guidance</li>
                    <li>Consider work-study programs where available</li>
                </ul>
            </div>

            <p class="mt-8">Remember that while these universities offer lower tuition rates, they still maintain high academic standards and provide quality education. The key is to research thoroughly and apply early, both for admission and financial aid opportunities.</p>
        </div>
        '''

        post = BlogPost.objects.create(
            title='5 Most Affordable Universities in Canada for International Students',
            slug='affordable-universities-canada',
            category=category,
            content=content,
            excerpt='Discover the top 5 budget-friendly Canadian universities for international students, with tuition fees starting from just $11,460 CAD per year.',
            author=author,
            status='PUBLISHED',
            published_at=timezone.now()
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created blog post "{post.title}"')
        ) 