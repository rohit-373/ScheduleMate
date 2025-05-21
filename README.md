# ScheduleMate
A Python Script to automatically create VIT Chennai courses timetable in Google Calendar using Google Calendar API. 

# How to use
1. Create a Google account (or use an existing one).
2. Go to the [Google Cloud Console](https://console.cloud.google.com/), create a new project.
3. Enable the Google Calendar API for that project.
4. Create OAuth 2.0 credentials:
    - Go to **APIs & Services** > **Credentials**
    - Click **Create Credentials** > **OAuth client ID**
    - Choose **Desktop app**
    - Download the `credentials.json` file
5. Add your Gmail ID in users:
    - Go to **APIs & Services** > **OAuth consent screen**
    - Click **Audience** 
    - Add your Gmail ID in **+ Add users** under **Test users**
6. Place the downloaded `credentials.json` in the same folder as this script
7. Run the script: `python main.py`
8. A browser window will open - **sign in to your Google account** and **authorize access**
9. Enter your course details when prompted

