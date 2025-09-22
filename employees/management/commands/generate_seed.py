from django.core.management.base import BaseCommand
from faker import Faker
from employees.models import Department, Employee, Attendance, Performance, Goal
import random
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Generate sample employees, departments, attendance, performance'

    def handle(self, *args, **options):
        fake = Faker()
        # Create some departments
        depts = ['Engineering','Sales','HR','Finance']
        dept_objs = []
        for d in depts:
            obj, _ = Department.objects.get_or_create(name=d, defaults={'location': fake.city()})
            dept_objs.append(obj)
        # Create 5 employees
        employees = []
        for _ in range(5):
            first = fake.first_name()
            last = fake.last_name()
            email = fake.unique.email()
            dept = random.choice(dept_objs)
            hire = fake.date_between(start_date='-5y', end_date='today')
            sal = round(random.uniform(30000,120000),2)
            emp = Employee.objects.create(
                first_name=first, last_name=last, email=email,
                department=dept, hire_date=hire, salary=sal,
                employment_type=random.choice(['FT','PT','CT','IN'])
            )
            employees.append(emp)

        # Attendance & performance
        for emp in employees:
            # Attendance for last 10 days
            for i in range(10):
                day = timezone.now().date() - timedelta(days=i)
                Attendance.objects.create(employee=emp, date=day, status=random.choice(['present','absent','leave']), hours=8.0 if random.random()>0.1 else 0)
            # Performance 2 reviews
            for j in range(2):
                Performance.objects.create(
                    employee=emp,
                    review_date=timezone.now().date() - timedelta(days=30*(j+1)),
                    rating=random.randint(1,5),
                    score=round(random.uniform(50,100),2),
                    comments=fake.sentence()
                )

        self.stdout.write(self.style.SUCCESS('Generated seed data: 5 employees + attendance + performance'))
