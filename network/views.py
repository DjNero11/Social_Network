from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
import json

from .models import User, Post, Follow_data


def index(request):
    if request.method == "POST":
        post_text = request.POST["newpost"]
        user = request.user

        p = Post.objects.create(user=user, text=post_text)
        p.save
        return HttpResponseRedirect(reverse("index"))
    else:
        posts_text = Post.objects.all().order_by('-date_time')
        paginator = Paginator(posts_text, 10) 
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
           "page_obj": page_obj
        })


def user_profile_view(request, user_id):
    if request.method == "POST":
        folow_value = request.POST.get("follow_button_profile")
        profile_id_follow = request.POST.get("follow_button_profile_id")
        user = request.user

        if folow_value == "Unfollow":
            try:
                #remove from follow
                follows_data = Follow_data.objects.get(user=user)
                user_unfollow = User.objects.get(id=profile_id_follow)
                follows_data.follows.remove(user_unfollow)
               
                #remove followers from follow user
                follower_data = Follow_data.objects.get(user=user_id)
                follower_data.followers.remove(user)

                #https://stackoverflow.com/questions/42311548/pass-argument-to-view-with-reverse-django
                return HttpResponseRedirect(reverse("user_profile", args=[user_id]))
            except:
                return HttpResponse("No such user in your follows.")
        else:
            try:
                #https://www.queworx.com/django/django-get_or_create/
                #append to user's follows
                follows_data, _ = Follow_data.objects.get_or_create(user=user)
                user_follow = User.objects.get(id=profile_id_follow)
                follows_data.follows.add(user_follow)

                #remove followers from follow user
                follower_data, _ = Follow_data.objects.get_or_create(user_id=user_id)
                follower_data.followers.add(user)

                return HttpResponseRedirect(reverse("user_profile", args=[user_id]))
            except:
                return HttpResponse("No such user to follow or other error.")
    else:
        try:
            username = User.objects.get(id=user_id).username
            profile_id = User.objects.get(id=user_id).id
        except: 
            return HttpResponse("User does not exist or other error.")
        
        user_posts = Post.objects.filter(user=user_id).order_by('-date_time')
        paginator = Paginator(user_posts, 10) 
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        follow_data = Follow_data.objects.filter(user=user_id)

        #followers count 
        if follow_data.exists():
            follow_data_i = follow_data[0]
            n_followers = follow_data_i.followers.count()
            n_follows = follow_data_i.follows.count()
        else:
            n_followers = 0
            n_follows = 0

        #folow button  
        user = request.user
        # https://stackoverflow.com/questions/4642596/how-to-check-whether-the-user-is-anonymous-or-not-in-django
        if not user.is_authenticated:
            folow_info = "Not authenticated"
        elif user.username == username:
            folow_info = "Do not show"
        elif follow_data.exists():
            follow_data_i = follow_data.first() 
            if user in follow_data_i.followers.all():
                folow_info = "Unfollow"
            else:
                folow_info = "Follow"
        else:
            folow_info = "Follow"


        return render(request, "network/user_page.html", {
        "page_obj": page_obj,
        "username": username,
        "n_follows": n_follows,
        "n_followers":n_followers,
        "folow_info":folow_info,
        "profile_id":profile_id,
        "user":user
        })

@login_required(login_url="login")
def following_views(request):
    user_signin = request.user
    follow_data = Follow_data.objects.get(user=user_signin) 
    followed_users = follow_data.follows.all()  
    # https://www.w3schools.com/django/ref_lookups_in.php
    posts = Post.objects.filter(user__in=followed_users).order_by('-date_time')  

    paginator = Paginator(posts, 10) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "page_obj": page_obj
    })

def edit_post_views(request, post_id):
    #https://www.geeksforgeeks.org/get_object_or_404-method-in-django-models/
    edited_post = get_object_or_404(Post, id=post_id)
    user_edditing = request.user
    post_owner = edited_post.user
    if user_edditing != post_owner:
        return HttpResponse("You do not have rights to edit this post.")

    if request.method == "POST":
        data = json.loads(request.body)
        new_text = data.get("newpost_text")
        edited_post.text = new_text
        edited_post.save()
        return JsonResponse({"success_message": "Post edited successfully."}, status=201)
    else:
        return JsonResponse({
            "error": "Post method request required."
        }, status=400)
    

def likes_change_API_views(request):
    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        post_id = data.get("post_id")
        post = Post.objects.get(id=post_id)
        if not user.is_authenticated:
            return JsonResponse({
                "Error": "User not signed in "
            }, status=400)
        else:
            if user in post.likes.all():
                post.likes.remove(user)
            else:
                post.likes.add(user)
            
            likes_num = post.likes.count()
            return JsonResponse({
                "Message": "Sucess",
                "likes_num": likes_num
            }, status=201)
    else:
        return JsonResponse({
            "error": "Post method request required."
        }, status=400)

    







def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
