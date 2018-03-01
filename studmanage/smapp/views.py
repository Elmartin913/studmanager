from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpResponseRedirect, request
from django.urls import reverse, reverse_lazy

# Create your views here.
from .models import (
    SCHOOL_CLASS,
    Student,
    SchoolSubject,
    StudentGrades,
)

from .forms import (
    StudentSearchForm,
    AddStudentForm,
    SchoolSubjectForm,
    MessageForm,
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


class AddStudentView(View):

    def get(self, request):
        form = AddStudentForm()
        return render(request, 'add_student.html', {'form': form})

    def post(self, request):
        form = AddStudentForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            school_class = form.cleaned_data['school_class']
            year_of_birth = form.cleaned_data['year_of_birth']
            new_student = Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                school_class=school_class,
                year_of_birth=year_of_birth
            )
            # new_student = Student.objects.create(**form.cleaned_data) rozpakowanie slownika
            url = reverse('student_details', kwargs={'student_id': new_student.id})   # generuje url
            return HttpResponseRedirect(url)

        else:
            return render(request, 'add_student.html', {'form': form})


class SchoolSubjectCreateView(CreateView):
    form_class = SchoolSubjectForm
    template_name = 'school_subject_form.html'
    success_url = reverse_lazy('create_school_subject')


class MessageFormView(CreateView):
    form_class = MessageForm
    template_name = 'message_create_form.html'
    success_url = reverse_lazy('compose_message')
