from django.contrib import admin
from iblapp.models import Greeting


@admin.register(Greeting)
class GreetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'message')
# Register your models here.
