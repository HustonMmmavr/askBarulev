from ask.models import Tag, User, Profile, Question, Answer, LikeToQuestion, LikeToAnswer
import random
import os

def generate_users(cnt):#, names, surnames):
	names = ['john', 'peter', 'kolya', 'misha', 'pasha', 'ilja', 'trump', 'derek']
	snames = ['obama', 'trum', 'ivanov' , 'prtrov', 'lomov', 'morgan']
	mails = ['ya', 'ma', 'go']
	nsize = len(names)
	ssize = len(snames)
	msize = len(mails)
	# print('a')
	imgs = os.listdir('/home/comp/askBarulev/scripts/test_img')
	imgsc = len(imgs)
	# print(imgs)
	#u = Profile.objects.all()
	#for t in u:
	#	print(t.avatar)
	for i in range(0,cnt):
		print(i)
		fname = names[random.randint(0, nsize-1)]
		sname = snames[random.randint(0, ssize - 1)]
		email = names[random.randint(0, nsize - 1)] + '@' + mails[random.randint(0, msize - 1)] + '.ru'
		pwd = str(random.randint(10000,1000000))
		u = User()
		u.username = fname + ' ' + sname + str(i)#data.get('username')
		u.password = pwd#make_password(password)
		u.email = email#data.get('email')
		u.first_name = fname#data.get('first_name')
		u.last_name = sname#data.get('last_name')
		u.is_active = True
		u.is_superuser = False
		u.save()

		img = imgs[random.randint(0, imgsc - 1)]
		print(img)
		#f = open('/home/comp/askBarulev/scripts/test_img/' + img, "r")

		#login = 'login'
		p = Profile(user=u, avatar=img)#User(use=name, password=pwd, image=img, email=email, login=login)
		p.save()
		print(p.avatar)	# print('use')

def generate_questions(n):
	arr = open('/home/comp/askBarulev/scripts/text.txt', 'r').read().split(' ')
	asize = len(arr)
	print(asize)
	tag_table_cnt = Tag.objects.count()
	print(tag_table_cnt)
	qcount = Profile.objects.count()
	for i in range(0,n):
		print(i)
		word_cnt = random.randint(20,50)
		text = ''
		title = arr[random.randint(0,asize-1)] + ' ' + str(i)
		own = Profile.objects.filter(id=random.randint(1, qcount))[0]
		for j in range(0,word_cnt):
			text += arr[random.randint(0,(asize-1))] + ' '

		q = Question(owner=own, title=title,text=text)
		q.save()
		tag_cnt = random.randint(1, 5)
		print(tag_cnt)
		for j in range(0,tag_cnt):
			print(j)
			tq = Tag.objects.filter(id=random.randint(1, tag_table_cnt))[0]
			print(tq.title)
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
	ucount = Profile.objects.count()
	qcount = Question.objects.count()

	for i in range(0,n):
		print(i)
		word_cnt = random.randint(20,50)
		text = ''
		title = arr[random.randint(0,asize-1)] + ' ' + str(i)
		own = Profile.objects.filter(id=random.randint(1, ucount))[0]

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
	users = Profile.objects.count()
	for i in range(0, n):
		print(i)
		idx = random.randint(0,1)
		u = Profile.objects.filter(id=random.randint(1, users))[0]
		a = Answer.objects.filter(id=random.randint(1, answers))[0]
		al = LikeToAnswer(answer=a, owner=u, value=arr[idx])
		LikeToAnswer.objects.add_or_update(u, a, arr[idx])
		#al.save()
	print('al')


def generate_question_likes(n):
	arr = [-1, 1]
	questions = Question.objects.count()
	users = Profile.objects.count()
	for i in range(0, n):
		print(i)
		idx = random.randint(0,1)
		u = Profile.objects.filter(id=random.randint(1, users))[0]
		a = Question.objects.filter(id=random.randint(1, questions))[0]
		al = LikeToQuestion(question=a, owner=u, value=arr[idx])
		LikeToQuestion.objects.add_or_update(u, a, arr[idx])
		#al.save()
	print('aq')


def generate_tags(n):
	#print('aaa')
	arr = open('/home/comp/askBarulev/scripts/tags', 'r').read().split('\n')
	asize = len(arr)#.size()
	for i in range(0, asize):
		t = Tag(title=arr[i])
		print(t.title)
		t.save()
	print('tag')


def run():
	try:
		#i = 0
		#while i < 10:
		#	print(random.randint(0,1))
		#generate_users(100)
		generate_tags(125)
		generate_questions(150)
		generate_answers(210)
		generate_answer_likes(350)
		generate_question_likes(350)
	except Exception as ex:
	    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
	    message = template.format(type(ex).__name__, ex.args)
	    print(message)
