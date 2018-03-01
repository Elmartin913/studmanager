from django.contrib import admin
from .models import Student

# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'school_class', 'year_of_birth', 'suspended']
    exclude = ('year_of_birth',)  # nie mozna edytowac i go nie widzimy aby byla krotka musi po str byc ,


admin.site.register(Student, StudentAdmin)
