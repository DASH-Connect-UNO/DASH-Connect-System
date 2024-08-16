import logging

from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import StudentForm, AdminForm, CustomUserCreationForm, VisitReasonForm, EditUserForm
from .models import StudentProfile, AdminProfile, VisitReason


logger = logging.getLogger(__name__)
User = get_user_model()


def admin_login_view(request):
    if request.method == 'POST':
        nuid = request.POST.get('nuid')
        password = request.POST.get('password')
        user = authenticate(request, username=nuid, password=password)
        if user is not None:
            if user.user_type == 'admin':
                if user.is_active:
                    login(request, user)
                    return redirect('admin_profile')
                else:
                    return render(request, 'admin/admin_login.html', {'error': 'This admin account is deactivated'})
            else:
                return render(request, 'admin/admin_login.html', {'error': 'You are not authorized as an admin'})
        else:
            return render(request, 'admin/admin_login.html', {'error': 'Invalid NUID or password'})
    else:
        return render(request, 'admin/admin_login.html')


def register_admin(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        admin_form = AdminForm(request.POST)
        if user_form.is_valid() and admin_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'admin'
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            admin = admin_form.save(commit=False)
            admin.user = user
            admin.save()
            return redirect('admin_login')
    else:
        user_form = CustomUserCreationForm()
        admin_form = AdminForm()
    return render(request, 'admin/register_admin.html', {'user_form': user_form, 'admin_form': admin_form})


def register_student(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        student_form = StudentForm(request.POST)

        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'student'  # user_type is set to 'student'
            user.username = user.NUID  # username to NUID
            user.set_password(user_form.cleaned_data['password1'])
            user.save()

            student = student_form.save(commit=False)
            student.user = user
            student.save()
            student_form.save_m2m()

            next_url = request.GET.get('next', 'student_login')
            return redirect(next_url)

    else:
        user_form = CustomUserCreationForm()
        student_form = StudentForm()

    return render(request, 'student/register_student.html', {
        'user_form': user_form,
        'student_form': student_form,
    })


def admin_profile_view(request):
    try:
        admin_profile = request.user.adminprofile
    except AdminProfile.DoesNotExist:
        return redirect('admin_login')
    return render(request, 'admin/admin_profile.html', {'admin_profile': admin_profile})


def add_admin(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        admin_form = AdminForm(request.POST)
        if user_form.is_valid() and admin_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'admin'
            user.username = user.NUID  # Ensure the username is set to NUID
            user.save()
            admin = admin_form.save(commit=False)
            admin.user = user
            admin.save()
            return redirect('admin_list')
    else:
        user_form = CustomUserCreationForm()
        admin_form = AdminForm()
    return render(request, 'admin/add_admin.html', {'user_form': user_form, 'admin_form': admin_form})


def edit_admin(request, NUID):
    admin = get_object_or_404(AdminProfile, user_id=NUID)
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, instance=admin.user)
        admin_form = AdminForm(request.POST, instance=admin)
        if user_form.is_valid() and admin_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'admin'
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            admin_form.save()
            return redirect('admin_list')
    else:
        user_form = CustomUserCreationForm(instance=admin.user)
        admin_form = AdminForm(instance=admin)
    return render(request, 'admin/edit_admin.html', {'user_form': user_form, 'admin_form': admin_form})


def admin_list_view(request):
    admins = AdminProfile.objects.order_by('-user__is_active', 'user__first_name')
    return render(request, 'admin/admin_list.html', {'admins': admins})


def deactivate_admin(request, NUID):
    if request.method == "POST":
        admin = get_object_or_404(User, NUID=NUID)
        admin.is_active = False
        admin.save()
        return redirect('admin_list')


def reactivate_admin(request, NUID):
    if request.method == "POST":
        admin = get_object_or_404(User, NUID=NUID)
        admin.is_active = True
        admin.save()
        return redirect('admin_list')


def student_profile(request, NUID):
    student = get_object_or_404(StudentProfile, user_id=NUID)

    visit_list = student.visitreason_set.all().order_by('-date_time')

    paginator = Paginator(visit_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student/student_profile.html', {
        'student': student,
        'page_obj': page_obj,
    })


def add_student(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'student'
            user.username = user.NUID
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            student_form.save_m2m()
            return redirect('student_information')
    else:
        user_form = CustomUserCreationForm()
        student_form = StudentForm()
    return render(request, 'student/add_student.html',
                  {'user_form': user_form, 'student_form': student_form})


def student_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.user_type == 'student':
                login(request, user)
                return redirect('visit_reason')
            else:
                form.add_error(None, "You are not authorized as a student.")
    else:
        form = AuthenticationForm()
    return render(request, 'student/student_login.html', {'form': form})


def edit_student(request, NUID):
    student = get_object_or_404(StudentProfile, user_id=NUID)
    user = student.user

    if request.method == 'POST':
        edit_user_form = EditUserForm(request.POST, instance=user)
        student_form = StudentForm(request.POST, instance=student)

        if edit_user_form.is_valid() and student_form.is_valid():
            edit_user_form.save()
            student_form.save()
            return redirect('student_profile', NUID=student.user.NUID)
    else:
        edit_user_form = EditUserForm(instance=user)
        student_form = StudentForm(instance=student)

    return render(request, 'student/edit_student.html', {
        'user_form': edit_user_form,
        'student_form': student_form
    })


def student_information(request):
    students = StudentProfile.objects.order_by('-user__is_active', 'user__first_name')
    paginator = Paginator(students, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student/student_information.html', {'page_obj': page_obj})


def toggle_student_status(request, NUID):
    if request.method == "POST":
        student = get_object_or_404(User, NUID=NUID)
        student.is_active = not student.is_active
        student.save()
    return redirect('student_information')


def visit_reason(request):
    if request.method == 'POST':
        form = VisitReasonForm(request.POST)
        if form.is_valid():
            visit_reason = form.save(commit=False)
            visit_reason.student = request.user.studentprofile
            visit_reason.save()
            return redirect('end_page')
    else:
        form = VisitReasonForm()

    return render(request, 'student/visit_reason.html', {'form': form})


def student_activity(request):
    visits = VisitReason.objects.select_related('student__user').order_by(
        '-date_time', 'student__user__first_name', 'student__user__last_name'
    )

    paginator = Paginator(visits, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student/student_activity.html', {'page_obj': page_obj})


def end_page(request):
    return render(request, 'student/end_page.html')
