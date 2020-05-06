from django.db import models

# Create your models here.
class Hospital(models.Model):
    Name = models.TextField(default='name')
    Contact = models.TextField(default='0')
    Address = models.TextField(default='hospital')
    pin = models.TextField(default='0')
    isoTotal = models.BigIntegerField(default=50)
    isoFree = models.BigIntegerField(default=10)
    uptime = models.TimeField(auto_now=True)


