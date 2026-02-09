from .views import ProjectSubmitView, ProjectDetailView , AllProjectsView
from django.urls import path

urlpatterns = [
    path('submit/', ProjectSubmitView.as_view(), name='project_submit'),
    path('detail/', ProjectDetailView.as_view(), name='project_detail'),
    path('all/', AllProjectsView.as_view(), name='all_projects'),
]