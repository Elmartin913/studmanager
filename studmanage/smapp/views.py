from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views import View

# Create your views here.
from .models import (
    SCHOOL_CLASS,
    Student,
    SchoolSubject,
    StudentGrades,
)


class SchoolView(View):

    def get(self, request):
        ctx = {
            'classes': SCHOOL_CLASS
        }
        return TemplateResponse(request, 'school_view.html', ctx)


class SchoolClassView(View):

    def get(self, request, school_class):
        students = Student.objects.filter(school_class=school_class)
        return render(request, "class.html", {"students": students,
                                              "class_name": SCHOOL_CLASS[int(school_class) - 1][1]
                                              })
