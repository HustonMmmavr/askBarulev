from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Sum
from django.core.urlresolvers import reverse
from    django.db.models.functions import Coalesce
import datetime

#class Profile(models.Model)


class User(models.Model):
    nick = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    image = models.ImageField(upload_to='avat')
    email = models.EmailField()
    login = models.CharField(max_length=50)

    def __unicode__(self):
    	return self.nick + ": " +str(self.id)

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
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=50)
    text = models.TextField()
    answers = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag)
    likes = models.IntegerField(default=0)

    objects = QuestionManager()
    #def likes(self):
    #    return LikeToQuestion.objects.sum_for_question(self)
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

class Answer(models.Model):
    owner = models.ForeignKey(User)
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
    owner = models.ForeignKey(User)
    value = models.SmallIntegerField(default=1)
    objects = LikeToQuestionManager()

# TODO Generate tags without repaea
# TODO likes
class LikeToAnswerManager(models.Manager):
    def has_answer(self, answer):
        return self.filter(answer=answer)

    # returns likes count (sum) for a question
    def sum_for_question(self, answer):
        res = self.has_question(answer).aggregate(sum=Sum('value'))['sum']
        return res if res else 0

    # add like if not exists
    def add_or_update(self, owner, answer, value):
        obj, new = self.update_or_create(
                owner=owner,
                answer=answer,
                defaults={'value': value}
                )

        answer.likes = self.sum_for_question(answer)
        answer.save()
        return new



class LikeToAnswer(models.Model):
    UP = 1
    DOWN = -1

    answer = models.ForeignKey(Answer)
    owner = models.ForeignKey(User)
    value = models.SmallIntegerField(default=1)
    objects = LikeToAnswerManager()


        # return if self.has_question(question).aggregate(sum=Sum('value'))['sum']
    #def sum_for_questions(self, questions)

         #ltq = LikeToQuestion.objects#.sum_for_question(self)
    #     likes = []
         #for q in self:
    #         #likes.append({'likes': ltq.sum_for_question(q)})
        #    q.likes = ltq.sum_for_question(q)
    #         print(q.likes)
    #         print(q)
    #         # if lik:
         #   print(str(q.id) + " " + str(q.likes))
    #         # q.add(likes=ltq.sum_for_question(q))

    #     for q in self:
    #         print(q.likes)


    # class QuestionSet(models.QuerySet):
#     def add_tags(self):
#         return self.prefetch_related('tags')
    
#     # preloads answers
#     def add_answers(self):
#         res = self.prefetch_related('answer_set')
#         res = self.prefetch_related('answer_set__owner')
#         # res = self.prefetch_related('answer_set__author__profile')
#         return res

#     # loads number of answers
#     def add_answers_count(self):
#         return self.annotate(answers_cnt=Count('answer__id', distinct=True))

#     def add_likes(self):

#         ltq = LikeToQuestion.objects#.sum_for_question(self)
#         likes = []
#         for q in self:
#         #likes.append({'likes': ltq.sum_for_question(q)})
#             q.likes = ltq.sum_for_question(q)
#             print(q.likes)
#             print(q)
#             # if lik:
#             print(str(q.id) + " " + str(q.likes))
#         # q.add(likes=ltq.sum_for_question(q))
#         return self.annotate(lik_cnt=LikeToQuestion.objects.value__sum)#Count('liketoquestion__id', distinct=True))
#          #aggregate(lik_cnt=(Sum('liketoquestion.question_id')))['sum']#, 0))#notate(likes=ltq.sum_for_question(int(self.id)))#(lambda f: (for q in self:
#     #                                     #ltq.sum_for_question(self))))#ltq.sum_for_question(self))
#     # loads author
#     def add_author(self):
#         return self.select_related('owner')#.select_related('owner__')

#     # order by popularity
#     def order_by_popularity(self):
#         return self.order_by('-likes')

#     # filter by date
#     def with_date_greater(self, date):
#         return self.filter(date__gt=date)
