from django.contrib import admin
from .models import project,Message,Topic
# Register your models here.
admin.site.register(project)
admin.site.register(Message)
admin.site.register(Topic)
