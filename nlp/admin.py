from django.contrib import admin
from .models import record, record_aggregate
# Register your models here.
admin.site.register(record)
admin.site.register(record_aggregate)