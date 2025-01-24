from django.db import models
from django.contrib.auth.models import User

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clock_in_time = models.DateTimeField(null=True, blank=True)
    clock_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.clock_in_time} to {self.clock_out_time}"
