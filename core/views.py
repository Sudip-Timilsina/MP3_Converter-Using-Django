from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.conf import settings
import os
from rest_framework.renderers import JSONRenderer  # To enforce JSON output
from yt_dlp import YoutubeDL
from django.core.files.storage import FileSystemStorage
import uuid
import traceback
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import DownloadHistory
from rest_framework import status



@login_required
def index(request):
    return render(request, 'index.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Credentials Invalid")
            return redirect("login")
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['repeatPassword']
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email taken")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username taken")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = authenticate(username=username, password=password)
                login(request, user_login)

                return redirect('index')
        else:
            messages.info(request, "Password Not Matching")
            return redirect('signup')
    else:
        return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')

@csrf_exempt
def converter(request):
    if request.method == 'POST':
        try:
            # Load JSON data from request body
            data = json.loads(request.body)
            yt_link = data.get('link')
            
            if not yt_link:
                return JsonResponse({'error': 'No YouTube link provided'}, status=400)

            # Set output directory for downloaded files
            output_dir = os.path.join(settings.MEDIA_ROOT, 'downloads')
            os.makedirs(output_dir, exist_ok=True)

            # Configure yt-dlp options with ffmpeg location
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'quiet': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': 'C:/ffmpeg/bin',  # Adjust this path as necessary
            }

            with YoutubeDL(ydl_opts) as ydl:
                # Attempt to extract video information
                info = ydl.extract_info(yt_link, download=True)
                print(f"Video info extracted: {info}")  # Debugging log

                # Generate a unique UUID as the file name
                unique_id = uuid.uuid4().hex  # This generates a unique 32-character hexadecimal string

                # Construct the audio file path based on the downloaded files
                audio_file_path = None
                for file in os.listdir(output_dir):
                    if file.endswith('.mp3') and file.startswith(info['title'][:5]):  # Match part of the title for the downloaded file
                        audio_file_path = os.path.join(output_dir, file)
                        break

                # Check if audio file exists
                if not audio_file_path:
                    print(f"Error: Audio file was not downloaded properly.")  # Debugging log
                    return JsonResponse({'error': 'Audio file was not downloaded properly.'}, status=500)

                # Use FileSystemStorage to save the audio file with the unique UUID as the name
                fs = FileSystemStorage(location=output_dir)
                new_audio_filename = f"{unique_id}.mp3"
                fs.save(new_audio_filename, open(audio_file_path, 'rb'))

                # Generate URL for the audio file
                audio_url = fs.url(f"downloads/{new_audio_filename}")
                print(f"Audio URL generated: {audio_url}")  # Debugging log

                def save_download_history(title, audio_url, user=None):
                         history = DownloadHistory(
                                title=title,
                                audio_url=audio_url,
                                user=user,
                             )
                         history.save()

                # Inside your converter view, after the download is complete:
                save_download_history(info['title'], audio_url, request.user)

                return JsonResponse({
                    'title': info['title'],
                    'thumbnail': info.get('thumbnail'),
                    'audio_url': audio_url,
                }, status=200)

        except Exception as e:
            # Log full traceback for debugging
            error_msg = traceback.format_exc()
            print(f"Error occurred: {error_msg}")  # Debugging log
            return JsonResponse({'error': error_msg}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_video_info(link):
    """
    Fetch video title and metadata using yt-dlp.
    """
    ydl_opts = {'quiet': True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        return {'title': info.get('title', 'Unknown Title')}

def download_audio(link):
    """
    Download the audio stream of the video using yt-dlp.
    """
    output_dir = os.path.join(settings.MEDIA_ROOT, 'downloads')
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        return ydl.prepare_filename(info).replace('.webm', '.mp3')
    






class DownloadHistoryAPI(APIView):
    permission_classes = [AllowAny]  # Allow all users (authenticated or not)
    renderer_classes = [JSONRenderer]  # Render response as JSON

    def get(self, request):
        # Retrieve all download history entries
        history = DownloadHistory.objects.all().order_by('-download_date')  # Sort by date, most recent first
        data = [
            {
                'title': entry.title,
                'audio_url': entry.audio_url,
                'download_date': entry.download_date,
                'user': entry.user.username if entry.user else None,
            }
            for entry in history
        ]
        return Response(data, status=status.HTTP_200_OK)
