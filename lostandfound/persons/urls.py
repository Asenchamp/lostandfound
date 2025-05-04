from django.urls import path
from . import views 

urlpatterns=[
    path('addMissingPerson/', views.addMissingPerson.as_view(), name='addMP'),
    path('editMissingPerson/<int:pk>/', views.updateMissingPerson.as_view(), name='editMP'),
    path('detailsMissingPerson/<int:pk>/', views.detailsMissingPerson.as_view(), name='detailsMP'),
    path('deleteMissingPerson/<int:pk>/', views.deleteMissingPerson.as_view(), name='deleteMP'),
]
