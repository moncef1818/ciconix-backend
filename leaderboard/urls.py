from .views import LeaderboardView
from django.urls import path

urlpatterns = [
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]