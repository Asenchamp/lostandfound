from django.urls import path
from . import views
urlpatterns=[
    path('',views.landingPage.as_view(),name='landing'),
    path('dashboard/',views.dashboard.as_view(),name='dashboard'),
    path('county-autocomplete/', views.CountyAutocomplete.as_view(), name='county-autocomplete'),
    path('location/<county_id>/', views.get_full_location, name='get_full_location'),
]