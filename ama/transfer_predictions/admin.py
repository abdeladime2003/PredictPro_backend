from django.contrib import admin
from .models import Prediction
# Register your models here.
class TransferPredictionAdmin(admin.ModelAdmin):
    list_display = ('user' , 'predicted_price' , 'features' , 'created_at')
    search_fields = ('user' , 'predicted_price' , 'features' , 'created_at')
admin.site.register(Prediction , TransferPredictionAdmin)