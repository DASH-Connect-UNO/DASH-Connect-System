from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    student_login_view, admin_login_view, admin_profile_view, student_profile, add_admin, edit_admin,
    edit_student, admin_list_view, register_admin, add_student, student_information, visit_reason,
    toggle_student_status, deactivate_admin, reactivate_admin, student_activity, register_student, end_page
)

urlpatterns = [
    path('student_login/', student_login_view, name='student_login'),
    path('admin_login/', admin_login_view, name='admin_login'),
    path('admin_profile/', admin_profile_view, name='admin_profile'),
    path('add_student/', add_student, name='add_student'),
    path('student_information/', student_information, name='student_information'),
    path('student_profile/<str:NUID>/', student_profile, name='student_profile'),
    path('add_admin/', add_admin, name='add_admin'),
    path('edit_admin/<str:NUID>/', edit_admin, name='edit_admin'),
    path('edit_student/<str:NUID>/', edit_student, name='edit_student'),
    path('admin_list/', admin_list_view, name='admin_list'),
    path('logout/', LogoutView.as_view(next_page='admin_login'), name='logout'),
    path('register_admin/', register_admin, name='register_admin'),
    path('register_student/', register_student, name='register_student'),
    path('visit_reason/', visit_reason, name='visit_reason'),
    path('student_activity/', student_activity, name='student_activity'),
    path('toggle-status/<str:NUID>/', toggle_student_status, name='toggle_student_status'),
    path('deactivate-admin/<str:NUID>/', deactivate_admin, name='deactivate_admin'),
    path('reactivate-admin/<str:NUID>/', reactivate_admin, name='reactivate_admin'),
    path('end_page/', end_page, name='end_page'),
]

