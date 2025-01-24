from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clock_in = models.DateTimeField(default=timezone.now)
    clock_out = models.DateTimeField(null=True, blank=True)
    work_duration = models.DurationField(null=True, blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    def save(self, *args, **kwargs):
        if self.clock_in and self.clock_out:
            self.work_duration = self.clock_out - self.clock_in
        super().save(*args, **kwargs)
