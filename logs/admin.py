from django.contrib import admin

# Register your models here.

from .models import OperationLog, SessionLog

admin.site.register(OperationLog)
admin.site.register(SessionLog)