#! /user/bin/python3
import requests 
from pprint import pprint
import datetime

def make_request(url ,session=None,timeout_seconds=60):
    if session is None :
        response = requests.request("GET", url, timeout=timeout_seconds)
    else : 
        response = session.get(url , timeout=timeout_seconds)
        
    if "403 Forbidden" not in response.text :
        return response.json()
    else:
        return ['Some Thing Wrong']

def get_incomming_events(start_timestamp=None,finish_timestamp=None,limit=100,session=None):
    default_start_end = timestamp_now_and_TillTime()
    
    if not start_timestamp : 
        start_timestamp = default_start_end[0]
    elif not finish_timestamp:
        finish_timestamp = default_start_end[1]
        
    url = 'https://ctftime.org/api/v1/events/?limit={}&start={}&finish={}'.format(limit=limit,
                                                                                  start_timestamp=start_timestamp,
                                                                                  finish_timestamp=finish_timestamp
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

if __name__ == "__main__":
    main()