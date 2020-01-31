from django.contrib import admin
from .models import Users, exampledata, datanew

admin.site.register(Users)
admin.site.register(datanew)
admin.site.register(exampledata)
