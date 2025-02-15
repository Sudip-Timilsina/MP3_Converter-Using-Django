﻿# YouTube to MP3 Converter with Download History

This project is a Django-based web application that allows users to convert YouTube videos to MP3 audio files. The app includes user authentication, a REST API to manage download history, and detailed error handling. It leverages Django REST Framework and yt-dlp for audio extraction and metadata handling.

## Features

- **User Authentication**: Login, signup, and logout functionalities for secure access.
- **YouTube to MP3 Conversion**: Download audio from YouTube videos as high-quality MP3 files.
- **Download History**: Save the details of downloaded videos to a database.
- **REST API**: Retrieve download history in JSON format using Django REST Framework.
- **CSRF Protection**: Secure endpoints from CSRF attacks.
- **Custom Error Handling**: Detailed debugging logs and error responses.

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS , Bootstrap 
- **Database**: SQLite 
- **Video Download**: yt-dlp
- **File Handling**: Django's FileSystemStorage

## Installation

### Prerequisites

- Python 3.7+
- pip 
- ffmpeg 

### Steps

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Sudip-Timilsina/youtube-to-mp3-converter.git
    cd youtube-to-mp3-converter
    ```

2. **Install dependencies**:

    Using `pip`:
    ```bash
    pip install -r requirements.txt
   

3. **Apply migrations**:

    ```bash
    python manage.py migrate
    ```

4. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

5. **Access the app**:

    Open your browser and navigate to `http://127.0.0.1:8000/`.

## Usage

1. **Sign Up and Login**:
   - Create a new account or log in with existing credentials.

2. **Convert YouTube Videos**:
   - Navigate to the converter page.
   - Paste the YouTube video link and submit to download the MP3 file.

3. **View Download History**:
   - Use the REST API endpoint `/history/` to retrieve past downloads in JSON format.



## Configuration

- **FFmpeg Path**: Update the `ffmpeg_location` in `ydl_opts` in the `converter` view if needed.
- **Media Storage**: Files are stored in the `media/downloads` directory by default. Update `MEDIA_ROOT` and `MEDIA_URL` in `settings.py` as necessary.

## Contributing

Feel free to fork the repository, make changes, and submit a pull request. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Django REST Framework](https://www.django-rest-framework.org/)
