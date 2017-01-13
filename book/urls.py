#--*--coding:utf-8--*--

"""book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from Home import views


urlpatterns = [
    url(r'^Admin_Login/', admin.site.urls),
    # url(r'^Home/', include('Home.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.index),
    url(r'^signin/$', views.signin),
    url(r'^signup/$', views.signup),
    url(r'^addbook/$', views.upload),
    url(r'^authordetils/name', views.AuthorDetils),
    url(r'^bookdetils/', views.ShowBookDetils),
    url(r'^type/$', views.showtype),
    url(r'^authorlist/$', views.showauthorlist),
    url(r'^blog/$', views.blog),
    url(r'^img/$', views.images),
    url(r'^user/$', views.usercenter),
    url(r'^typedetils/name', views.typedetils),

    # ajax
    url(r'^CheckInfo_for_DouBan/$', views.CheckInfo_for_DouBan),
    url(r'^AddDownNum/$', views.AddDownNumCount),
    url(r'^Logout/$', views.Logout),
    url(r'^UpHeadImg/$', views.UpHeadImg),
    url(r'^dianzan/$', views.Zan),
    url(r'^pushbook/$', views.PushBook),
    url(r'^submitcomment/$', views.submitcomment),
    url(r'^commentlike/$', views.dianzan),
    url(r'^first_getchat/$', views.first_getchat),
    url(r'^ChatSave/$', views.ChatSave),
    url(r'^UpMobi/$', views.UploadFiles),
]
