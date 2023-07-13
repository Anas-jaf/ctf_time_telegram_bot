#! /bin/python3
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from PIL import Image as PILImage
from pprint import pprint
from io import BytesIO
import requests 
import datetime
import json
import pytz
import glob
import os

def delete_send_folder():
    files = glob.glob('./send_folder/*')
    for f in files:
        os.remove(f)

def count_files():
    files = glob.glob('./send_folder/*')
    return files

def create_pdf_from_dictionary_list(output_path, data_list):
    doc = SimpleDocTemplate(output_path, pagesize=A4, topMargin=20)
    styles = getSampleStyleSheet()
    session = requests.Session() 
    flowables = []

    title_style = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,  # Increase the leading (line spacing) for space between lines
        spaceAfter=0.5 * inch,
        alignment=1  # Center alignment
    )

    title_paragraph = Paragraph('CTF Challenges from {} to {}'.format( datetime.date.today() , datetime.date.today()+datetime.timedelta(days=5) ), title_style)
    flowables.append(title_paragraph)
    flowables.append(Spacer(1, 0.5 * inch))  # Spacing after the title   
    
    for item in data_list:
        title = "<b>TITLE: </b> {}".format(item['title'])
        organizer = "<b>ORGANIZER:</b> {}".format(item['organizers'][0]['name'])
        starts_at = "<b>STARTS AT:</b> {}".format(format_time(item['start']))
        ends_at = "<b>ENDS AT:</b> {}".format(format_time(item['finish']))
        description = "<b>DESCRIPTION:</b> {}".format(item['description'])
        url_link = '<b>URL LINK:</b> <u><font color="blue"><a href="{}">{}</a></font></u>'.format(item['url'], item['url'])
        ctf_type = "<b>CTF TYPE:</b> {}".format(item['format'])
        participant_number = "<b>PARTICIPANT NUMBER:</b> {}".format(item['participants'])
        duration = "<b>DURATION:</b> {}".format(json.dumps(item['duration']))

        flowables.append(Paragraph(title, styles['Normal']))
        flowables.append(Paragraph(organizer, styles['Normal']))
        flowables.append(Paragraph(starts_at, styles['Normal']))
        flowables.append(Paragraph(ends_at, styles['Normal']))
        flowables.append(Paragraph(description, styles['Normal']))
        flowables.append(Paragraph(url_link, styles['Normal'], encoding='utf-8'))  # Specify encoding for non-ASCII characters
        flowables.append(Paragraph(ctf_type, styles['Normal']))
        flowables.append(Paragraph(participant_number, styles['Normal']))
        flowables.append(Paragraph(duration, styles['Normal']))

        # Add image from URL using PIL and ReportLab
        try:
            if item['logo']:
                img_data = fetch_image_data(item['logo'] , session)
                if img_data:
                    img = PILImage.open(img_data)
                    img_width, img_height = img.size
                    aspect_ratio = img_height / img_width
                    max_width = 2 * inch  # Maximum width of the image
                    image_width = min(max_width, img_width)
                    image_height = image_width * aspect_ratio
                    flowables.append(Spacer(1, 0.2 * inch))
                    flowables.append(Image(img_data, width=image_width, height=image_height))
                    print("Success retrieving image: ",200 ,item['logo'])
        except Exception as e:
            print("Error adding image:", str(e))

        flowables.append(Spacer(1, 0.5 * inch))  # Adjust spacing between entries

    doc.build(flowables)

def fetch_image_data(url,session):
    headers = {'User-Agent': 'Mozilla/5.0'}  # Example header
    response = session.get(url, headers=headers,timeout=9000)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        print("Error retrieving image:", response.status_code)
        return None

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
    
    return [int(current_timestamp) , int(after_after_days_timestamp)]

def get_running_events():
    pass

def get_time_stamp():
    pass

def main():
    print('starting ctf_times_utils script')

if __name__ == "__main__":
    main()