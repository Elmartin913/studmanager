from django import forms
from .models import (SCHOOL_CLASS, Student, SchoolSubject)


class StudentSearchForm(forms.Form):

    name = forms.CharField(label='Nazwisko ucznia')
