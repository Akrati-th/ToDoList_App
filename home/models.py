from django.db import models
from django.contrib.auth.models import User


class MyTask(models.Model):
    priority_choices = [
        ('H', 'HIGH'),
        ('K', 'MODERATE'),
        ('L', 'LOW')
    ]

    status_choices = [
        ('S', 'FINISHED'),
        ('P', 'IN PROGRESS'),
        ('N', 'NOT STARTED YET')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=1, choices=priority_choices, blank=False, null=False)
    status = models.CharField(max_length=1, choices=status_choices, blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['status', '-created_on']


