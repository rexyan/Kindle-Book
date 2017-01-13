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
from django.conf.urls import url
from django.contrib import admin
from views import index,signin,signup,upload,CheckInfo_for_DouBan,UploadFiles,AuthorDetils,AddDownNumCount,ShowBookDetils,showtype,showauthorlist,blog,images,usercenter,typedetils,Logout,UpHeadImg,Zan,PushBook,submitcomment,dianzan,first_getchat,ChatSave


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^index/$', index),
    # url(r'^signin/$', signin),
    # url(r'^signup/$', signup),
    # url(r'^addbook/$', upload),
    # url(r'^authordetils/name', AuthorDetils),
    # url(r'^bookdetils/', ShowBookDetils),
    # url(r'^type/$',showtype),
    # url(r'^authorlist/$', showauthorlist),
    # url(r'^blog/$', blog),
    # url(r'^img/$', images),
    # url(r'^user/$', usercenter),
    # url(r'^typedetils/name', typedetils),
    #
    # #ajax
    # url(r'^CheckInfo_for_DouBan/$', CheckInfo_for_DouBan),
    # url(r'^AddDownNum/$', AddDownNumCount),
    # url(r'^Logout/$', Logout),
    # url(r'^UpHeadImg/$', UpHeadImg),
    # url(r'^dianzan/$', Zan),
    # url(r'^pushbook/$', PushBook),
    # url(r'^submitcomment/$', submitcomment),
    # url(r'^commentlike/$', dianzan),
    # url(r'^first_getchat/$', first_getchat),
    # url(r'^ChatSave/$', ChatSave),
    #
    #
    # #上传文件
    # url(r'^UpMobi/$', UploadFiles),
]
