from rest_framework import viewsets, generics, permissions, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Avg, Count
from .models import Department, Employee, Attendance, Performance
from .serializers import DepartmentSerializer, EmployeeSerializer, AttendanceSerializer, PerformanceSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import HttpResponse
import csv
from django.utils import timezone

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('department').all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email', 'department__name']
    ordering_fields = ['hire_date', 'salary']

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('employee').all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related('employee').all()
    serializer_class = PerformanceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

# Analytics endpoint: aggregates
class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Single-query-friendly aggregates
        dept_counts = Department.objects.annotate(num_employees=Count('employees')).values('name','num_employees')
        avg_salary = Employee.objects.aggregate(avg_salary=Avg('salary'))
        avg_rating = Performance.objects.aggregate(avg_rating=Avg('rating'))
        data = {
            'departments': list(dept_counts),
            'avg_salary': float(avg_salary['avg_salary'] or 0),
            'avg_rating': float(avg_rating['avg_rating'] or 0)
        }
        return Response(data)

# CSV export for employees
class EmployeeCSVExportView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        qs = Employee.objects.all().select_related('department')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="employees_{timezone.now().date()}.csv"'
        writer = csv.writer(response)
        writer.writerow(['id','first_name','last_name','email','department','hire_date','salary'])
        for e in qs:
            writer.writerow([e.id, e.first_name, e.last_name, e.email, e.department.name if e.department else '', e.hire_date, e.salary])
        return response

# health
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health(request):
    return Response({'status':'ok', 'timestamp': str(timezone.now())})
