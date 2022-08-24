from django.urls import path, re_path
from . import views

urlpatterns = [
    path('cognitive_assessment_home', views.cognitive_assessment_home, name='cognitive_assessment_home'),
    path('cognitive_task', views.cognitive_task, name='cognitive_task'),
    path('exit_view_cognitive_task', views.exit_view_cognitive_task, name='exit_view_cognitive_task')
]

