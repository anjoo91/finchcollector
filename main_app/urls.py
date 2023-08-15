from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name = 'about'),
    # finch index route
    path('finches/', views.finches_index, name = 'index'),\
    # finch detail route
    path('finches/<int:finch_id>/', views.finches_detail, name='detail'),
    # finch create route
    path('finches/create/', views.FinchCreate.as_view(), name='finch_create'),
    # finch update route
    path('finches/<int:pk>/update/', views.FinchUpdate.as_view(), name='finch_update'),
    # finch delete route
    path('finches<int:pk>/delete/', views.FinchDelete.as_view(), name='finch_delete'),
]
