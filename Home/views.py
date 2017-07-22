# --*--coding:utf-8--*--
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from Home import HtmlForms
from Home import models
import urllib2
import urllib
import json
from book import settings
import time
import os
from book import MySQLDB_Config
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import json
from django.core import serializers
import random
from  django.http import response

# Create your views here.

#首页
def index(request):
    #查询书籍信息,采用sql方式两表联查
    sql='select  a.zan,a.ImgAdd,a.BookID,a.BookName,a.BookAuthor,a.DownNum,a.PushNum,a.rating,b.FileName from home_bookinfo a,home_uploadfile b where a.BookID = b.BookID  order by a.DownNum DESC limit 18;'
    row=MySQLDB_Config.connection(1,sql)

    #查询热门作家
    BookAuthor=models.BookInfo.objects.all().order_by('rating')[0:5].values('BookAuthor','author_intro','BookID')

    #获取热门类型
    sql='select booktype,count(*) from home_booktype group by booktype order by count(*) desc limit 20 ;'
    row11 = MySQLDB_Config.connection(1, sql)
    for x in range(len(row11)):
        if   random.randint(0,3) <= x <= random.randint(0,3):
            list(row11)[x]['color']='default'
        elif random.randint(3,6) <= x <= random.randint(3,6):
            list(row11)[x]['color']='primary'
        elif random.randint(6,10) <= x <= random.randint(6,10):
            list(row11)[x]['color']='success'
        elif random.randint(10,12) <= x <= random.randint(10,12):
            list(row11)[x]['color']='info'
        elif random.randint(12,15) <= x <= random.randint(12,15):
            list(row11)[x]['color']='warning'
        elif random.randint(15,17) <= x <= random.randint(15,17):
            list(row11)[x]['color']='danger'
        elif random.randint(17,20) <= x <= random.randint(17,20):
            list(row11)[x]['color']='dark'

    #判断用户是否登录
    UserName=""
    img=""
    LikeObj=""
    islogin=request.session.get('user', default=None)
    if islogin!=None:
        LoginStatus=1
        # 获取用户头像
        UserObj = models.UserInfo.objects.filter(Email=islogin).values('HeadImg','UserName')
        UserName=UserObj[0]['UserName']
        img = UserObj[0]['HeadImg']
        if img=="":
            img = 'user_default.jpg'
        else:
            img = UserObj[0]['HeadImg']

        #获取用户点赞信息
        LikeObj=models.Like.objects.filter(User=islogin).values('BookId')
    else:
        LoginStatus=0
    return render_to_response('index.html',{'data_obj':row,'BookAuthor':BookAuthor,'type':row11,'LoginStatus':LoginStatus,'User':UserName,'HeadImg':img,'LikeBookID':LikeObj,'UserName':UserName})

#登录
def signin(request):
    Status=""
    LoginFormClass = HtmlForms.LoginForm()
    if request.method=="GET":
        return  render_to_response('signin.html',{'form': LoginFormClass,'Status':3})
    else:
        Email=request.POST.get('Email')
        PassWord=request.POST.get('PassWord')
        UserInfoObject = models.UserInfo.objects.filter(PassWord=PassWord,Email=Email).count()
        if UserInfoObject==1:
            Status=1
            request.session['user']=Email  #用户登录session
            return HttpResponseRedirect('/index/?message=true')
        else:
            Status=0
            return render_to_response('signin.html',{'form': LoginFormClass,'Status':Status})

#注册
def signup(request):
    Error_Message=""
    LoginFormClass=HtmlForms.LoginForm()
    if request.method=="GET":
        return  render_to_response('signup.html',{'form':LoginFormClass})
    else:
       checkform=HtmlForms.LoginForm(request.POST)
       if checkform.is_valid():
           data=checkform.cleaned_data
           if data['PassWord']!=data['RePassWord']:
               Error_Message = '输入密码不一致'
           else:
               #写入数据库
               try:
                   UserInfoObject = models.UserInfo(UserName=data['UserName'], PassWord=data['PassWord'],Email=data['Email'])
                   UserInfoObject.save()
               except  Exception,e:
                   Error_Message=e
       else:
           Error_Message= str(checkform.errors.as_text().encode('utf-8')).split('*')[2]
    return render_to_response('signup.html', {'form': LoginFormClass,'Error':Error_Message})


