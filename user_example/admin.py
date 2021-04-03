from django.contrib import admin
from .models import UserPanel, Doctor, Comment, VisitTime

# Register your models here.

admin.site.register(UserPanel)
admin.site.register(Doctor)
admin.site.register(Comment)
admin.site.register(VisitTime)