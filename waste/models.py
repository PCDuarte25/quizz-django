from django.db import models

# Create your models here.
class Person(models.Model):
    class Meta:
        verbose_name = 'Pessoa'

    name = models.CharField('nome', unique=True, max_length=128)
    score = models.SmallIntegerField('pontuação', default=0)
    current_question = models.SmallIntegerField('questão atual', default=1)
    quizz_start_time = models.DateTimeField('horário que começou o quizz', auto_now_add=True)
    quizz_end_time = models.DateTimeField('horário que terminou o quizz', null=True)

    @property
    def get_finished_quizz_time(self):
        return self.quizz_end_time - self.quizz_start_time

    @property
    def is_quizz_finished(self):
        return self.quizz_end_time is not None
