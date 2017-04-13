from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Sum
from django.core.urlresolvers import reverse
from django.db.models.functions import Coalesce
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatars')
    info = models.TextField(default='mm')

class TagManager(models.Manager):
    # searches using title
    def get_by_title(self, title):
        return self.get(title=title)


class Tag(models.Model):
    title = models.CharField(max_length=100)
    objects=TagManager()



class QuestionManager(models.Manager):
    # custom query set
    #def get_queryset(self):
        #res = QuestionSet(self.model, using=self._db)
    #    return res.add_answers_count().add_author().add_tags().add_likes()

    # list of new questions
    def list_new(self):
        return self.order_by('-date')

    # list of hot questions
    def list_hot(self):
        return self.order_by('-likes')

    def count_likes(self):
        q = self.get_queryset()

    # list of questions with tag
    def list_tag(self, tag):
        return self.filter(tags=tag)

    # single question
    def get_single(self, id_):
        res = self.get_queryset()
        return res.add_answers().get(id=id_)

    # best questions
    def get_best(self):
        week_ago = timezone.now() + datetime.timedelta(-7)
        return self.get_queryset().order_by_popularity().with_date_greater(week_ago)

class Question(models.Model):
    owner = models.ForeignKey(Profile)
    title = models.CharField(max_length=50)
    text = models.TextField()
    answers = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag)
    likes = models.IntegerField(default=0)

    objects = QuestionManager()
    class Meta:
        ordering = ['-date']


class LikeToQuestionManager(models.Manager):
    # adds a condition: with question
    def has_question(self, question):
        return self.filter(question=question)

    # returns likes count (sum) for a question
    def sum_for_question(self, question):
        res = self.has_question(question).aggregate(sum=Sum('value'))['sum']
        return res if res else 0

    # add like if not exists
    def add_or_update(self, owner, question, value):
        obj, new = self.update_or_create(
                owner=owner,
                question=question,
                defaults={'value': value}
                )

        question.likes = self.sum_for_question(question)
        question.save()
        return new

# TODO Answer manager
class Answer(models.Model):
    owner = models.ForeignKey(Profile)
    question = models.ForeignKey(Question)
    title = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)

class LikeToQuestion(models.Model):
    UP = 1
    DOWN = -1

    question = models.ForeignKey(Question)
    owner = models.ForeignKey(Profile)
    value = models.SmallIntegerField(default=1)
    objects = LikeToQuestionManager()

# TODO Generate tags without repaea
# TODO likes
class LikeToAnswerManager(models.Manager):
    def has_answer(self, answer):
        return self.filter(answer=answer)

    # returns likes count (sum) for a question
    def sum_for_answer(self, answer):
        res = self.has_answer(answer).aggregate(sum=Sum('value'))['sum']
        return res if res else 0

    # add like if not exists
    def add_or_update(self, owner, answer, value):
        obj, new = self.update_or_create(
                owner=owner,
                answer=answer,
                defaults={'value': value}
                )

        answer.likes = self.sum_for_answer(answer)
        answer.save()
        return new



class LikeToAnswer(models.Model):
    UP = 1
    DOWN = -1

    answer = models.ForeignKey(Answer)
    owner = models.ForeignKey(Profile)
    value = models.SmallIntegerField(default=1)
    objects = LikeToAnswerManager()
