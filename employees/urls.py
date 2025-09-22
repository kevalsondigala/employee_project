from rest_framework import routers
from .views import EmployeeViewSet, DepartmentViewSet, AttendanceViewSet, PerformanceViewSet, AnalyticsView, EmployeeCSVExportView, health
from django.urls import path, include

router = routers.DefaultRouter()
router.register('employees', EmployeeViewSet)
router.register('departments', DepartmentViewSet)
router.register('attendance', AttendanceViewSet)
router.register('performance', PerformanceViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/analytics/', AnalyticsView.as_view(), name='analytics'),
    path('api/export/employees/', EmployeeCSVExportView.as_view(), name='employee-csv'),
    path('health/', health),
]