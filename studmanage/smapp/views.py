from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, request
from django.urls import reverse, reverse_lazy

# Create your views here.
from .models import (
    SCHOOL_CLASS,
    Student,
    SchoolSubject,
    StudentGrades,
    PresenceList,
)

from .forms import (
    StudentSearchForm,
    AddStudentForm,
    PresenceListForm,
    SchoolSubjectForm,
    MessageForm,
    LoginForm,
    ChangePassForm,
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


class PresenceListView(View):

    def get(self, request, student_id, date):
        form = PresenceListForm(initial={'day': date})
        return render(request, 'class_presence.html', {'form': form})

    def post(self, request, student_id, date):
        form = PresenceListForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            day = form.cleaned_data['day']
            present = form.cleaned_data['present']
            PresenceList.objects.create(
                student=student,
                day=day,
                present=present
            )
            url = reverse('student_details', kwargs={'student_id': student.id})
            return HttpResponseRedirect(url)


class SchoolSubjectCreateView(CreateView):
    form_class = SchoolSubjectForm
    template_name = 'school_subject_form.html'
    success_url = reverse_lazy('create_school_subject')


class MessageFormView(CreateView):
    form_class = MessageForm
    template_name = 'message_create_form.html'
    success_url = reverse_lazy('compose_message')


class UserListView(ListView):
    model = User
    template_name = 'user_list.html'


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login2 = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(
                username=login2,
                password=password
            )
            if user is not None:
                login(request, user)
                return HttpResponse('Zalogowany {}'.format(user.username))
            else:
                return HttpResponse('Niepoprawne dane do logowania')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


class ChangePassView(PermissionRequiredMixin, View):
    permission_required = 'change_user'

    def get(self, request, user_id):
        form = ChangePassForm()
        return render(request, 'change_pass.html', {'form': form})

    def post(self, request, user_id):
        form = ChangePassForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=user_id)
            user = authenticate(
                username=user.username,
                password=form.cleaned_data['old_pass']
            )
            if not user.check_password(form.cleaned_data['old_pass']):
                return HttpResponse('Niepoprane aktualne haslo')

            if form.cleaned_data['new_pass'] != form.cleaned_data['new_pass_2']:
                return HttpResponse('Nowe hasla nie s takie same')

            user.set_password(form.cleaned_data['new_pass'])
            user.save()
            return HttpResponse('Haso zmienione')
