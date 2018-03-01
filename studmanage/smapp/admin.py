from django.contrib import admin
from .models import Student

# Register your models here.


def suspend_student(admin, request, queryset):
    queryset.update(suspended=True)


suspend_student.short_description = 'Zawies studentow'


def unsuspend_student(admin, request, queryset):
    queryset.update(suspended=False)


unsuspend_student.short_description = 'Odwies studentow'


class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'school_class', 'year_of_birth', 'suspended']
    exclude = ('year_of_birth',)  # nie mozna edytowac i go nie widzimy aby byla krotka musi po str byc ,
    actions = (suspend_student, unsuspend_student)


admin.site.register(Student, StudentAdmin)
