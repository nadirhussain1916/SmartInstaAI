import os
import requests
from django.core.files.base import ContentFile
from django.shortcuts import render
import instaloader
from .models import Instagram_User
import datetime

def instagram_user_view(request):
    user_data = None
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        if '@' in username:
            error = "Please enter a valid Instagram username, not an email address."
        else:
            loader = instaloader.Instaloader()
            try:
                profile = instaloader.Profile.from_username(loader.context, username)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
                pic_url = profile.profile_pic_url
                response = requests.get(pic_url)
                file_name = f"{username}_profile_{timestamp}.jpg"

                # Save user to DB
                ig_user, created = Instagram_User.objects.get_or_create(username=username)
                ig_user.full_name = profile.full_name
                ig_user.followers = profile.followers
                ig_user.posts = profile.mediacount

                # Save image to model
                if response.status_code == 200:
                    ig_user.profile_pic.save(file_name, ContentFile(response.content), save=True)

                ig_user.save()

                user_data = {
                    'username': ig_user.username,
                    'full_name': ig_user.full_name,
                    'followers': ig_user.followers,
                    'posts': ig_user.posts,
                    'profile_pic_url': ig_user.profile_pic.url  # This is relative to MEDIA_URL
                }

            except Exception as e:
                error = f"Error: {str(e)}"

    return render(request, 'instagram_user.html', {'user_data': user_data, 'error': error})
