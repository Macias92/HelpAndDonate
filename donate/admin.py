from django.contrib import admin

# Register your models here.
from donate.models import User, Institution

admin.site.register(User)
admin.site.register(Institution)
