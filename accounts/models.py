from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from accounts.CustomUserManager import CustomUserManager


class CustomUser(AbstractUser):
    # Explicitly removed the username field
    username = None

    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    NUID = models.CharField(max_length=8, unique=True, primary_key=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'NUID'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.NUID})"


class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, db_column='nuid')
    role_within_DASH = models.CharField(max_length=50)
    edits_made = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.NUID})"


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, db_column='nuid')
    year = models.CharField(max_length=50)
    other_year = models.CharField(max_length=100, blank=True, null=True)
    DASH_Member = models.BooleanField(default=False)
    scholarships = models.ManyToManyField('DASH_pillars.Scholarship', blank=True)
    hardships = models.ManyToManyField('DASH_pillars.Hardship', blank=True)
    basic_need_supports = models.ManyToManyField('DASH_pillars.BasicNeedSupport', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class VisitReason(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE)
    appointment = models.BooleanField(default=False)
    printing = models.BooleanField(default=False)
    study = models.BooleanField(default=False)
    socialize = models.BooleanField(default=False)
    student_affinity_group = models.BooleanField(default=False)
    event = models.BooleanField(default=False)
    schedule_appointment = models.BooleanField(default=False)
    hardship = models.BooleanField(default=False)
    basic_needs_support = models.BooleanField(default=False)
    financial_wellness = models.BooleanField(default=False)
    volunteer_opportunities = models.BooleanField(default=False)
    other = models.BooleanField(default=False)
    date_time = models.DateTimeField(default=timezone.now)

    def clean(self):
        super().clean()
        if not (
            self.appointment or
            self.printing or
            self.study or
            self.socialize or
            self.student_affinity_group or
            self.event or
            self.schedule_appointment or
            self.hardship or
            self.basic_needs_support or
            self.financial_wellness or
            self.volunteer_opportunities or
            self.other
        ):
            raise ValidationError(_('At least one reason for the visit must be selected.'))

    def __str__(self):
        return f"Visit Reason ID: {self.id} for {self.student.user.first_name} {self.student.user.last_name}"

