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
from rest_framework.decorators import api_view, permission_classes
import threading
import os
from rest_framework_simplejwt.tokens import RefreshToken
from instaapp.models import Instagram_User
from .serializers import InstagramUserSerializer
from instaapp.helper import fetch_instagram_data,get_and_save_post_detail
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Instagram_User,InstagramPost
from .serializers import InstagramUserSerializer, InstagramPostSerializer
from django.shortcuts import get_object_or_404
import instaloader
from django.core.files.base import ContentFile
import requests
import datetime
from instaapp.helper import save_user_and_posts
import asyncio
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI, AuthenticationError, RateLimitError, OpenAIError
from .serializers import CarouselGeneratorSerializer
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
                    # Step 3: Save Instagram user profile (you can fill others later)
                    Instagram_User.objects.create(
                        user=user,
                        username=username,
                        password=password  # 🔒 WARNING: Only store this if you absolutely need to.
                    )

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
            # ✅ Define your background task
            def background_task():
                try:
                    res = fetch_instagram_data(insta_username, insta_password)
                    if res.get("status") == "success":
                        save_user_and_posts(
                            insta_username,
                            insta_password,
                            res.get("full_name"),
                            res.get("followers"),
                            res.get("post_count"),
                            res.get("profile_image"),
                            res.get("post_links")
                        )
                    print("Instagram data fetched and saved in background.")
                except Exception as e:
                    print(f"Background task error: {e}")
                get_and_save_post_detail(insta_username)

            # ✅ Run it in background
            threading.Thread(target=background_task).start()
            # ✅ Return immediately
            return Response(
                {"message": "Data fetching started in background."},
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to fetch Instagram data: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
    
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') 

# Assume `client` is your OpenAI client instance
client = OpenAI(api_key=OPENAI_API_KEY)  # or use settings.ENV

SYSTEM_PROMPT = "You are a helpful assistant that creates engaging Instagram carousel content."

async def process_inspiration(inspiration):
    # Dummy async function (replace with actual processing)
    await asyncio.sleep(0.1)
    return f"Inspired by: {inspiration}" if inspiration else ""

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_carousel(request):
    """Generate Instagram carousel content"""
    serializer = CarouselGeneratorSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    content_type = data['content_type']
    description = data['description']
    slides = data['slides']
    inspiration = data.get('inspiration', '')

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        processed_inspiration = loop.run_until_complete(process_inspiration(inspiration))
        loop.close()

        # Build user prompt
        user_prompt = f"""
        Generate Instagram carousel content with the following specifications:

        **Content Type:** {content_type}
        **Description:** {description}
        **Number of Slides:** {slides}
        """
        if processed_inspiration:
            user_prompt += f"\n{processed_inspiration}"

        user_prompt += f"""

        Please generate exactly {slides} slides of content. Format your response as a numbered list where each number represents one slide's content.

        Example format:
        1. [Hook content for slide 1]
        2. [Content for slide 2]
        ...
        {slides}. [CTA content for final slide]
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()

        # Parse numbered list
        slide_contents = []
        lines = content.split('\n')
        current_slide = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line[0].isdigit() and '.' in line:
                if current_slide:
                    slide_contents.append(current_slide.strip())
                current_slide = line.split('.', 1)[1].strip()
            else:
                current_slide += " " + line

        if current_slide:
            slide_contents.append(current_slide.strip())

        if len(slide_contents) != slides:
            return Response({
                'error': f'Generated {len(slide_contents)} slides but expected {slides}. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'success': True,
            'carousel_content': {
                'content_type': content_type,
                'description': description,
                'slides': slides,
                'inspiration': inspiration,
                'slide_contents': slide_contents
            }
        }, status=status.HTTP_200_OK)

    except AuthenticationError:
        return Response({'error': 'OpenAI API key is invalid or missing'}, status=status.HTTP_401_UNAUTHORIZED)

    except RateLimitError:
        return Response({'error': 'OpenAI API rate limit exceeded. Please try again later.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    except OpenAIError as e:
        return Response({'error': f'OpenAI API error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    auth_username = request.user.username
    print(auth_username)
    user = get_object_or_404(Instagram_User, username=auth_username)
    serializer = InstagramUserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_posts(request):
    auth_username = request.user.username
    user = get_object_or_404(Instagram_User, username=auth_username)
    posts = InstagramPost.objects.filter(user=user).order_by('-likes')[:3]
    serializer = InstagramPostSerializer(posts, many=True)
    return Response(serializer.data)