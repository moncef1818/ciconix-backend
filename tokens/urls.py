from django.urls import path
from .views import TokenSubmitView, TeamTokenHistoryView

urlpatterns = [
    path('submit/', TokenSubmitView.as_view(), name='token_submit'),
    path('history/', TeamTokenHistoryView.as_view(), name='team_token_history'),
]