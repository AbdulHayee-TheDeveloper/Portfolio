from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    # path("about/", views.about, name='about'),
    # path("projects/", views.projects, name='projects'),
    path("experiences/", views.experiences_view, name='experiences'),
    path("skills/", views.skills_section, name='skills'),
    path("contact/", views.contact, name='contact'),
    path("resume/",views.resume,name="resume"),

    path('projects/', views.all_projects, name='all_projects'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
   
]



