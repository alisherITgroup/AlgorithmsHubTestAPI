from django.db import models

class Test(models.Model):
    nano = models.CharField(max_length=16)
    status = models.CharField(max_length=50, default="Accepted")
    author = models.CharField(max_length=100)
    code = models.TextField(default="")
    language = models.CharField(max_length=20, default="python")
    tests = models.TextField(default={})
    timelimit = models.FloatField(default=1)
    results = models.TextField(default={})
    time = models.FloatField(default=0)

    def __str__(self):
        return self.nano