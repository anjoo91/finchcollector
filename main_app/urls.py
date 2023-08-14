from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name = 'about'),
    # finch index route
    path('finches/', views.finches_index, name = 'index'),\
    # finch detail route
    path('finches/<int:finch_id>/', views.finches_detail, name='detail'),
]
