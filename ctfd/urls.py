from django.urls import path
from .views import CTFdConfigView

urlpatterns = [
    path('ctfd-config/', CTFdConfigView.as_view(), name='ctfd_config'),
]
