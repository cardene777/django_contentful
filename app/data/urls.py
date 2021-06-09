from django.urls import path
from . import views

app_name = "data"

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('import/', views.PostImport.as_view(), name="csv"),
    path('check/', views.CheckData.as_view(), name='check'),

    # choice path
    path('choice_hospital/', views.choice_hospital, name="choice_hospital"),
    path('choice_category/', views.choice_category, name="choice_category"),
    path('choice_url/', views.choice_url, name="choice_url"),
    path('choice_form/', views.choice_form, name="choice_form"),
    path('data_register/', views.data_register, name="data_register"),



    path('data_choice/', views.data_choice, name='data_choice'),
    path('register/', views.register, name='register'),
    path('extract/', views.extract, name='extract'),
]
