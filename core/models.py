from django.db import models

# Create your models here.
class VoiceAnswer(models.Model):
    request = models.CharField(max_length= 255)
    response = models.TextField()
    def __str__(self):
        return f"Відповідь на {self.request}"
    
class AppCommand(models.Model):
    path = models.CharField(max_length= 255)
    name = models.CharField(max_length= 100)
    keyword = models.CharField(max_length= 100)
    def __str__(self):
        return f"Запускає {self.name} за комнадою {self.keyword}"