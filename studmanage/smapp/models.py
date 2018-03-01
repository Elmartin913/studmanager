from django.db import models

# Create your models here.

SCHOOL_CLASS = (
    (1, "1a"),
    (2, "1b"),
    (3, "2a"),
    (4, "2b"),
    (5, "3a"),
    (6, "3b"),
)

GRADES = (
    (1, "1"),
    (1.5, "1+"),
    (1.75, "2-"),
    (2, "2"),
    (2.5, "2+"),
    (2.75, "3-"),
    (3, "3"),
    (3.5, "3+"),
    (3.75, "4-"),
    (4, "4"),
    (4.5, "4+"),
    (4.75, "5-"),
    (5, "5"),
    (5.5, "5+"),
    (5.75, "6-"),
    (6, "6")
)


class SchoolSubject(models.Model):
    name = models.CharField(max_length=64)
    teacher_name = models.CharField(max_length=64)

    @property
    def name2(self):
        return "{} - {}".format(self.teacher_name, self.name)

    def __str__(self):
        return self.name2


class Student(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    school_class = models.IntegerField(choices=SCHOOL_CLASS, verbose_name='Klasa')
    grades = models.ManyToManyField(SchoolSubject, through="StudentGrades")
    year_of_birth = models.IntegerField(null=True, blank=True, verbose_name='Rok urodzenia')  # brlam pozwala na wyslanie niewypenionego pola
    suspended = models.BooleanField(default=False, verbose_name='Zawieszony')

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.name


class StudentGrades(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    school_subject = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE)
    grade = models.FloatField(choices=GRADES)


class Message(models.Model):
    subject = models.CharField(max_length=256, verbose_name='Temat')
    content = models.TextField(null=True)
    date_sent = models.DateTimeField(auto_now_add=True)  # tylko data utworzenia, auto_now - czas ostatniego uzycia
    to = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE)
    author = models.ForeignKey(Student, on_delete=models.CASCADE)

