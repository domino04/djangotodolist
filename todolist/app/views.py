from django.shortcuts import render, redirect
from .models import List, Comment
import datetime
from django.contrib.auth.models import User
from django.contrib import auth 
from django.contrib.auth.decorators import login_required 
from .utils import upload_and_save 
# Create your views here.

from todolist.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME
import boto3
from boto3.session import Session 
from datetime import datetime 

# CRUD - HOME
def home(request):
    lists = List.objects.all().order_by("duedate")
    return render(request, 'home.html', {'lists': lists})

# CRUD - CREATE
@login_required(login_url="/registration/login")
def new(request):
    if request.method == "POST":
        print(request.POST)
        file_to_upload = request.FILES.get('img')
        session = Session(
            aws_access_key_id= AWS_ACCESS_KEY_ID,
            aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
            region_name= AWS_S3_REGION_NAME
        )
        s3 = session.resource('s3')
        now = datetime.now().strftime('%Y%H%M%S')
        
        img_object = s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(
            Key = str(request.user.pk)+'/'+now+file_to_upload.name,
            Body = file_to_upload
        )
        
        s3_url = 'https:///to-do-list-danbi.s3.ap-northeast-2.amazonaws.com/'
        new_list = List.objects.create(
            title = request.POST['title'],
            content = request.POST['content'],
            duedate = request.POST['duedate'],
            author = request.user,
            img = s3_url +str(request.user.pk)+'/' + now + file_to_upload.name
        )
        # upload_and_save(request, file_to_upload, new_list)
        return redirect('detail', new_list.pk)
    return render(request, 'new.html')

# CRUD - READ
def detail(request, list_pk):
    list = List.objects.get(pk=list_pk)
    
    if request.method == "POST":
        Comment.objects.create(
            list = list,
            content = request.POST['content']
        )
        return redirect('detail', list_pk)
    return render(request, 'detail.html', {'list' : list})

# CRUD - UPDATE
def edit(request, list_pk):
    list = List.objects.get(pk=list_pk)

    if request.method =="POST":
        List.objects.filter(pk=list_pk).update(
            title = request.POST['title'],
            content = request.POST['content'],
            duedate = request.POST['duedate'],
            img = upload_and_save(request, file_to_upload)
        )
        return redirect('detail', list_pk)
    return render(request, 'edit.html', {'list' : list})

# CRUD - DELETE:
def delete(request, list_pk):
    list = List.objects.get(pk=list_pk)
    list.delete()
    return redirect('home')

def delete_comment(request, list_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('detail', post_pk)

def signup(request):
    if (request.method == "POST"):
        new_user = User.objects.create_user(
            username = request.POST['username'],
            password = request.POST['password']
        )
        return redirect('home')
    return render(request, 'registration/signup.html')

def login(request):
    if request.method == 'POST':
        found_user = auth.authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )

        if found_user is None:
            error = "아이디 또는 비밀번호가 틀렸습니다"
            return render(request, 'registration/login.html', {'error': error})

        auth.login(
            request,
            found_user,
            backend = 'django.contrib.auth.backends.ModelBackend'
        )

        return redirect(request.GET.get('next', '/'))

    return render(request, 'registration/login.html')


def logout(request):
    auth.logout(request)

    return redirect('home')

def mylist(request):
    lists = List.objects.all()
    comment = Comment.objects.all()

    return render(request, 'mylist.html', {'lists':lists, 'comment':comment})