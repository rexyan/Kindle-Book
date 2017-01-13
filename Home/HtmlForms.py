#--*--coding:utf-8--*--

from django import forms

class LoginForm(forms.Form):
    UserName = forms.CharField(min_length=5,max_length=50,error_messages={
        'required': u'Name 不能为空',
        'min_length': u'Name 最少为5个字符',
        'max_length': u'Name 最多为50个字符',
    },
    widget=forms.TextInput(attrs={
        'class':'form-control rounded input-lg text-center no-border',
        'placeholder':'Name'
    }))

    PassWord = forms.CharField(min_length=8,max_length=50,error_messages={
        'required': u'Password 不能为空',
        'min_length': u'Password 最少为8个字符',
        'max_length': u'Password 最多为50个字符',
    },
        widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded input-lg text-center no-border',
        'placeholder': 'Password'
    }))

    RePassWord = forms.CharField(min_length=8,widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded input-lg text-center no-border',
        'placeholder': 'Repeat Password '
    }))

    Email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control rounded input-lg text-center no-border',
        'placeholder': 'Email'
    }))


class UploadForm(forms.Form):
    FileAdd = forms.FileField(widget=forms.FileInput(attrs={
        'class':"btn btn-default btn-block"
    }))

class UserImgUpload(forms.Form):
    FileAdd = forms.FileField(widget=forms.FileInput(attrs={
        'class':"id_FileAdd btn btn-default btn-block"
    }))