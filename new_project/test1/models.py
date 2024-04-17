from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    start_time = models.DateTimeField(default='')
    end_time = models.DateTimeField(default='')
    priority_choices = (('1', 'Very important'), ('2', 'Important'), ('3', 'Ordinary'))
    priority = models.CharField(max_length=20, choices=priority_choices, default='3')
    def __str__(self):
        return self.title


class Notebook(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    cover = models.ImageField(upload_to='images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notebook_detail', args=[self.id])

# Create your models here.