from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import News, NewsCategory

class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(NewsCategory, slug=category_slug)
            return News.objects.filter(
                category=category, 
                is_published=True,
                status='APPROVED'
            )
        return News.objects.filter(
            is_published=True,
            status='APPROVED'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = NewsCategory.objects.all()
        context['is_user_authenticated'] = self.request.user.is_authenticated
         
        return context
    

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve the dialog content associated with the news
        dialog_content = getattr(self.object, 'dialog_content', None)
        
        # Print statements to verify the dialog content
        if dialog_content:
            print(f"Dialog Title: {dialog_content.title}")
            print(f"Dialog Body: {dialog_content.body}")
        else:
            print("No dialog content found for this news article.")
        
        return context
