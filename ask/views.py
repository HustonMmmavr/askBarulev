
from django.http import HttpResponse, Http404, HttpResponseRedirect
from  django.template import loader
from django.template import Template
from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ask.models import Question, Profile, Answer, LikeToQuestion, LikeToAnswer, Tag
from ask.form import LoginForm, SignupForm, SettingsForm, NewQuestionForm, AnswerForm
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from ask.decorators import need_login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
import simplejson as json

@csrf_exempt
def main( wsgi_request):
    resp = ['<p>I Like ruby!</p>']
    print(wsgi_request)
    print(wsgi_request.GET)
    if wsgi_request.method == 'GET':
        if (len(wsgi_request.GET)):
            resp.append("GET<br>")
            print(wsgi_request.GET.items)
            for item in wsgi_request.GET:
                print (item, wsgi_request.GET[item])
                arr = (item, '=', wsgi_request.GET[item],'<br>')
                resp.append(''.join(arr))

    if wsgi_request.method == 'POST':
        print(wsgi_request.POST.items)
        resp.append("POST<br>")
        if (len(wsgi_request.POST)):
            for item in wsgi_request.POST:
                print (item, wsgi_request.body)
                arr = (item, '=', wsgi_request.POST[item],'<br>')
                resp.append(''.join(arr))
    return HttpResponse(resp)


def paginate(objects, count_on_page, page_num, pages_to_show):
	print(page_num)
	paginator = Paginator(objects, count_on_page)
	interval = int(pages_to_show / 2) + 1
	
	try:
		num_page = int(page_num)
	except ValueError:
		num_page = 1
	except PageNotAnInteger:
		num_page = 1
	if num_page < 1:
		num_page = 1
	if num_page > paginator.num_pages:
		num_page = paginator.num_pages
	
	paginated = paginator.page(num_page)
	min_idx = 0 if (num_page - interval < 0) else num_page - interval
	max_idx =  num_page + interval if (num_page + interval < paginator.num_pages) else paginator.num_pages
	page_range = paginator.page_range[min_idx:max_idx]
	return paginated, page_range


def hot(request, page_num=1):
	questionsObjs = Question.objects.list_hot()
	questions, page_range = paginate(questionsObjs, 5, page_num, 5)
	return render(request, 'hot.html', {'questions': questions, 'page_range': page_range, 'paginator_url': 'hot-url'}) 

def tag(request, tag_name, page_num=1):
	try:
		tag = Tag.objects.get_by_title(tag_name)
	except Tag.DoesNotExist:
		raise Http404()
	questionsObjs = Question.objects.list_tag(tag)
	questions, page_range = paginate(questionsObjs, 5, page_num, 5)
	return render(request, 'tag.html', {'questions': questions, 'page_range': page_range, 'paginator_url': 'tag-url', 'tag': tag}) 

def question(request, question_number, page_num=1):
	try:
		q = Question.objects.get_single(int(question_number))
		answers_list = Answer.objects.by_id(q.id)
		answers, page_range = paginate(answers_list, 6, page_num, 5)
		if request.method == "POST":
			form = AnswerForm(request.POST)
			if form.is_valid():
				answer, page = form.save(request, q)
				return HttpResponseRedirect('/question/' + str(q.id) + '/' + str(page) +  '/#a_' + str(answer.id))
		else:
			form = AnswerForm()
	except Question.DoesNotExist:
		raise Http404()
	except ValueError:
		raise Http404()
	return render(request, 'question.html', {'question': q, 'answers': answers, 'page_range': page_range, 'form': form})

def all(request, page_num=1):
	questions = Question.objects.list_ordered_date()
	questions, page_range = paginate(questions, 5, page_num, 5)
	return render(request, 'all.html', {'questions': questions, 'page_range': page_range, 'paginator_url': 'all-url'})

@login_required(redirect_field_name='continue')
def logout(request):
	redirect = request.GET.get('continue', '/')
	auth.logout(request)
	return HttpResponseRedirect(redirect)

def signup(request):
	if request.user.is_authenticated():
		request.session['img'] = Profile.objects.filter(user_id=request.user.id)[0].get_avatar()
		return HttpResponseRedirect('/')

	if request.method == "POST":
		form = SignupForm(request.POST, request.FILES)
		if form.is_valid():
			user = form.save()
			auth.login(request, user)
			request.session['img'] = Profile.objects.filter(user_id=request.user.id)[0].get_avatar()
			return HttpResponseRedirect('/')
	else:
		request.img = None
		form = SignupForm()
	return render(request, 'signup.html', {
			'form': form,
			})

def form_login(request):
    redirect = request.GET.get('continue', '/')
    if request.user.is_authenticated():
        request.session['img'] = Profile.objects.filter(user_id=request.user.id)[0].get_avatar()
        return HttpResponseRedirect(redirect)

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            request.session['img'] = Profile.objects.filter(user_id=request.user.id)[0].get_avatar()
            return HttpResponseRedirect(redirect)
    else:
        request.img = None
        form = LoginForm()

    return render(request, 'login.html', {
            'form': form,
})

@login_required
def ask(request):
	if request.method == "POST":
		form = NewQuestionForm(request.POST)
		if form.is_valid():
			question = form.save(request.user)
			return HttpResponseRedirect('/question/' + str(question.id) + '/')
	else:
		request.img = None
		form = NewQuestionForm()

	return render(request, 'ask.html', {
			'form': form,
			})



@login_required
def settings(request):
	profile = Profile.objects.get(user_id=request.user.id)
	avatar = profile.avatar
	if request.method == "POST":
		form = SettingsForm(request.user, avatar, request.POST, request.FILES)
		if form.is_valid():
			user = form.save(request.user)
			auth.login(request, user)
			request.session['img'] = Profile.objects.filter(user_id=request.user.id)[0].get_avatar()
			return HttpResponseRedirect('/settings')
	else:
		request.img = None
		form = SettingsForm(request.user, avatar)
	return render(request, 'settings.html', {
			'form': form,
			})

@login_required()
def correct(request):
	print(request.body)
	body = request.body.decode("utf-8")
	request.POST = json.loads(body)
	a = Answer.objects.get(id=request.POST.get('aid', False))
	is_correct = request.POST.get('checked', False)
	print(is_correct)
	a.correct = is_correct
	a.save()
	return HttpResponse(
		json.dumps({"aid": request.POST['aid'], 'correct': is_correct}),
		content_type="application/json"
		)


@login_required()
def like(request):
	body = request.body.decode("utf-8")
	request.POST = json.loads(body)
	if request.POST['type'] == 'que':
		q = Question.objects.get(id=request.POST['qid'])
		p = Profile.objects.get(user_id=request.user.id)
		value = 1 if request.POST['type_like'] == 'like_question' else -1
		LikeToQuestion.objects.add_or_update(owner=p, question=q, value=value)
		return HttpResponse(
			json.dumps({"qid": request.POST['qid'], 'like': value}),
			content_type="application/json"
		)
	else:
		if request.POST['type'] == 'ans':
			
			a = Answer.objects.get(id=request.POST['aid'])
			p = Profile.objects.get(user_id=request.user.id)
			value = 1 if request.POST['type_like'] == 'like_answer' else -1
			LikeToAnswer.objects.add_or_update(owner=p, answer=a, value=value)
			return HttpResponse(
				json.dumps({"aid": request.POST['aid'], 'like': value}),
				content_type="application/json"
			)