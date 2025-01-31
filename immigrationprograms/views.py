from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from tools.models import Country
from .models import ImmigrationProgram
from django.http import JsonResponse
from tools.models import Countries

def program_list(request):
    """Display countries that have immigration programs"""
    countries = Country.objects.filter(
        immigration_programs__status='APPROVED',  # Only approved programs
        immigration_programs__isnull=False  # Only countries with programs
    ).distinct().prefetch_related(
        Prefetch(
            'immigration_programs',
            queryset=ImmigrationProgram.objects.filter(
                status='APPROVED'
            ).order_by('-featured', '-created_at')
        )
    )

    return render(request, "programs/country_list.html", {
        "countries": countries,
        "featured_programs": ImmigrationProgram.objects.filter(
            status='APPROVED',
            featured=True
        )[:5]  # Limit featured programs
    })

def country_programs(request, country_slug):
    """Display all programs for a specific country"""
    country = get_object_or_404(Country, slug=country_slug)
    
    programs = ImmigrationProgram.objects.filter(
        country=country,
        status='APPROVED'
    ).select_related('country').order_by('-featured', '-created_at')

    return render(request, "programs/country_detail.html", {
        "country": country,
        "programs": programs,
    })

def program_detail(request, country_slug, program_slug):
    """Display specific program details"""
    # First get the country using iso_code_2
    country = get_object_or_404(Countries, iso_code_2__iexact=country_slug.upper())
    
    # Then get the program using the country and program slug
    program = get_object_or_404(
        ImmigrationProgram.objects.select_related('country'), 
        country=country,  # Use the country object directly
        slug=program_slug,
        status='APPROVED'
    )
    
    # Get related programs from same country
    related_programs = ImmigrationProgram.objects.filter(
        country=country,
        status='APPROVED'
    ).exclude(id=program.id)[:3]

    return render(request, "immigrationprograms/program_detail.html", {
        "program": program,
        "related_programs": related_programs,
    })

def get_countries_with_programs(request):
    """API endpoint to get specific countries with active programs"""
    specific_countries = ['UK', 'CA', 'NZ']  # ISO codes for UK, Canada, New Zealand
    countries = Country.objects.filter(
        immigration_programs__status='APPROVED',
        iso_code_2__in=specific_countries
    ).distinct().values('name', 'slug', 'flag_url')
    
    return JsonResponse({'countries': list(countries)})

def get_featured_immigration_data():
    """
    Fetch immigration data for specific countries (UK, Canada, New Zealand)
    Returns a dictionary with country data and their approved programs
    """
    FEATURED_COUNTRIES = ['UK', 'CA', 'NZ']
    
    # Get the countries
    countries = Countries.objects.filter(
        iso_code_2__in=FEATURED_COUNTRIES
    ).values('name', 'iso_code_2')

    # Create a structured response with programs for each country
    immigration_data = {}
    for country in countries:
        programs = ImmigrationProgram.objects.filter(
            country__iso_code_2=country['iso_code_2'],
            status='APPROVED'
        ).values('name', 'slug')
        
        immigration_data[country['iso_code_2']] = {
            'country_info': {
                'name': country['name'],
                'slug': country['iso_code_2'].lower(),
            },
            'programs': list(programs)
        }
    
    return immigration_data

def immigration_nav_programs(request):
    immigration_data = get_featured_immigration_data()
    is_mobile = 'mobile' in request.GET
    template_name = (
        "immigrationprograms/partials/nav_programs_mobile.html" if is_mobile
        else "immigrationprograms/partials/nav_programs.html"
    )
    return render(request, template_name, {
        "immigration_data": immigration_data
    })