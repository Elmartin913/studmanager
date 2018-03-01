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

from .forms import (
    StudentSearchForm,
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


class StudentView(View):

    def get(self, request, student_id):
        student = Student.objects.get(pk=student_id)
        subjects = SchoolSubject.objects.all()
        ctx = {
            "student": student,
            "subjects": subjects
        }
        return render(request, "student.html", ctx)


class Grades(View):

    def get(self, request, student_id, subject_id):
        student = Student.objects.get(pk=student_id)
        subject = SchoolSubject.objects.get(pk=subject_id)
        grades = StudentGrades.objects.filter(
            student_id=student_id,
            school_subject=subject_id
        )

        try:
            sum = 0
            for g in grades:
                sum += int(g.grade)
            avg = round(sum / len(grades), 2)
        except ZeroDivisionError:
            avg = 0

        ctx = {
            'student': student,
            'subject': subject,
            'grades': grades,
            'avg': avg,
        }
        return render(request, 'grades.html', ctx)


class StudentSearchView(View):

    def get(self, request):
        form = StudentSearchForm()
        return render(request, 'student_search.html', {'form': form})

    def post(self, request):
        form = StudentSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            students = Student.objects.filter(last_name__icontains=name)
            # niezwaza na wielkosc znakow
            return render(request, 'student_search.html', {'form': form, 'students': students})
