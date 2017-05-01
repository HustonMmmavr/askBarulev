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

    def get_avatar(self):
        return str(self.avatar)

class TagManager(models.Manager):
    def get_or_create(self, title):
        try:
            tag = self.get_by_title(title)
        except Tag.DoesNotExist:
            tag = self.create(title=title)
        return tag
    
    # searches using title
    def get_by_title(self, title):
        return self.get(title=title)


class Tag(models.Model):
    title = models.CharField(max_length=100)

    def get_url(self):
        return reverse(kwargs={'tag': self.title})
    objects=TagManager()


# class QuestionQuerySet(models.QuerySet):
#     # preloads tags
#     def with_tags(self):
#         return self.prefetch_related('tags')


#     # preloads answers
#     def with_answers(self):
#         res = self.prefetch_related('answer_set')
#         #res = self.prefetch_related('answer_set__author')
#        # res = self.prefetch_related('answer_set__author__user')
#         return res

#     def order_by_popularity(self):
#         return self.order_by('-likes')

#     # loads number of answers
#     def with_answers_count(self):
#         return self.annotate(answers_count=Count('answer__id', distinct=True))

#     # loads author
#     def with_author(self):
#         return self.select_related('owner').select_related('owner__user')

#    # loads number of answers
#    # def with_answers_count(self):
        # return self.annotate(answers_count=Count('answer__id', distinct=True))

class QuestionManager(models.Manager):
    qs = None

    def init(self):
        self.qs = self.get_queryset()
        return self

    def get_query(self):
        return self.qs

    def add_tags(self):
        self.qs.prefetch_related('tags')
        return self

    # preloads answers
    def add_answers(self):
        self.qs.prefetch_related('answer_set')
        return self

    # loads author
    def add_author(self):
        self.qs.select_related('owner').select_related('owner__user')
        return self
 
    # list of hot questions
    def list_hot(self):
        return self.init().add_tags().add_author().get_query().order_by('-likes')

    def list_ordered_date(self):
        return self.init().add_tags().add_author().order_by('-date')
    
    # list of questions with tag
    def list_tag(self, tag):
        return self.init().add_tags().add_author().filter(tags=tag).order_by('-date')

    # single question
    def get_single(self, id_):
        return self.init().add_author().add_answers().add_tags().get(id=id_)

    # best questions
    # def get_best(self):
        # week_ago = timezone.now() + datetime.timedelta(-7)
        # return self.get_queryset().order_by_popularity().with_date_greater(week_ago)

class Question(models.Model):
    owner = models.ForeignKey(Profile)
    title = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag)
    likes = models.IntegerField(default=0)
    answers_cnt = models.IntegerField(default = 0)

    objects = QuestionManager()


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

# class AnswerQuerySet(models.QuerySet):
#     # loads author
#     def with_author(self):
#         return self.select_related('author').select_related('author__profile')

#     # loads question
#     def with_question(self):
#         return self.select_related('question')

#     # order by popularity
#     def order_by_popularity(self):
#         return self.order_by('-likes')

#     # filter by date
#     def with_date_greater(self, date):
#         return self.filter(date__gt=date)

class AnswerManager(models.Manager):
    # # custom query set
    # def get_queryset(self):
    #     res = AnswerQuerySet(self.model, using=self._db)
    #     return res.with_author()

    def has_question(self, question):
        return self.filter(question=question)

    def sum_for_question(self, question):
        res = self.has_question(question).count()
        return res if res else 0

    # create
    def create(self, **kwargs):
        ans = super(AnswerManager, self).create(**kwargs);
        #print('a')
        ans.question.answers_cnt = self.sum_for_question(ans.question)
        #print('b')
        ans.question.save()
        #print('c')
        return ans

#     # best answers
#     def get_best(self):
#         week_ago = timezone.now() + datetime.timedelta(-7)
# return self.get_queryset().order_by_popularity().with_date_greater(week_ago)

class Answer(models.Model):
    owner = models.ForeignKey(Profile)
    question = models.ForeignKey(Question)
    title = models.CharField(max_length=150)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)
    objects = AnswerManager()

class LikeToQuestion(models.Model):
    UP = 1
    DOWN = -1

    question = models.ForeignKey(Question)
    owner = models.ForeignKey(Profile)
    value = models.SmallIntegerField(default=1)
    objects = LikeToQuestionManager()

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
