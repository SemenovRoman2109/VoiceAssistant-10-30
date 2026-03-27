from django.contrib import admin
from .models import VoiceAnswer, AppCommand, AppGroup, WebSite

# Register your models here.
admin.site.register([VoiceAnswer, AppCommand, AppGroup, WebSite])