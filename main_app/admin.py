from django.contrib import admin

# Register your models here.
from .models import Finch

# Give CRUD operations to admin app for Finch table in db
admin.site.register(Finch)