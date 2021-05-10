"""
App urls
"""

from django.contrib.auth.views import PasswordResetView
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.home, name='home',),
    path('accounts/profile/', views.profile, name = 'profile'),
    path('accounts/signup/', views.signup.as_view(), name='signup'),
    path('accounts/signup/company/', views.signup_company, name='signup_company'),
    path('accounts/signup/client/', views.signup_client, name='signup_client'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('lots/', views.CompanyLotsListView.as_view(), name='lots'),
    path('lot/<slug:slug>', views.CompanyLotDetailView.as_view(), name='lot_detail'),
    
]