#上传页面
def upload(request):
    UploadFormObj=HtmlForms.UploadForm
    # 判断用户是否登录
    UserName = ""
    img = ""
    islogin = request.session.get('user', default=None)
    if islogin != None:
        LoginStatus = 1
        # 获取用户头像
        UserObj = models.UserInfo.objects.filter(Email=islogin).values('HeadImg','UserName')
        img = UserObj[0]['HeadImg']
        UserName=UserObj[0]['UserName']
        if img == "":
            img = 'user_default.jpg'
        else:
            img = UserObj[0]['HeadImg']
    else:
        LoginStatus = 0
    return render_to_response('upload.html',{'obj':UploadFormObj,'User':UserName,'HeadImg':img})


#获取豆瓣API数据
def CheckInfo_for_DouBan(request):
    if request.method=="POST":
        data=request.POST.get('data')
        data = urllib2.urlopen('https://api.douban.com/v2/book/'+data).read()
        tmp=json.loads(data)
        author=  tmp['author'][0]          #作者
        pubdate=  tmp['pubdate']           # 出版时间
        catalog=  tmp['catalog']           # 序言
        pages=  tmp['pages']               # 页数

        images=  tmp['images']['large']    # 图片
        img = (images).encode('utf-8').split('/')
        imagename = img[len(img) - 1]

        publisher=  tmp['publisher']       # 出版社
        id=  tmp['id']                     # id
        author_intro=  tmp['author_intro'] # 作者介绍
        summary=  tmp['summary']           # 书籍介绍
        title=  tmp['title']               # 名称
        rating=tmp['rating']['average']    #评分

        tp=''
        for x in range(len(tmp['tags'])):  # 类别
            tp+=tmp['tags'][x]['name']+','
        BookTypeId=tp

        try:
            translator=tmp['translator'][0]#译者
        except  Exception:
            translator=''
        subtitle=tmp['subtitle']           #副标题
        isbn13=tmp['isbn13']               #ISBN
        price=tmp['price']

        dic={'author':author,
             'pubdate':pubdate,
             'catalog':catalog,
             'pages':pages,
             'images':imagename,
             'publisher':publisher,
             'id':id,
             'author_intro':author_intro,
             'summary':summary,
             'title':title,
             'rating':rating,
             'translator':translator,
             'subtitle':subtitle,
             'isbn13':isbn13,
             'price':price,
             'BookTypeId':tp
             }
        request.session['dic'] = dic

        #下载图片到本地
        img=(images).encode('utf-8').split('/')
        imagename=img[len(img)-1]
        urllib.urlretrieve(images,filename='./static/images/mpic/'+imagename)

        return HttpResponse(author+','+images+','+title+','+pages+','+price+','+pubdate+','+rating+','+translator+","+subtitle+","+isbn13)
    else:
        return HttpResponse('0')


