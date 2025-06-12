# instagram_app/views.py

import datetime
import requests
import instaloader

from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Instagram_User
from .serializers import InstagramUserSerializer

# views.py
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Instagram_User
from .serializers import InstagramUserSerializer
import instaloader
from django.core.files.base import ContentFile
import requests
import datetime

from instaloader.exceptions import (
    QueryReturnedNotFoundException,
    LoginRequiredException,
    BadResponseException,
    ConnectionException,
    InstaloaderException
)

class InstagramUserAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        if not username or '@' in username:
            return Response(
                {"error": "Please enter a valid Instagram username."},
                status=status.HTTP_400_BAD_REQUEST
            )

        loader = instaloader.Instaloader()

        try:
            profile = instaloader.Profile.from_username(loader.context, username)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
            pic_url = profile.profile_pic_url
            response = requests.get(pic_url)
            file_name = f"{username}_profile_{timestamp}.jpg"

            # Create or update user
            ig_user, _ = Instagram_User.objects.get_or_create(username=username)
            ig_user.full_name = profile.full_name
            ig_user.followers = profile.followers
            ig_user.posts = profile.mediacount

            # Save image
            if response.status_code == 200:
                ig_user.profile_pic.save(file_name, ContentFile(response.content), save=True)

            ig_user.save()
            serializer = InstagramUserSerializer(ig_user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except QueryReturnedNotFoundException:
            return Response(
                {"error": "Instagram username not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        except LoginRequiredException:
            return Response(
                {"error": "Instagram requires login to access this data."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        except BadResponseException as e:
            return Response(
                {"error": f"Bad response from Instagram: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except ConnectionException:
            return Response(
                {"error": "Network error. Please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except InstaloaderException as e:
            return Response(
                {"error": f"Instaloader error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            return Response(
                {"error": f"Unexpected error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# class InstagramUserAPIView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         if not username or '@' in username:
#             return Response(
#                 {"error": "Please enter a valid Instagram username."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         loader = instaloader.Instaloader()

#         try:
#             profile = instaloader.Profile.from_username(loader.context, username)
#             timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
#             pic_url = profile.profile_pic_url
#             response = requests.get(pic_url)
#             file_name = f"{username}_profile_{timestamp}.jpg"

#             # Create or update user
#             ig_user, _ = Instagram_User.objects.get_or_create(username=username)
#             ig_user.full_name = profile.full_name
#             ig_user.followers = profile.followers
#             ig_user.posts = profile.mediacount

#             # Save image to model
#             if response.status_code == 200:
#                 ig_user.profile_pic.save(file_name, ContentFile(response.content), save=True)

#             ig_user.save()
#             serializer = InstagramUserSerializer(ig_user)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response(
#                 {"error": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

class CreateUserFromInstagramAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user exists in Instagram_User table
        if not Instagram_User.objects.filter(username=username).exists():
            return Response({"error": "User not exists in Instagram_User table."}, status=status.HTTP_404_NOT_FOUND)

        # Check if already exists in Django's auth_user table
        if User.objects.filter(username=username).exists():
            return Response({"error": "User already created in auth system."}, status=status.HTTP_400_BAD_REQUEST)

        # Create user in Django's built-in auth system
        user = User.objects.create_user(username=username, password=password)
        user.save()

        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
