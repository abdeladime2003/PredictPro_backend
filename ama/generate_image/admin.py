from django.contrib import admin
from .models import GeneratedImage
class GeneratedImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'prompt', 'created_at']
    search_fields = ['prompt']
    list_filter = ['created_at']
admin.site.register(GeneratedImage, GeneratedImageAdmin
)   
# Register your models here.
