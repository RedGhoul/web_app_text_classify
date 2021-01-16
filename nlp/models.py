from django.db import models
from django.utils import timezone
# Create your models here.

class record(models.Model):
    input_text = models.TextField()
    output_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.created_at)

class apistat(models.Model):
    name = models.TextField()
    hit_count = models.IntegerField()

    def __str__(self):
        return str(self.name) + " " + str(self.hit_count)