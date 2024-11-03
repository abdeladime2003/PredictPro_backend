from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ( 'first_name',)
# Enregistrer les modèles dans l'interface d'administration avec personnalisation
admin.site.register(User, UserAdmin)