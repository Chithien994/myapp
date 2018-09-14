import datetime

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return 'Question #%s' % self.pk

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def create_question(question_text):
        time = timezone.now()
        return Question.objects.create(question_text=question_text, pub_date=time)

    def delete_question(id__in):
        try:
            return Question.objects.filter(pk=id__in).delete()
        except Exception as e:
            return Question.objects.filter(id__in=id__in).delete()

    def update_question(id, question_text, pub_date):
        question = Question.objects.get(pk=id)
        question.question_text = question_text
        question.pub_date = pub_date
        question.save()

    def getCount():
        return Question.objects.filter().count()

    def getQuestion(id__in):
        try:
            return Question.objects.filter(pk=id__in)
        except Exception as e:
            return Question.objects.filter(id__in=id__in)

    class Meta:
        db_table = 'questions'
        verbose_name_plural = 'questions'
        ordering = ['-pub_date']


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choice', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text

    class Meta:
        db_table = 'choice'
        verbose_name_plural = 'choice'