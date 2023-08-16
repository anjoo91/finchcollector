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
    # finch add feeding route
    path('finches/<int:finch_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    # associating finch & toy route
    path('finches/<int:finch_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
    # unassociating finch & toy route
    path('finches/<int:finch_id>/unassoc_toy/<int:toy_id>/', views.unassoc_toy, name='unassoc_toy'),
    # toys index route
    path('toys/', views.ToyList.as_view(), name='toys_index'),
    # toys detail route
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
    # toys create route
    path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    # toys update route
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
    # toys delete route
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
]
