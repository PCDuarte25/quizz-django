from django.contrib import admin
from .models import Person

# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    model = Person
    fields = [
        'name',
        'score',
        'current_question',
        'quizz_start_time',
        'quizz_end_time',
    ]
    list_display = [
        'pk',
        'name',
        'score',
        'current_question',
        'quizz_start_time',
        'quizz_end_time',
    ]

admin.site.register(Person, PersonAdmin)
