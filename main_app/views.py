from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# importing Finch model
from .models import Finch, Toy
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
    # list of toy ids that finch does have
    id_list = finch.toys.all().values_list('id')
    # query for the toys that the finch doesn't have
    # by using the exclude() method vs the filter() method
    toys_finch_doesnt_have = Toy.objects.exclude(id__in = id_list)
    
    # instantiate FeedingForm() class
    # create form from class
    feeding_form = FeedingForm()
    
    return render(request, 'finches/detail.html',{
        'finch':finch,
        'feeding_form': feeding_form,
        'toys': toys_finch_doesnt_have
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
    fields = ['name','breed','description','age']

# Defining finch update function
class FinchUpdate(UpdateView):
    model = Finch
    fields = ['breed','description','age']

# Defining finch delete function
class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches'
    
def add_feeding(request, cat_id):
  # create a ModelForm instance using 
  # the data that was submitted in the form
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # We want a model instance, but
    # we can't save to the db yet
    # because we have not assigned the
    # cat_id FK.
    new_feeding = form.save(commit=False)
    new_feeding.cat_id = cat_id
    new_feeding.save()
  return redirect('detail', cat_id=cat_id)

# Index of Toys
class ToyList(ListView):
  model = Toy

# Detail of Toys
class ToyDetail(DetailView):
  model = Toy

# Create Toys
class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

# Update Toys
class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

# Delete Toys
class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys'

# Finding Finch & Associating Toy to Finch
def assoc_toy(request, finch_id, toy_id):
  Finch.objects.get(id=finch_id).toys.add(toy_id)
  return redirect('detail', finch_id_id=finch_id)

# Finding Finch & Unassociating Toy from Finch
def unassoc_toy(request, finch_id, toy_id):
  Finch.objects.get(id=finch_id).toys.remove(toy_id)
  return redirect('detail', finch_id=finch_id)