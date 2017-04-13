"""askBarulev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from ask import views
#from . import contr
from django.conf.urls.static import static

#TODO Tag num..
#for default ex no page in reques
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^main/', views.main),
    #url(r'^contr/(?P<num>\w+)/', contr.app),
    url(r'^hot/', views.hot, name='hot-url'),
    url(r'^tag/(?P<tag_name>\w+)/', views.tag, name='tag-url'),
    url(r'^login/', views.login, name='login-url'),
    url(r'^signup/', views.signup, name='signup-url'),
    url(r'^ask/', views.ask, name='ask-url'),
    url(r'^settings/', views.settings, name='settings-url'),
    url(r'^question/(?P<question_number>[0-9]+)/', views.question, name='question-url'),
    url(r'^all/(?P<page_num>[0-9]+)/', views.all, name='all-url'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

