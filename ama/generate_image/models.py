from django.db import models
from users.models import User
class GeneratedImage(models.Model):
    prompt = models.CharField(max_length=255)
    image_data = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Permettre des valeurs nulles pour user
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Image generated for prompt: {self.prompt}"
