from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class List(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField(null=True)
    duedate = models.DateTimeField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", null = True)
    img = models.TextField(null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
