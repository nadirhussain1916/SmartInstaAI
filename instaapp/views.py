# instagram_app/views.py

import datetime
import requests
import instaloader
from rest_framework.permissions import IsAuthenticated
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from instaapp.helper import check_instagram_credentials
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from instaapp.models import Instagram_User
from .serializers import InstagramUserSerializer
from instaapp.helper import fetch_instagram_data
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
from instaapp.helper import save_user_and_posts
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


class CustomSignInView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password required.'}, status=status.HTTP_400_BAD_REQUEST)

        if '@' in username:
            return Response({'error': 'Please enter your Instagram username, not email.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            # User doesn't exist or wrong password — now call your external check
            try:
                user = User.objects.get(username=username)
                return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
               # First check the Instagram credentials
                result = check_instagram_credentials(username, password)

                if result.get("status") == "success":
                    # Create the user securely (with hashed password)
                    user = User.objects.create_user(
                        username=username,
                        password=password
                    )

                    # Authenticate the user
                    user = authenticate(username=username, password=password)

                    if user:
                        refresh = RefreshToken.for_user(user)
                        return Response({
                            "status": "success",
                            "access": str(refresh.access_token),
                            "refresh": str(refresh),
                        }, status=status.HTTP_201_CREATED)
                    else:
                        return Response({
                            "status": "error",
                            "message": "Authentication failed after user creation."
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                else:
                    return Response({
                        "status": result.get("status"),
                        "message": result.get("message")
                    }, status=status.HTTP_401_UNAUTHORIZED)

class InstagramFetchData(APIView):
    permission_classes = [IsAuthenticated]  # ✅ only authenticated users allowed

    def post(self, request):
        auth_username = request.user.username

        try:
            # Fetch Instagram user details using Django username
            insta_user = Instagram_User.objects.get(username=auth_username)
            insta_username = insta_user.username
            insta_password = insta_user.password
        except Instagram_User.DoesNotExist:
            return Response(
                {"error": "Instagram credentials not found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            # ✅ Run async function in sync view context
            res = fetch_instagram_data(insta_username, insta_password)
            print(res)
            if res.get("status") == "success":
                save_user_and_posts(
                    insta_username,insta_password,
                    res.get("full_name"),
                    res.get("followers"),
                    res.get("post_count"),
                    res.get("profile_image"),
                    res.get("post_links")
                )
            return Response(
                {"message": "Instagram data fetched and saved successfully."},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to fetch Instagram data: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )