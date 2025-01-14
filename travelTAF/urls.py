"""
URL configuration for travelTAF project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # This will handle all core app URLs, including home page
    path("__reload__/", include("django_browser_reload.urls")),
    path('api/agent/', include('agent.urls')),
    path('news/', include('news.urls', namespace='news')),
    path('subscribers/', include('subscribers.urls')),
    path('tools/', include('tools.urls')),  # Include tools app URLs
    path('authentication/', include('authentication.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('credits/', include('credits.urls')),
    path('payments/', include('payments.urls')),
    path('resume_builder/', include('resume_builder.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('customerSupport/', include('customerSupport.urls')),
    path('faqs/', include('faqs.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('service_offerings/', include('service_offerings.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
