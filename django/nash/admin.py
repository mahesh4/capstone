from django.contrib import admin
from .models import Users

class signup(admin.ModelAdmin):
	class Meta:
		model=Users
admin.site.register(Users,signup)
# Register your models here.
