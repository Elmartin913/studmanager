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
    PresenceListView,
    SchoolSubjectCreateView,
    MessageFormView,
    UserListView,
    LoginView,
    LogoutView,
    ChangePassView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', SchoolView.as_view(),
         name="index"),
    path('class/<int:school_class>', SchoolClassView.as_view(),
         name="school-class"),
    re_path(r'^student/(?P<student_id>(\d)+)', StudentView.as_view(),
            name="student_details"),
    re_path(r'^grades/(?P<student_id>(\d)+)/(?P<subject_id>(\d)+)', Grades.as_view(),
            name="student_grades"),
    re_path(r'^student_search', StudentSearchView.as_view(),
            name="student_search"),
    re_path(r'^add_student', AddStudentView.as_view(),
            name="add_student"),
    re_path(r'^class_presence/(?P<student_id>(\d)+)/(?P<date>\d{4}-\d{2}-\d{2})$', PresenceListView.as_view(),
            name="class_presence"),
    re_path(r'create_school_subject', SchoolSubjectCreateView.as_view(),
            name="create_school_subject"),
    re_path(r'compose_message', MessageFormView.as_view(),
            name="compose_message"),
    re_path(r'list_users', UserListView.as_view(),
            name="list_users"),
    re_path(r'login', LoginView.as_view(),
            name="login"),
    re_path(r'logout', LogoutView.as_view(),
            name="logout"),
    re_path(r'reset_password/(?P<user_id>(\d)+)$', ChangePassView.as_view(),
            name="reset_password"),
]