#上传mobi类似文件,保存图书信息
def UploadFiles(request):
    UploadFormObj = HtmlForms.UploadForm
    if request.method == "POST":
        uf = HtmlForms.UploadForm(request.POST, request.FILES)
        if uf.is_valid():
           infor = request.session.get('dic', default=None)
           if infor ==None:
               return HttpResponse('0')  #没有通过上面的API调用数据，或者调用失败
           else:
                # 保存书籍信息到书籍信息表
                BookInfoObj=models.BookInfo(
                    BookID=infor['id'],
                    BookName = infor['title'], # 书名,
                    BookAuthor =infor['author'],   # 作者,
                    BookIntroduction =infor['summary']  ,# 简介
                    ImgAdd = infor['images'], # 图片名称
                    BookPublishTime = infor['pubdate'], # 图书出版时间
                    catalog=infor['catalog'], #序言
                    pages=infor['pages'], #页数
                    publisher=infor['publisher'], #出版社
                    author_intro=infor['author_intro'], #作者简介
                    rating=infor['rating'], #评分，
                    price=str(infor['price'].encode('utf-8')).split('元')[0]
                )
                BookInfoObj.save()

           # 保存上传的文件信息
           FileObj=uf.cleaned_data
           name= str(time.time())+str(FileObj['FileAdd'])
           obj=models.UploadFile(BookId=infor['id'],UpUser=request.session.get('user', default="Rex"),FileName=name,FileAdd=name)  #文件上传
           obj.save()

           #保存书籍类型：
           type1=str(infor['BookTypeId'].encode('utf-8')).split(',')
           for x in type1:
               if x !=None and len(x)!=0:
                   Tobj=models.BookType(BookId=int(infor['id']),BookType=x,TypeImage='')
                   Tobj.save()

           #更新用户积分:
           jifen= int(str(infor['price'].encode('utf-8')).split('.')[0])/10
           UserObj=models.UserInfo.objects.get(Email=request.session.get('user'))
           UserObj.Integral+=jifen
           UserObj.save()

           return render_to_response('upload.html', {'obj': UploadFormObj,'status':'1','jifen':jifen})
        else:
           return render_to_response('upload.html', {'obj': UploadFormObj,'status':'0'})
    else:
        return render_to_response('upload.html', {'obj': UploadFormObj, 'status': '0'})

#作者详情页面
def AuthorDetils(request, param):
    '''
    :param request:
    :param param: 书籍ID或者all，当为书籍ID时，应该根据ID获取作者
    :return:
    '''
    if param != 'all':
        sql = 'select BookAuthor from home_bookinfo where BookID="%s"' % (param)
        row = MySQLDB_Config.connection(1, sql)
        Author = row[0]['BookAuthor']
        # 查询热门作品书籍信息,采用sql方式两表联查
        sql = 'select  a.ImgAdd,a.BookID,a.BookName,a.BookAuthor,a.DownNum,a.PushNum,a.rating,a.BookIntroduction,b.FileName from home_bookinfo a,home_uploadfile b where a.BookID = b.BookID and a.BookAuthor="%s" order by a.DownNum DESC  limit 6 ;'%(Author)
        row = MySQLDB_Config.connection(1, sql)

        # 作品列表,分页
        sql = 'select COUNT(a.BookID) from home_bookinfo a,home_uploadfile b where a.BookID = b.BookID and a.BookAuthor="%s";'%(Author)
        Max_Num=MySQLDB_Config.connection(1, sql)[0]['COUNT(a.BookID)']
        pagenum = 12
        Max_Page_Num,yu =divmod(Max_Num,pagenum)
        if yu!=0:
            Max_Page_Num+=1
        try:
            page = int((request.path_info).encode('utf-8').split('/')[5])
        except Exception,e:
            page = 1

        if page == None:
            page = 1
        elif page < 0:
            page = 1
        elif page>Max_Page_Num:
            page=Max_Page_Num

        startpage =(page - 1) * pagenum
        endpage = page * pagenum

        page_html = []
        for x in range(Max_Page_Num):
            str = ('/authordetils/name/%s/%d/' % (param,int(x)+1))
            page_html.append(str)

        sql = 'select  a.ImgAdd,a.BookID,a.BookName,a.BookAuthor,a.DownNum,a.PushNum,a.rating,a.BookIntroduction,b.FileName from home_bookinfo a,home_uploadfile b where a.BookID = b.BookID and a.BookAuthor="%s" order by a.PushNum DESC  limit %d,%d  ;' % (Author,startpage,endpage)
        row1 = MySQLDB_Config.connection(1, sql)

        # 判断用户是否登录
        UserName = ""
        img = ""
        LikeObj = ""
        islogin = request.session.get('user', default=None)
        if islogin != None:
            LoginStatus = 1
            # 获取用户头像
            UserObj = models.UserInfo.objects.filter(Email=islogin).values('HeadImg', 'UserName')
            img = UserObj[0]['HeadImg']
            UserName = UserObj[0]['UserName']
            if img == "":
                img = 'user_default.jpg'
            else:
                img = UserObj[0]['HeadImg']

            # 获取用户点赞信息
            LikeObj = models.Like.objects.filter(User=islogin).values('BookId')
        else:
            LoginStatus = 0
        return render_to_response('author.html', {'data': row, 'data1': row1, 'page_num': page_html,'LoginStatus':LoginStatus,'HeadImg':img,'User':UserName})
    else:
        return render_to_response('author.html')


