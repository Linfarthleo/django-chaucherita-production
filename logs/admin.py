from django.contrib import admin

# Register your models here.

from .models import OperationLog, SessionLog, InvalidLoginLog

admin.site.register(OperationLog)
admin.site.register(SessionLog)
admin.site.register(InvalidLoginLog)