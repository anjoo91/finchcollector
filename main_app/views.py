from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# importing Finch model
from .models import Finch
from .forms import FeedingForm

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
    # instantiate FeedingForm() class
    # create form from class
    feeding_form = FeedingForm()
    
    return render(request, 'finches/detail.html',{
        'finch':finch,
        'feeding_form': feeding_form
    })

def add_feeding(request, finch_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the finch_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.save()
  return redirect('detail', finch_id=finch_id)

# Defining finch create function
class FinchCreate(CreateView):
    model = Finch
    fields = '__all__'

# Defining finch update function
class FinchUpdate(UpdateView):
    model = Finch
    fields = ['breed','description','age']

# Defining finch delete function
class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches'