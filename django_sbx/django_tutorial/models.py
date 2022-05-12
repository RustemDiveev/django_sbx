import datetime

from django.db import models
from django.utils import timezone 

# Create your models here.
class Question(models.Model):
    """
        Список вопросов
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        """
            Представление объекта в интерактивном режиме
        """
        return self.question_text

    def was_published_recently(self):
        """
            Был ли вопрос опубликован сегодня
        """
        # Фикс, после того как тест вскрыл ошибку метода 
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now 
    
class Choice(models.Model):
    """
        Вариант ответа на тот или иной вопрос и подсчет голосов 
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
            Представление объекта в интерактивном режиме
        """
        return self.choice_text
