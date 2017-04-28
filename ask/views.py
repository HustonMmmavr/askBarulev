
from django.http import HttpResponse, Http404
from  django.template import loader
from django.template import Template
from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ask.models import Question, Profile, Answer, LikeToQuestion, LikeToAnswer, Tag
from ask.form import LoginForm, SignupForm
from ask.decorators import need_login

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

# def login(request):
# 	return render(request, 'login.html')

@need_login
def form_login(request):
    #redirect = request.GET.get('continue', '/')
    if request.user.is_authenticated():
        return HttpResponseRedirect('/all/1/')

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            print('a')
            return HttpResponseRedirect('/all/1/')
    else:
        form = LoginForm()

    return render(request, 'login.html', {
            'form': form,
})

def signup(request):
	return render(request, 'signup.html') 

def ask(request):
	temp = loader.get_template('ask.html')
	return render(request, 'ask.html')

def settings(request):
	return render(request, 'settings.html')




def paginate(objects, count_on_page, page_num, pages_to_show):
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

def question(request, question_number):
	try:
		q = Question.objects.get_single(int(question_number))
	except Question.DoesNotExist:
		raise Http404()
	except ValueError:
		raise Http404()
	return render(request, 'question.html', {'question': q})

def all(request, page_num=1):
	questions = Question.objects.list_ordered_date()
	questions, page_range = paginate(questions, 5, page_num, 5)
	return render(request, 'all.html', {'questions': questions, 'page_range': page_range, 'paginator_url': 'all-url'})