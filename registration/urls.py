from django.urls import path
from .views import BasicPassRegistrationView , SpecialPassRegistrationView

urlpatterns = [
    path('basic-pass/', BasicPassRegistrationView.as_view(), name='basic_pass_registration'),
    path('special-pass/', SpecialPassRegistrationView.as_view(), name='special_pass_registration'),
]
