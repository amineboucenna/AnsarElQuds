import calendar
import datetime
import random
import cv2
from django.db.models import Count, Max,Avg
from django.db import IntegrityError
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.hashers import check_password,make_password
from .models import NewsVote, User,News
from django.utils.translation import gettext as _

# Create your views here.


# Login | Register | Logout
def Login(request):
    msg = ''
    if request.method == 'POST':
        email_username = request.POST.get('email')
        password = request.POST.get('password')

        if "@" in email_username:
            try:
                user = User.objects.get(email=email_username)
            except User.DoesNotExist:
                msg = _('There is no Account assosited with this Email!')
                return render(request, 'auth/login.html', {'msg': msg})
        else:
            try:
                user = User.objects.get(username=email_username)
            except User.DoesNotExist:
                msg = _('There is no Account assosited with this Username!')
                return render(request, 'auth/login.html', {'msg': msg})
        if user.is_active:
            if check_password(password=password, encoded=user.password):
                authentification = authenticate(request, username=email_username, password=password,
                                                backend='Arabic.backends.EmailOrUsernameModelBackend')
                if authentification is not None:
                    login(request, authentification)
                    return redirect('profile')
            else:
                msg = _('Wrong Password!')
        else:
            msg = _('Your account is banned')
        return render(request, 'auth/login.html', {'msg': msg})

    return render(request, 'auth/login.html')


def Logout(request):
    logout(request)
    return redirect('profile')


def Register(request):
    msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        country = request.POST.get('country')

        try:
            User.objects.get(username=username)
            msg = _('User Already Exist!')
            return render(request, 'auth/register.html', {'msg': msg})
        except User.DoesNotExist:
            created_user = User.objects.create_user(username=username, email=email, password=password,
                                                    first_name=firstname, last_name=lastname,country=country)
            created_user.save()
            authentification = authenticate(request, username=username, password=password,
                                            backend='App.backends.EmailOrUsernameModelBackend')
            if authentification is not None:
                login(request, authentification)
                return redirect('profile')
    return render(request, 'auth/register.html', {'msg': msg})


@login_required(login_url='/sign-in/')
def Profile(request):
    username = request.user
    user = User.objects.get(email=username)
    return render(request,"profile.html",{'user':user})


@login_required(login_url='/sign-in/')
def Settings(request):
    message=''
    if request.method == 'POST':
        username = request.user.username
        email = request.POST.get('email')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        country  = request.POST.get('country')
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')



        try:    
            profile_picture = request.FILES['profile-file']
            # generate a unique name based on the original file name
            if '.jpg' in profile_picture.name :
                unique_name = f'{username}_profile.jpg'
                # set the new file name
                profile_picture.name = unique_name
            if '.png' in profile_picture.name :
                unique_name = f'{username}_profile.png'
                # set the new file name
                profile_picture.name = unique_name
            # set the new file name
            profile_picture.name = unique_name
            print('profile picture uploaded')
        except :
            profile_picture = None

        
        if check_password(password,request.user.password):
            user = User.objects.get(username=username)
            user.email = email
            user.first_name = fname
            user.last_name = lname
            user.country = country
            if profile_picture is not None:
                user.profile_picture = profile_picture
               
            try:   
                user.save()      
                if new_password != '':
                    user.password = make_password(new_password)
                    user.save()
                    logout(request)
                    authentification = authenticate(request,username=username,password=new_password,backend='Arabic.backends.EmailOrUsernameModelBackend')
                    if authentification is not None :
                        login(request,authentification)
            except IntegrityError:
                message = _("Email already associated with an account.")
                return render(request,'profile/settings.html',{'message':message})

            return redirect('profile')
            
        else :
            message = _('Sorry, the password you entered is invalid.')
            return render(request,'profile/settings.html',{'message':message})
            

    return render(request,'profile/settings.html')


from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger

import os

def NewsPage(request):
    if request.method == 'POST':
        media = request.FILES['media-input']
        title = request.POST.get('news-title')
        position = request.POST.get('position')
        user = User.objects.get(username=request.user.username)

        file_extension = os.path.splitext(media.name)[1].lower()
        if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
            media_type = 'image'
        elif file_extension == '.mp4':
            media_type = 'video'

        news = News.objects.create(
            media=media,
            posted_by=user,
            title=title,
            position=position,
            media_type=media_type
        )
        news.save()
        return redirect('news')

    # case in GET
    news_list = News.objects.all()  
    paginator = Paginator(news_list, 10)  

    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
      
        news = paginator.page(1)
    except EmptyPage:
       
        news = paginator.page(paginator.num_pages)

    return render(request, 'news.html', {'news': news})


from .models import NewsVote

def upvote_news(request, article_id):
    news = News.objects.get(id=article_id)
    user = request.user
    current_vote = NewsVote.objects.filter(user=user, news=news).first()

    if current_vote:
        if current_vote.vote_type == 'upvote':
            current_vote.vote_type = 'downvote'
            news.up_votes -= 1
            news.down_votes += 1
        else:
            current_vote.vote_type = 'upvote'
            news.up_votes += 1
            news.down_votes -= 1
        current_vote.save()
    else:
        NewsVote.objects.create(user=user, news=news, vote_type='upvote')
        news.up_votes += 1

    news.save()
    return redirect('news')

def downvote_news(request, article_id):
    news = News.objects.get(id=article_id)
    user = request.user
    current_vote = NewsVote.objects.filter(user=user, news=news).first()

    if current_vote:

        if current_vote.vote_type == 'downvote':
            current_vote.vote_type = 'upvote'
            news.up_votes += 1
            news.down_votes -= 1
        else:
            current_vote.vote_type = 'downvote'
            news.up_votes -= 1
            news.down_votes += 1
        current_vote.save()
    else:
        NewsVote.objects.create(user=user, news=news, vote_type='downvote')
        news.down_votes += 1

    news.save()
    return redirect('news')
