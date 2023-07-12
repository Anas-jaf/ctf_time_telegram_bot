#! /user/bin/python3
import requests 
from pprint import pprint
import datetime
import json
import pytz

def incomming_events_list_wrapper(start_timestamp=None,finish_timestamp=None,limit=100,session=None):
    
    return [
                [  
                    "TITLE : " + i['title'],
                    "ORGANIZER : " + i['organizers'][0]['name'][:30] + ' ...' if len(i['organizers'][0]['name']) else '',
                    "STARTS AT : " + format_time(i['start']),
                    "ENDS AT : " + format_time(i['finish']),
                    "DESCRIPTION : " + i['description'][:30].replace('\n','\\n').replace('\r','\\r')+' ...',
                    "URL LINK : " + i['url'],
                    "CTF TYPE : " + i['format'],
                    "PARTICIPANT NUMBER : " + str(i['participants']),
                    "DURATION : " +json.dumps(i['duration'])
                ] 
                for i in get_incomming_events(start_timestamp=start_timestamp,finish_timestamp=finish_timestamp,limit=limit,session=session)
            ]
    
def format_time(time_string):
    # Convert string to datetime object
    datetime_obj = datetime.datetime.fromisoformat(time_string)

    # Create a new naive datetime object without time zone information
    naive_datetime = datetime.datetime(datetime_obj.year, datetime_obj.month, datetime_obj.day, datetime_obj.hour, datetime_obj.minute, datetime_obj.second)

    # Define UTC timezone
    utc_timezone = pytz.timezone('UTC')

    # Define Asia/Amman timezone
    amman_timezone = pytz.timezone('Asia/Amman')

    # Convert datetime to UTC timezone
    datetime_utc = utc_timezone.localize(naive_datetime)

    # Convert UTC datetime to Asia/Amman timezone
    datetime_amman = datetime_utc.astimezone(amman_timezone)

    # Format the datetime in Asia/Amman timezone with AM/PM indication
    formatted_time = datetime_amman.strftime("%A, %Y-%m-%d at %I:%M %p Amman")

    return formatted_time

def make_request(url ,session=None,timeout_seconds=60):
    
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'}
    if session is None :
        response = requests.request("GET", url, timeout=timeout_seconds, headers=headers)
    else : 
        response = session.get(url , timeout=timeout_seconds, headers=headers)
        
    if "403 Forbidden" not in response.text :
        return response.json()
    else:
        return ['Some Thing Wrong']

def get_incomming_events(start_timestamp=None,finish_timestamp=None,limit=100,session=None):
    default_start_end = timestamp_now_and_TillTime()
    
    if not start_timestamp : 
        start_timestamp = default_start_end[0]
    if not finish_timestamp:
        finish_timestamp = default_start_end[1]
        
    url = 'https://ctftime.org/api/v1/events/?limit={}&start={}&finish={}'.format(limit,
                                                                                  start_timestamp,
                                                                                  finish_timestamp
                                                                                  )
    return make_request(url=url,session=session)

def timestamp_now_and_TillTime(after=5):
    current_timestamp = datetime.datetime.now().timestamp()
    after_after_days = datetime.datetime.now() + datetime.timedelta(days=after)
    after_after_days_timestamp = after_after_days.timestamp()
    
    return [current_timestamp , after_after_days_timestamp]

def get_running_events():
    pass

def get_time_stamp():
    pass

def main():
    print('starting script')
    print(get_incomming_events())

if __name__ == "__main__":
    main()