import os.path
from datetime import date, timedelta
from dotenv import load_dotenv
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()
academics = os.getenv("ACADEMICS")
extraCurricular = os.getenv("EXTRA_CURRICULAR")

with open('timetable.json') as f:
    timetable = json.load(f)

availableColors = {
    "lavender":   1,
    "sage":       2,
    "grape":      3,
    "flamingo":   4,
    "banana":     5,
    "tangerine":  6,
    "peacock":    7,
    "graphite":   8,
    "blueberry":  9,
    "basil":      10,
    "tomato":     11
}

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def next_weekday(weekday: str) -> date:
    """
    Returns the date of the next occurrence of a given weekday.
    """
    weekdays = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4, "SA": 5, "SU": 6}
    days_ahead = weekdays[weekday] - date.today().weekday()
    if days_ahead < 0:
        days_ahead += 7
    return date.today() + timedelta(days_ahead)

def init_calendar() -> object:
    """
    Initializes the Google Calendar API.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)

def create_event(service, courseTitle, courseCode, slotCombined, venue, facultyName, colorCode) -> None:
    """
    Creates a Google Calendar event.
    """
    slots = slotCombined.replace(" ", "").split('+')
    for slot in slots:
        if slot in timetable:
            for session in timetable[slot]['sessions']:
                startTime = session['startTime']
                endTime = session['endTime']
                weekDay = session['weekDay']
                event = {
                    'summary': courseTitle,
                    'description': f'{courseCode} - {facultyName}',
                    'location': venue,
                    'start': {
                        'dateTime': f'{next_weekday(weekDay)}T{startTime}:00+05:30',
                        'timeZone': 'Asia/Kolkata',
                    },
                    'end': {
                        'dateTime': f'{next_weekday(weekDay)}T{endTime}:00+05:30',
                        'timeZone': 'Asia/Kolkata',
                    },
                    'recurrence': [
                        f'RRULE:FREQ=WEEKLY;WKST=SU;BYDAY={weekDay}'
                    ],
                    'reminders': {
                        'useDefault': False,
                        'overrides': [
                            {'method': 'popup', 'minutes': 15}
                        ],
                    },
                    'colorId': colorCode,
                }

                event = service.events().insert(calendarId=academics, body=event).execute()
        else:
            print(f"Slot {slot} not found in timetable.")
            return None
    print(f"Event created: {courseTitle} - {courseCode} in {venue} with {facultyName} on slots {slots}")
    return None

def main():
    """
    Main function to run the script.
    Prompts the user for course details and creates events in Google Calendar.
    """

    try:
        # Build the Google Calendar API service
        service = init_calendar()

        loop = True
        while loop:
            courseTitle = input('Enter the course title: ')
            courseCode = input('Enter the course code: ')
            slotCombined = input('Enter the slot: ')
            venue = input('Enter the venue: ')
            facultyName = input('Enter the faculty name: ')
            print('Available colors:')
            for i, color in enumerate(availableColors.keys(), start=1):
                print(f"{i}. {color}")
            colorName = input('Enter the color name: ')
            colorCode = availableColors.get(colorName, 1)

            create_event(service, courseTitle, courseCode, slotCombined, venue, facultyName, colorCode)

            ask = input('Do you want to add another course? (y/n): ')
            if ask.lower() == 'y':
                loop = True
            else:
                loop = False

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()