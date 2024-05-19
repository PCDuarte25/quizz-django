from django.db import models

# Create your models here.
class Person(models.Model):
    class Meta:
        verbose_name = 'Pessoa'

    name = models.CharField('nome', unique=True, max_length=128)
    score = models.SmallIntegerField('pontuação', default=0)
    current_question = models.SmallIntegerField('questão atual', default=1)
