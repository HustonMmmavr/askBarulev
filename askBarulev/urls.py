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
from django.conf.urls.static import static

urlpatterns = [
    url(r'^correct$', views.correct, name='correct'),
    url(r'^admin/', admin.site.urls),
    url(r'^main/', views.main),
    url(r'^login/', views.form_login, name='login-url'),
    url(r'^logout/', views.logout, name='log-out'),
    url(r'^hot/(?P<page_num>\w+)/', views.hot, name='hot-url'),
    url(r'^hot/', views.hot, name='hot-url'),
    url(r'^tag/(?P<tag_name>\w+)/(?P<page_num>\w+)/', views.tag, name='tag-url'),
    url(r'^tag/(?P<tag_name>\w+)/', views.tag, name='tag-url'),
    url(r'^signup/', views.signup, name='signup-url'),
    url(r'^ask/', views.ask, name='ask-url'),
    url(r'^settings/', views.settings, name='settings-url'),
    url(r'^like$', views.like, name='like'),
    url(r'^question/(?P<question_number>\w+)/', views.question, name='question-url'),
    url(r'^all/(?P<page_num>\w+)/', views.all, name='all-url'),
    url(r'^all/', views.all, name='all-url'),
    url(r'^(?P<page_num>\w+)/', views.all, name='all-url'),
    url(r'^$', views.all,  name='all-url'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

