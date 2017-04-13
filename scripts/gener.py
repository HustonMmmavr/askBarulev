from ask.models import Tag, User, Question, Answer, LikeToQuestion, LikeToAnswer
import random


def generate_users(cnt):#, names, surnames):
	names = ['john', 'peter', 'kolya', 'misha', 'pasha', 'ilja', 'trump', 'derek']
	snames = ['obama', 'trum', 'ivanov' , 'prtrov', 'lomov', 'morgan']
	mails = ['ya', 'ma', 'go']
	nsize = len(names)
	ssize = len(snames)
	msize = len(mails)
	for i in range(0,cnt):
		print(i)
		name = names[random.randint(0, nsize-1)] + ' ' + snames[random.randint(0, ssize - 1)]
		email = names[random.randint(0, nsize - 1)] + '@' + mails[random.randint(0, msize - 1)] + '.ru'
		pwd = str(random.randint(10000,1000000))
		img = 'rnd'
		login = 'login'
		u = User(nick=name, password=pwd, image=img, email=email, login=login)
		u.save()
	print('use')

def generate_questions(n):
	arr = open('/home/comp/askBarulev/scripts/text.txt', 'r').read().split(' ')
	asize = len(arr)
	print(asize)
	tag_table_cnt = Tag.objects.count()
	qcount = User.objects.count()
	for i in range(0,n):
		print(i)
		word_cnt = random.randint(20,50)
		text = ''
		title = arr[random.randint(0,asize-1)] + ' ' + str(i)
		own = User.objects.filter(id=random.randint(1, qcount))[0]
		for j in range(0,word_cnt):
			text += arr[random.randint(0,(asize-1))] + ' '

		q = Question(owner=own, title=title,text=text)
		q.save()
		tag_cnt = random.randint(1, 5)
		for j in (0,tag_cnt):
			tq = Tag.objects.filter(id=random.randint(1, tag_table_cnt))[0]
			q.tags.add(tq)
	print('que')

#36
		# print(own)
		#or el in own:
		#	print(el)
		# print(own.id)
	#for u in User.objects.all():
	#	print(u.nick)
		

def generate_answers(n):
	#for u in User.objects.all()[0]:
	#	print(u.nick)
	arr = open('/home/comp/askBarulev/scripts/text.txt', 'r').read().split(' ')
	asize = len(arr)#.size()
	ucount = User.objects.count()
	qcount = Question.objects.count()

	for i in range(0,n):
		print(i)
		word_cnt = random.randint(20,50)
		text = ''
		title = arr[random.randint(0,asize-1)] + ' ' + str(i)
		own = User.objects.filter(id=random.randint(1, ucount))[0]

		for j in range(0,word_cnt):
			text += arr[random.randint(0,(asize-1))] + ' '

		q = Question.objects.filter(id=random.randint(1, qcount))[0]
		a = Answer(owner=own, question=q, title=title,text=text)
		a.save()
	print('ans')

def generate_answer_likes(n):
	arr = [-1, 1]
	answers = Answer.objects.count()
	print(answers)
	users = User.objects.count()
	for i in range(0, n):
		print(i)
		idx = random.randint(0,1)
		u = User.objects.filter(id=random.randint(1, users))[0]
		a = Answer.objects.filter(id=random.randint(1, answers))[0]
		al = LikeToAnswer(answer=a, owner=u, value=arr[idx])
		LikeToAnswer.objects.add_or_update(u, a, arr[idx])
		#al.save()
	print('al')


def generate_question_likes(n):
	arr = [-1, 1]
	questions = Question.objects.count()
	users = User.objects.count()
	for i in range(0, n):
		print(i)
		idx = random.randint(0,1)
		u = User.objects.filter(id=random.randint(1, users))[0]
		a = Question.objects.filter(id=random.randint(1, questions))[0]
		al = LikeToQuestion(question=a, owner=u, value=arr[idx])
		LikeToQuestion.objects.add_or_update(u, a, arr[idx])
		#al.save()
	print('aq')


def generate_tags(n):
	#print('aaa')
	arr = open('/home/comp/askBarulev/scripts/tags', 'r').read().split(' ')
	asize = len(arr)#.size()
	for i in range(0, asize):
		#//tornd = random.randint(0,asize-1)
		#print(arr[tornd])
		t = Tag(title=arr[i])
		t.save()
	print('tag')


def run():
	try:
		#i = 0
		#while i < 10:
		#	print(random.randint(0,1))
		generate_users(100)
		generate_tags(125)
		generate_questions(1150)
		generate_answers(1150)
		generate_answer_likes(2500)
		generate_question_likes(2500)
	except Exception as ex:
	    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
	    message = template.format(type(ex).__name__, ex.args)
	    print(message)
