from django.db import models

# Create your models here.
class List(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField(null=True)
    duedate = models.DateTimeField(null=True)

    def __str__(self):
        return self.title