#ajax,下载次数增加
def AddDownNumCount(request):
    islogin = request.session.get('user', default=None)

    if islogin !=None:
         if request.method == "POST":
            BookId = request.POST.get('data')
            #获取书籍的价格，计算积分
            BookInfoObj = models.BookInfo.objects.get(BookID=BookId)
            jifen = int(str(BookInfoObj.price).split('.')[0]) / 10
            UserObj = models.UserInfo.objects.get(Email=request.session.get('user'))
            if UserObj.Integral-jifen>0:
                UserObj.Integral -= jifen
                UserObj.save()

                #下载次数统计
                BookInfoObj = models.BookInfo.objects.get(BookID=BookId)
                BookInfoObj.DownNum += 1
                BookInfoObj.save()
                DownNum = BookInfoObj = models.BookInfo.objects.filter(BookID=BookId).values('DownNum')[0]['DownNum']

                #获取下载文件名
                FileDownObj=models.UploadFile.objects.filter(BookId=BookId).values('FileName')
                filename=FileDownObj[0]['FileName']
                return HttpResponse(str(DownNum)+','+filename)
            else:
                return HttpResponse('DeficiencyOfIntegral')
    else:
        return HttpResponse('LoginFaile')

#书籍详情页面
def ShowBookDetils(request, param):
    BookID = param
    # 查询书籍信息,采用sql方式两表联查
    sql = 'select  a.BookID,a.publisher,a.BookPublishTime,a.ImgAdd,a.BookName,a.BookAuthor,a.DownNum,a.PushNum,a.rating,b.UpUser from home_bookinfo a,home_uploadfile b where a.BookID = b.BookID AND a.BookID=%d ;'%(int(BookID))
    row = MySQLDB_Config.connection(1, sql)

    # 查询评论
    ComObj = models.Comment.objects.filter(BookId=BookID).order_by('-Zan')

    # 判断用户是否登录
    UserName = ""
    img = ""
    islogin = request.session.get('user', default=None)
    if islogin != None:
        LoginStatus = 1
        # 获取用户头像
        UserObj = models.UserInfo.objects.filter(Email=islogin).values('HeadImg', 'UserName')
        img = UserObj[0]['HeadImg']
        UserName = UserObj[0]['UserName']
        if img == "":
            img = 'user_default.jpg'
        else:
            img = UserObj[0]['HeadImg']
    else:
        LoginStatus = 0
    return  render_to_response('invoice.html',{'data':row,'comment':ComObj,'LoginStatus':LoginStatus,'HeadImg':img,'User':UserName})


#类型页面
def showtype(request):
    sql = 'select booktype,count(*) as cishu from home_booktype group by booktype order by count(*) desc;'
    row11 = MySQLDB_Config.connection(1, sql)

    # 判断用户是否登录
    UserName = ""
    img = ""
    islogin = request.session.get('user', default=None)
    if islogin != None:
        LoginStatus = 1
        # 获取用户头像
        UserObj = models.UserInfo.objects.filter(Email=islogin).values('HeadImg', 'UserName')
        img = UserObj[0]['HeadImg']
        UserName = UserObj[0]['UserName']
        if img == "":
            img = 'user_default.jpg'
        else:
            img = UserObj[0]['HeadImg']
    else:
        LoginStatus = 0
    return render_to_response('type.html',{'type':row11,'LoginStatus':LoginStatus,'HeadImg':img,'User':UserName})


