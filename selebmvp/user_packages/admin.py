from django.contrib import admin
from .models import UserPackages

@admin.register(UserPackages)
class UserPackagesAdmin(admin.ModelAdmin):
	fieldsets = [
		("User Packages", {"fields": ["filename", "name", "owner"]}),
	]

	list_display = ("name", "owner", "filename",)
