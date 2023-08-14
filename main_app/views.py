from django.shortcuts import render
# importing Finch model
from .models import Finch

# Create your views here.
def home(request): 
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# Defining finch index function
def finches_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', {'finches':finches})

# Defining finch details/show function
def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    return render(request, 'finches/detail.html', {'finch':finch})