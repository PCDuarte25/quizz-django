from django.contrib import admin
from .models import Person

# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    model = Person
    fields = [
        'name',
        'score',
        'current_question',
    ]
    list_display = [
        'name',
        'score',
        'current_question',
    ]

admin.site.register(Person, PersonAdmin)
