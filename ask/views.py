#from cgi import parse_qsl
# from django import http
from django.http import HttpResponse
from  django.template import loader
from django.template import Template
from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ask.models import Question, Profile, Answer, LikeToQuestion, LikeToAnswer, Tag

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

def login(request):
	return render(request, 'login.html')

def signup(request):
	return render(request, 'signup.html') 

def ask(request):
	temp = loader.get_template('ask.html')
	return render(request, 'ask.html')

def settings(request):
	return render(request, 'settings.html')




#TODO try 
#and send url to paginator


def hot(request, page_num=1):
	return render(request, 'hot.html')

def tag(request, tag_name):
	return render(request, 'tag.html') 

def question(request, question_number):
	q = Question.objects.get_single(int(question_number))
	print(q.text)
	return render(request, 'question.html', {'question': q})

def paginate(objects, count_on_page, num_page, pages_to_show):
#	try
	interval = int(pages_to_show / 2) + 1
	paginator = Paginator(objects, count_on_page)
	min_idx = 0 if (int(num_page) - interval < 0) else int(num_page) - interval
	max_idx =  num_page + interval if (num_page + interval < paginator.num_pages) else paginator.num_pages
	paginated = paginator.page(int(num_page))
	page_range = paginator.page_range[min_idx:max_idx]
#	exept PageNotInteger:
	return paginated, page_range

def all(request, page_num):
	questions = Question.objects.all()#.append_author()#.append_answers_count()
	questions, page_range = paginate(questions, 5, int(page_num), 5)
	print(page_range)
	return render(request, 'all.html', {'questions': questions, 'page_range': page_range, 'paginator_url': 'all-url'})
















		#print(str(q.answers_count) + ' ' + str(q.likes))#owner.first_name)
	# for i in range(1,30):
	# 	questions.append({
	# 		'title': 'title ' + str(i),
	# 		'id': i,
	# 		'text': 'text' + str(i),
	# 		'tags': {'politics', 'america'},
	# })
	# 	print()








	#temp = loader.get_template('hot.html')
	#url(r'^/', views.all, name='all-url'),





	#temp = loader.get_template('question.html')


	#temp = loader.get_template('login.html')


#def paginate(request, objects, template, 
# 	      count_on_page, page_num, context_variables):#name):
# 	paginator = Paginator(objects, 5)
# 	questions = paginator.page(int(page_num))	
# 	return render(request, tamplate, context_variables) 






















	#template = 'all.html'

	#return paginat(request, objects, template, 5. page_num, 
	 #questions = ['john', 'paul', 'george', 'ringo', 'paul', 'jim', 'kim','charles']
	#tags = { 	


#render(request, 'login.html', {'post': post})#HttpResponse(temp.render(context))#, env))
#	#resp = ['login']
#	#return HttpResponse(resp)

#def login(wsgi_request):
#	resp = ['login']
#	return HttpResponse(resp)

 #item.join(' '))
        #resp.append(wsgi_request.GET.dict)
        # resp.append("aaa")
        # print (wsgi_request.GET)
    # if HttpRequest.GET
        # resp.append(HttpRequest.GET)
        # print HttpRequest.GET

    #resp_len = sum(len(line) for line in resp)
#    response('200 OK', [('Content-type', 'text/html'),
#                              ('Content-Length', str(resp_len))])

    # xrange
    #for i in range(len(resp)):
    #    resp[i] = bytes(resp[i], "utf-8")
