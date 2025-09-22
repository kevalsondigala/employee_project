from django.db import models
from django.contrib.auth import get_user_model

class Department(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    EMPLOYMENT_TYPE = [('FT','Full-Time'),('PT','Part-Time'),('CT','Contract'),('IN','Intern')]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees')
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    hire_date = models.DateField()
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPE, default='FT')
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present','Present'),('absent','Absent'),('leave','Leave')])
    hours = models.DecimalField(max_digits=4, decimal_places=2, default=8.0)

    class Meta:
        unique_together = ('employee','date')

class Performance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance')
    review_date = models.DateField()
    rating = models.PositiveSmallIntegerField()  # 1-5
    score = models.DecimalField(max_digits=5, decimal_places=2)
    comments = models.TextField(blank=True)

class Goal(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=150)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)
