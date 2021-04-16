from django.db import models
from django.utils import timezone
# Create your models here.

class record(models.Model):
    api_name = models.CharField(max_length=600,blank=True,null=True)
    input_text = models.TextField(blank=True,null=True)
    output_text = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.created_at)

class record_aggregate(models.Model):
    api_name = models.CharField(max_length=600,blank=True,null=True)
    call_amount = models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.created_at)

