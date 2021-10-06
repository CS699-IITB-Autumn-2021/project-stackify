from django.contrib import admin
from .models import Job, Job_preference, Seeker
# Register your models here.

admin.site.register(Seeker)
admin.site.register(Job_preference)
admin.site.register(Job)