#作家页面
def showauthorlist(request):
    sql = 'select bookauthor,count(*) as cishu from home_bookinfo group by bookauthor order by count(*) desc;'
    result = MySQLDB_Config.connection(1, sql)
    for x in range(len(result)):

        if random.randint(0, 3) <= x <= random.randint(0, 3):
            list(result)[x]['color'] = 'default'
        elif random.randint(3, 6) <= x <= random.randint(3, 6):
            list(result)[x]['color'] = 'primary'
        elif random.randint(6, 10) <= x <= random.randint(6, 10):
            list(result)[x]['color'] = 'success'
        elif random.randint(10, 12) <= x <= random.randint(10, 12):
            list(result)[x]['color'] = 'info'
        elif random.randint(12, 15) <= x <= random.randint(12, 15):
            list(result)[x]['color'] = 'warning'
        elif random.randint(15, 17) <= x <= random.randint(15, 17):
            list(result)[x]['color'] = 'danger'
        elif random.randint(17, 20) <= x <= random.randint(17, 20):
            list(result)[x]['color'] = 'dark'

        # 判断用户是否登录
        UserName=""
        img = ""
        islogin = request.session.get('user', default=None)
        if islogin != None:
            LoginStatus = 1
            # 获取用户头像
            UserObj = models.UserInfo.objects.filter(Email=islogin).values('HeadImg', 'UserName')
            img = UserObj[0]['HeadImg']
            UserName = UserObj[0]['UserName']
            if img == "":
                img = 'user_default.jpg'
            else:
                img = UserObj[0]['HeadImg']
        else:
            LoginStatus = 0
    return render_to_response('authorlist.html',{'author':result,'LoginStatus':LoginStatus,'HeadImg':img,'User':UserName})


#博客页面
def blog(request):
    UserName=""
    img = ""
    islogin = request.session.get('user', default=None)
    if islogin != None:
        LoginStatus = 1
        # 获取用户头像
        UserObj = models.UserInfo.objects.filter(Email=islogin).values('HeadImg', 'UserName')
        img = UserObj[0]['HeadImg']
        UserName = UserObj[0]['UserName']

        img = UserObj[0]['HeadImg']
        if img == "":
            img = 'user_default.jpg'
        else:
            img = UserObj[0]['HeadImg']

        # 获取用户点赞信息
        LikeObj = models.Like.objects.filter(User=islogin).values('BookId')
    else:
        LoginStatus = 0
    return  render_to_response('blog.html',{'LoginStatus':LoginStatus,'HeadImg':img,'User':UserName})

#图片页面
def images(request):
    img = ""
    UserName=""
    islogin = request.session.get('user', default=None)
    if islogin != None:
        LoginStatus = 1
        # 获取用户头像
        UserObj = models.UserInfo.objects.filter(Email=islogin).values('HeadImg', 'UserName')
        img = UserObj[0]['HeadImg']
        UserName = UserObj[0]['UserName']

        if img == "":
            img = 'user_default.jpg'
        else:
            img = UserObj[0]['HeadImg']

        # 获取用户点赞信息
        LikeObj = models.Like.objects.filter(User=islogin).values('BookId')
    else:
        LoginStatus = 0
    return render_to_response('images.html',{'LoginStatus':LoginStatus,'HeadImg':img,'User':UserName})


