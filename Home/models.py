#--*--coding:utf-8--*--
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#用户信息
class UserInfo(models.Model):
     UserName=models.CharField(max_length=50)
     PassWord=models.CharField(max_length=50)
     Email=models.EmailField()
     LoginTime=models.DateTimeField(auto_now=True)
     RegisterTime=models.DateTimeField(auto_now_add=True)
     Integral=models.IntegerField(default=0,null=True)
     HeadImg=models.FileField(null=True)
     Other_Info=models.TextField(null=True)

     #书籍信息表
class BookInfo(models.Model):
     BookID=models.IntegerField(primary_key = True,unique=True) #ID
     BookName=models.CharField(max_length=100)           #书名
     BookAuthor=models.CharField(max_length=100)         #作者
     BookIntroduction=models.CharField(max_length=2000) #图书简介
     DownNum=models.IntegerField(default=0)        #下载数
     PushNum=models.IntegerField(default=0)        #推送数
     ImgAdd=models.CharField(max_length=200)        #图片名称
     BookPublishTime=models.CharField(null=True,max_length=50)  #图书出版时间

     catalog=models.CharField(max_length=4000,null=True)  #序言
     pages=models.CharField(max_length=50,null=True)  #页数
     publisher=models.CharField(max_length=100,null=True) #出版社
     author_intro=models.CharField(max_length=4000,null=True)  #作者简介
     rating=models.CharField(max_length=3)  #评分
     price = models.CharField(max_length=10,null=True)  # 评分
     zan=models.IntegerField(default=0) #点赞


#电子书籍存放
class UploadFile(models.Model):
     BookId = models.IntegerField(primary_key = True,unique=True) #书籍ID
     UpUser=models.CharField(max_length=50)  #上传用户
     FileName=models.CharField(max_length=300)  #文件名称
     FileAdd=models.FileField(upload_to='./static/book')  #上传文件路径


#书籍类别
class BookType(models.Model):
     BookId = models.IntegerField()  # 书籍ID
     BookType=models.CharField(max_length=50,null=True)   #书籍类别
     TypeImage=models.CharField(max_length=50,null=True)   #书籍图片地址

#推送
class PushBook(models.Model):
     BookId = models.IntegerField()  # 推送书籍ID
     SendUser = models.CharField(max_length=50)  #用户
     Status=models.BooleanField(default=False)  #推送状态

#点赞
class Like(models.Model):
     BookId = models.IntegerField(primary_key=True, unique=True)  # 书籍ID
     User = models.CharField(max_length=50)  #点赞用户

#评论
class Comment(models.Model):
     BookId = models.IntegerField(null=True)  # 评论书籍ID
     User = models.CharField(max_length=50)     #评论用户
     Content=models.CharField(max_length=7000)  #评论内容
     CommentTime = models.DateTimeField(auto_now_add=True)#评论时间
     Zan=models.IntegerField(default=0)  #赞同的回答

#聊天室
class Chat(models.Model):
     User = models.CharField(max_length=50)  #聊天用户
     Content = models.CharField(max_length=7000)  # 聊天内容
     CommentTime = models.CharField(max_length=50,null=True)  #聊天时间