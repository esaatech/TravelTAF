from django.shortcuts import render

def visa_checker(request):
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