#个人中心页面
def usercenter(request):
    islogin = request.session.get('user', default=None)
    if islogin != None:
        UserObj=models.UserInfo.objects.filter(Email=islogin)
        FileObj=models.UploadFile.objects.filter(UpUser=islogin).count()
        # 获取用户头像
        UserObj = models.UserInfo.objects.filter(Email=islogin).values('HeadImg', 'UserName', 'Integral')
        UserName = UserObj[0]['UserName']
        img = UserObj[0]['HeadImg']
        if img == "":
            img = 'user_default.jpg'
        else:
            img = UserObj[0]['HeadImg']
        return  render_to_response('user.html',{'data':UserObj,'filecount':FileObj,'UserimgObj':HtmlForms.UserImgUpload,'HeadImg':img})
    else:
        return HttpResponseRedirect('/signin')

#类别详情页
def typedetils(request, param):
    TypeName = param
    sql = 'select  a.ImgAdd,a.BookID,a.BookName,a.BookAuthor,a.DownNum,a.PushNum,a.rating,b.FileName from home_bookinfo a,home_uploadfile b,home_booktype c where a.BookID = b.BookID and b.BookID=c.BookId and c.BookType="%s" order by a.DownNum DESC ;'%(TypeName)
    row11 = MySQLDB_Config.connection(1, sql)

    # 判断用户是否登录
    UserName = ""
    img = ""
    LikeObj = ""
    islogin = request.session.get('user', default=None)
    if islogin != None:
        LoginStatus = 1
        # 获取用户头像
        UserObj = models.UserInfo.objects.filter(Email=islogin).values('HeadImg', 'UserName')
        img = UserObj[0]['HeadImg']
        UserName = UserObj[0]['UserName']
        if img == "":
            img = 'user_default.jpg'
        else:
            img = UserObj[0]['HeadImg']

        # 获取用户点赞信息
        LikeObj = models.Like.objects.filter(User=islogin).values('BookId')
    else:
        LoginStatus = 0
    return render_to_response('typedetils.html',{'data1':row11,'type':TypeName,'LoginStatus':LoginStatus,'HeadImg':img,'LikeBookID':LikeObj,'User':UserName})


#退出
def Logout(request):
    islogin = request.session.get('user', default=None)
    if islogin != None:
        del request.session['user']
        return HttpResponse('1')
    return HttpResponse('0')


#用户中心修改头像
def UpHeadImg(request):
    uf = HtmlForms.UserImgUpload(request.POST, request.FILES)
    if uf.is_valid():
        uploadfile = uf.cleaned_data['FileAdd']
    return HttpResponse('1')

#书籍点赞
def Zan(request):
    res={'status':"",'count':""}
    islogin = request.session.get('user', default=None)
    if islogin != None:
        if request.method=="POST":
            id = request.POST.get('data')
            LikeObj=models.Like.objects.filter(BookId=id,User=islogin)
            if len(LikeObj)==0:  #用户没有点过赞
                #保存信息到点赞表
                LikeObj1 = models.Like(BookId=id,User=islogin)
                LikeObj1.save()

                #更新bookinfo点赞数量
                bookinfoobj = models.BookInfo.objects.get(BookID=id)
                zancount = bookinfoobj.zan + 1
                bookinfoobj.zan = zancount
                bookinfoobj.save()
                res['status'] = '点赞'
                res['count'] = zancount
                return HttpResponse(json.dumps(res))
            else:               #取消点赞
                # 删除信息从点赞表
                LikeObj1 = models.Like(BookId=id, User=islogin).delete()
                # 更新bookinfo点赞数量
                bookinfoobj = models.BookInfo.objects.get(BookID=id)
                zancount = bookinfoobj.zan - 1
                bookinfoobj.zan = zancount
                bookinfoobj.save()
                res['status'] = '取消点赞'
                res['count'] = zancount
                return HttpResponse(json.dumps(res))
        else:
           res['status'] = '点赞失败'
           return HttpResponse(json.dumps(res))
    else:
        res['status']='未登录'
        return HttpResponse(json.dumps(res))

