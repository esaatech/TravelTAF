from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from tools.models import Country
from .models import ImmigrationProgram, FeaturedCountry
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
    Fetch immigration data for featured countries with program limits
    Returns a dictionary with country data and their approved programs
    """
    PROGRAMS_LIMIT = 5  # Show only 5 programs in dropdown
    
    featured_countries = FeaturedCountry.objects.filter(
        is_active=True
    ).select_related('country')
    
    immigration_data = {}
    for featured in featured_countries:
        country = featured.country
        
        # Get all approved programs for this country
        all_programs = ImmigrationProgram.objects.filter(
            country=country,
            status='APPROVED'
        )
        
        # Calculate totals and limits
        total_programs = all_programs.count()
        limited_programs = all_programs.values('name', 'slug')[:PROGRAMS_LIMIT]
        
        immigration_data[country.iso_code_2] = {
            'country_info': {
                'name': country.name,
                'slug': country.iso_code_2.lower(),
            },
            'programs': list(limited_programs),  # Only first 5 programs
            'total_programs': total_programs,    # Total count
            'has_more': total_programs > PROGRAMS_LIMIT,  # True if more than 5
            'remaining_count': max(0, total_programs - PROGRAMS_LIMIT)  # How many more
        }
    
    return immigration_data

def immigration_nav_programs(request):
    immigration_data = get_featured_immigration_data()
    is_mobile = 'mobile' in request.GET
    
    print("Request GET params:", request.GET)  # Debug info
    print("Is mobile?", is_mobile)
    
    template_name = (
        "immigrationprograms/partials/nav_programs_mobile.html" if is_mobile
        else "immigrationprograms/partials/nav_programs.html"
    )
    print("Using template:", template_name)
    
    return render(request, template_name, {
        "immigration_data": immigration_data
    })