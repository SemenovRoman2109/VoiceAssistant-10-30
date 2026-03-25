from django.contrib import admin
from .models import VoiceAnswer, AppCommand

# Register your models here.
admin.site.register([VoiceAnswer, AppCommand])