#书籍推送
def PushBook(request):
    res = {'status': "",'pushnum':""}
    if request.method=="POST":
        islogin = request.session.get('user', default=None)
        if islogin != None:
            id = request.POST.get('data')
            PushObj = models.PushBook.objects.filter(BookId=id,SendUser=islogin).count()
            if PushObj>=1:
                #用户推送过该书
                res['status'] = '在列表中'
                return HttpResponse(json.dumps(res))
            else:
                #用户没有推送过该书
                PushObj=models.PushBook(BookId=id,SendUser=islogin)
                PushObj.save()

                #推送数+1
                booobj=models.BookInfo.objects.get(BookID=id)
                tmp=booobj.PushNum+1
                booobj.PushNum =tmp
                booobj.save()
                res['status'] = '推送'
                res['pushnum'] =tmp
                return HttpResponse(json.dumps(res))
        else:
            res['status'] = '未登录'
            return HttpResponse(json.dumps(res))
    else:
        res['status'] = '推送异常'
        return HttpResponse(json.dumps(res))

#书籍详情页面评论
def submitcomment(request):
    res = {'status': ''}
    if request.method=="POST":
        data=request.POST.get('data')
        id=request.POST.get('id')
        islogin = request.session.get('user', default=None)
        if islogin != None:
            #新增加评论
            ComObj=models.Comment(BookId=id,User=islogin,Content=data)
            ComObj.save()
            res['status'] = '评论成功'
            return HttpResponse(json.dumps(res))
        else:
            res['status'] = '未登录'
            return HttpResponse(json.dumps(res))
    else:
        res['status']='未知错误'
        return HttpResponse(json.dumps(res))

#评论点赞
def dianzan(request):
    res = {'status': '','zan':""}
    if request.method == "POST":
        id = request.POST.get('id')
        islogin = request.session.get('user', default=None)
        if islogin != None:
            # 评论点赞
            ComObj=models.Comment.objects.get(id=id)
            tmp=ComObj.Zan+1
            ComObj.Zan=tmp
            ComObj.save()
            res['status'] = '点赞成功'
            res['zan'] =tmp
            return HttpResponse(json.dumps(res))
        else:
            res['status'] = '未登录'
            return HttpResponse(json.dumps(res))
    else:
        res['status'] = '未知错误'
        return HttpResponse(json.dumps(res))

#聊天室获取数据
def first_getchat(request):
    max=[]
    res = {'data': '', 'MaXId': ""}
    if request.method == "POST":
        id = request.POST.get('tag')
        global MaXId
        if id=='1':  #第一次进入页面
            ChatObj=models.Chat.objects.all().order_by('-id')[0:5]
            res=serializers.serialize('json',ChatObj)
            # 取最大ID
            MaXId = models.Chat.objects.latest('id')
            MaXId = MaXId.id
            return HttpResponse(res)
        elif id=='2':
            if not 'MaXId' in dir() :  #如果没有MaXId则查询一下
                MaXId = models.Chat.objects.latest('id')
                MaXId = MaXId.id
            ChatObj = models.Chat.objects.filter(id__gt=MaXId).order_by('-id')
            res = serializers.serialize('json', ChatObj)
            # 取最大ID
            MaXId = models.Chat.objects.latest('id')
            MaXId = MaXId.id
            return HttpResponse(res)
    else:
        return HttpResponse('错误')

#保存聊天
def ChatSave(request):
    res = {'User': '', 'time': "", "content": ""}
    islogin = request.session.get('user', default=None)
    if islogin != None:
        # 查询用户名
        UserObj = models.UserInfo.objects.filter(Email=islogin).values('UserName')
        UserName = UserObj[0]['UserName']

        content = request.POST.get('content')
        CreTime = time.strftime('%Y-%m-%d %H:%m')
        ChatObj = models.Chat(User=UserName, Content=content, CommentTime=CreTime)
        ChatObj.save()
        res['User']=ChatObj.User
        res['time']=ChatObj.CommentTime
        res['content']=ChatObj.Content
        return HttpResponse(json.dumps(res))
    else:
        return HttpResponse('未登录')