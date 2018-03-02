from django import forms

from .validators import range_validator
from .models import (
    SCHOOL_CLASS, Student, SchoolSubject, Message
)


class StudentSearchForm(forms.Form):

    name = forms.CharField(label='Nazwisko ucznia')


class AddStudentForm(forms.Form):

    first_name = forms.CharField(label='Imie', max_length=64)
    last_name = forms.CharField(label='Nazwisko', max_length=64)
    school_class = forms.ChoiceField(label='Klasa', choices=SCHOOL_CLASS)
    year_of_birth = forms.IntegerField(label="Data urodzenia", validators=[range_validator])


class PresenceListForm(forms.Form):

    student = forms.ModelChoiceField(label='Student', queryset=Student.objects.all())
    day = forms.DateField(label='Data', widget=forms.HiddenInput())
    present = forms.NullBooleanField(label='Obecnosc')


class SchoolSubjectForm(forms.ModelForm):
    class Meta:
        model = SchoolSubject
        # fields = '__all__'
        fields = ['name', 'teacher_name']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['date_sent']


class LoginForm(forms.Form):
    login = forms.CharField(label='Login')
    password = forms.CharField(label='Haslo', widget=forms.PasswordInput)


class ChangePassForm(forms.Form):
    old_pass = forms.CharField(widget=forms.PasswordInput())
    new_pass = forms.CharField(widget=forms.PasswordInput())
    new_pass_2 = forms.CharField(widget=forms.PasswordInput())
