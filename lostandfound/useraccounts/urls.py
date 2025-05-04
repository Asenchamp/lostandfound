from django.urls import path
from . import views


urlpatterns = [
    path('register/',views.registerView.as_view(),name='register'),
    path('login/',views.customloginView.as_view(),name='login'),
    path('logout/',views.customlogoutView.as_view(),name='logout'),
]