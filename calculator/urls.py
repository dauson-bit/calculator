# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('program_selection/', views.program_selection, name='program_selection'),
    path('course_list/<int:program_id>/<int:year>/<int:semester>/', views.course_list, name='course_list'),
    path('gpa_result/<int:program_id>/<int:year>/<int:semester>/', views.gpa_result, name='gpa_result'),
]
