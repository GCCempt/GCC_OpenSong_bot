from datetime import datetime
import calendar
import datefinder
from dateparser.search import search_dates


# --- Get the current date / time and format it
def currentdatetime(dateformat='%m/%d/%Y %H:%M %p'):
    received_dt = datetime.now()
    received_dt = received_dt.strftime(dateformat)

    return(received_dt)
# --- End Get the current date / time

# --- Get the current date and format it
def currentdate():
    #    received_dt = datetime.now() - timedelta(days=6)
    received_dt = datetime.now()
    received_dt = received_dt.strftime('%m/%d/%Y')

    return received_dt
# --- End Get the current date / time


# ------------ function to extract date from a string
def parsedates(text_string):
    # print('\nParse Dates')
    # text_string = '**2/28/21 Worship Schedule**'
    returned_dates = datefinder.find_dates(text_string, strict=False)  # --- returns a list containing matched dates
    for match in returned_dates:
        # print('\nReturned date:', match.strftime('%m/%d/%Y'))
        return match.strftime('%m/%d/%Y')


# ------------ extract dates
def parsedates2(text_string):
    print('\nParse Dates2')
    dates = search_dates(text_string)
    print(dates)

    # returned_dates = dateparser.parse(str(dates[0]))
    # print(returned_dates)


# ------------ display a calendar for a given month
def displayCalendar():
    print('\nDisplay calendar for a given month')
    yy = 2021
    mm = 2
    print(calendar.month(yy, mm))


# ------------ display the first Sunday of a month
def firstSunday(cal_month=5):
    print('\nFind First Sunday')

    cal = calendar.TextCalendar(calendar.SUNDAY)
    print(cal.prmonth(2021, cal_month))
    print(calendar.SUNDAY)


# ------------ Find the date of "next" Sunday (the first Sunday from Today)
def nextSunday():
    import datetime as DT
    import dateutil.relativedelta as REL
    # print('\nFind date of next Sunday')

    today = DT.date.today()
    # print('\nToday is ', today)

    rd = REL.relativedelta(days=1, weekday=REL.SU)
    next_Sunday = today + rd
    return next_Sunday


# ------------ search a given string for dates
def searchdates(mystring):
    from dateparser.search import search_dates

    print('\nSearch for dates in a string')
    print(search_dates(mystring))  # --- use the search_dates utility to find dates in string


# --- Covnert Date to mm/dd
def convertdate(receivedDate='2021-04-04'):
    #    received_dt = datetime.now() - timedelta(days=6)
    receivedDateObject = datetime.strptime(receivedDate, '%Y-%m-%d')
    convertedDateObject = receivedDateObject.strftime('%m/%d')

    print('\nConverted Date=', convertedDateObject)
    return convertedDateObject
# --- End Get the current date / time

# --- get the current day of the week (i.e. for today)
def getDayOfWeek():
    return datetime.today().strftime('%A')