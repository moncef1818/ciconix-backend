from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import TeamLoginView, TeamLogoutView, TeamProfileView
urlpatterns = [
        path('login/', TeamLoginView.as_view(), name='team_login'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
        path('profile/', TeamProfileView.as_view(), name='team_profile'),
        path('logout/', TeamLogoutView.as_view(), name='team_logout'),
]