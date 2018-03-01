"""studmanage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from smapp.views import (
    SchoolView,
    SchoolClassView,
    StudentView,
    Grades,
    StudentSearchView,
    AddStudentView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', SchoolView.as_view(),
         name="index"),
    path('class/<int:school_class>', SchoolClassView.as_view(),
         name="school-class"),
    path('^student/<student_id>', StudentView.as_view(),
         name="student_details"),
    path('^grades/<int:student_id>/<int:subject_id>', Grades.as_view(),
         name="student_grades"),
    re_path(r'^student_search', StudentSearchView.as_view(),
            name="student_search"),
    re_path(r'^add_student', AddStudentView.as_view(),
            name="add_student"),
]
