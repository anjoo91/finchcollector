from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
# importing classes for inheritance to create class based views
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# importing things needed for authentication
# login function
from django.contrib.auth import login
# user signup form
from django.contrib.auth.forms import UserCreationForm
# decorator for view funcs to require authentication
from django.contrib.auth.decorators import login_required
# mixins for class based views to require authentication
from django.contrib.auth.mixins import LoginRequiredMixin
# importing models
from .models import Finch, Toy, Photo
# import forms
from .forms import FeedingForm
# importjign things for aws upload
# generate random numbers for ids
import uuid 
# make calls to AWS S3
import boto3 
# reference .env variables (os.environ['BUCKET_NAME'])
import os

# Create your views here.
def home(request): 
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def signup(request):
  # initialize error msg for error handling
  # empty string if no error; will be rendered
  # but can't be seen if it's empty
  error_message = ''
  if request.method == 'POST':
    # initialize sign up form object
    # with the data from the browser page
    form = UserCreationForm(request.POST)
    # if form data is valid, is_valid() will return True
    if form.is_valid():
      # add user by saving the data from form to the db
      user = form.save()
      # now that user has been created, let's log them in automatically
      # we don't need to define a login function since we've already imported it
      login(request, user)
      # redirect to the index page after successful login
      return redirect('index')
    else:
      # if sign up failed, then error message is rendered
      error_message = 'Invalid sign up - try again'
  # create form for initial render for GET request instead of POST
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

# Defining finch index function
# Requires Authentication
@login_required
def finches_index(request):
    # filtering Finch for only rows where user_id = current user
    finches = Finch.objects.filter(user=request.user)
    return render(request, 'finches/index.html', {'finches':finches})

# Defining finch details/show function
@login_required
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
    
# function to add photos to finch
@login_required
def add_photo(request, finch_id):
  # retrieve file from form
  # html: <input type='file' name='photo-file'/>
  photo_file = request.FILES.get('photo-file', None)
  # if a file exists..
  if photo_file:
    # initialize boto3 client
    s3 = boto3.client('s3')
    # key = path for where file will be stored + name of file + file extension
    # photo_file.name.rfind('.') returns anything right of the period in the string ('.jpg','.gif',etc.)
    key = 'finchcollector-s3/' + uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.')]
    try:
      bucket = os.environ['BUCKET_NAME']
      # upload to s3
      s3.upload_fileobj(photo_file, bucket, key)

      # build url for where the image is stored on s3
      url = f'{os.environ["S3_BASE_URL"]}{bucket}/{key}'
      # save the url to the photo model with an fk for the finch
      Photo.objects.create(url=url, finch_id = finch_id)
    except Exception as e:
      print('An error occured uploading to s3, probably wrong url, bucket name or keys. code ~/.aws/credentials is where your keys are.')
      print(e)
  # when done, redirect back to detail page
  return redirect('detail', finch_id = finch_id)
    

@login_required
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
class FinchCreate(LoginRequiredMixin, CreateView):
    model = Finch
    fields = ['name','breed','description','age']

    # we need to define what happens when a cat form
    # is submitted - basically we have to set user attr
    # to the current user
    def form_valid(self, form):
      # assign the current user to user attribute in cat
      # form.instance is the cat bc the class is called in each instance
      # of a cat
      form.instance.user = self.request.user
      # we let CreateView do its job as usual
      return super().form_valid(form)
# Defining finch update function
class FinchUpdate(LoginRequiredMixin, UpdateView):
    model = Finch
    fields = ['breed','description','age']

# Defining finch delete function
class FinchDelete(LoginRequiredMixin, DeleteView):
    model = Finch
    success_url = '/finches'

# Index of Toys
class ToyList(LoginRequiredMixin, ListView):
  model = Toy

# Detail of Toys
class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

# Create Toys
class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

# Update Toys
class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

# Delete Toys
class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys'

# Finding Finch & Associating Toy to Finch
@login_required
def assoc_toy(request, finch_id, toy_id):
  Finch.objects.get(id=finch_id).toys.add(toy_id)
  return redirect('detail', finch_id=finch_id)

# Finding Finch & Unassociating Toy from Finch
@login_required
def unassoc_toy(request, finch_id, toy_id):
  Finch.objects.get(id=finch_id).toys.remove(toy_id)
  return redirect('detail', finch_id=finch_id)