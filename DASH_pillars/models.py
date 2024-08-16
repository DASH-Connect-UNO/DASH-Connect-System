from django.db import models

class Scholarship(models.Model):
    name = models.CharField(max_length=255)
    is_deactivated = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Hardship(models.Model):
    name = models.CharField(max_length=255)
    is_deactivated = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class BasicNeedSupport(models.Model):
    name = models.CharField(max_length=255)
    is_deactivated = models.BooleanField(default=False)

    def __str__(self):
        return self.name

