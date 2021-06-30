from django.urls import path
from . import views

app_name = "data"

urlpatterns = [
    path('', views.home, name="home"),
    path('import/', views.PostImport.as_view(), name="csv"),
    path('check/', views.CheckData.as_view(), name='check'),

    path('register/', views.register, name='register'),
    path('create_category/', views.create_category, name='create_category'),
    path('data_register/', views.data_register, name='data_register'),
    path('create_tag/', views.create_tag, name='create_tag'),
    path('import_contentful/', views.import_contentful, name='import_contentful'),
]
