from django.shortcuts import render
from django.http import JsonResponse
import random
from datetime import timedelta

def visa_checker(request):
    if request.method == 'POST':
        from_country = request.POST.get('fromCountry')
        to_country = request.POST.get('toCountry')
        
        if not from_country or not to_country:
            return JsonResponse({
                'error': 'Both countries are required'
            }, status=400)

        # Simulate API response
        visa_statuses = ['visa_required', 'visa_free', 'visa_on_arrival', 'e_visa']
        processing_times = ['5-7 business days', '10-15 business days', '3-4 weeks', '24-48 hours']
        costs = ['$50', '$100', '$150', '$200', 'Free']
        
        response_data = {
            'status': random.choice(visa_statuses),
            'details': {
                'processing_time': random.choice(processing_times),
                'validity': f"{random.randint(1, 12)} months",
                'cost': random.choice(costs),
                'max_stay': f"{random.randint(30, 180)} days",
                'entry_type': random.choice(['Single', 'Multiple']),
                'requirements': [
                    'Valid passport',
                    'Passport-size photos',
                    'Bank statements',
                    'Travel insurance',
                    'Hotel bookings',
                    'Return ticket'
                ],
                'additional_info': [
                    'Passport must be valid for at least 6 months',
                    'Must have at least 2 blank pages in passport',
                    'Proof of sufficient funds may be required'
                ]
            }
        }
        
        return JsonResponse(response_data)
        
    return render(request, 'tools/visa_checker.html')

def points_calculator(request):
    return render(request, 'tools/points_calculator.html')

def cost_estimator(request):
    return render(request, 'tools/cost_estimator.html')

def document_checker(request):
    return render(request, 'tools/document_checker.html')

def timeline_planner(request):
    return render(request, 'tools/timeline_planner.html')

def language_test(request):
    return render(request, 'tools/language_test.html')

def job_search(request):
    return render(request, 'tools/job_search.html')

def school_finder(request):
    return render(request, 'tools/school_finder.html')
