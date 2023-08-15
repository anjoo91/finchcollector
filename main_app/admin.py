from django.contrib import admin

# Register your models here.
from .models import Finch, Feeding

# Give CRUD operations to admin app for Finch table in db
admin.site.register(Finch)
admin.site.register(Feeding)