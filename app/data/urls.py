from django.urls import path
from . import views

app_name = "data"

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('import/', views.PostImport.as_view(), name="csv"),
    path('check/', views.CheckData.as_view(), name='check'),
    path('data_import', views.data_import, name='data_import'),
    path('extraction/', views.extraction, name='extraction'),
    path('register/', views.register, name='register'),
]
