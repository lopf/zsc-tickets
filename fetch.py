from bs4 import BeautifulSoup
import requests
import json

url = 'https://tickets.zsclions.ch/webshop/webticket/eventlist'
headers = { # headers from the curl command
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://tickets.zsclions.ch/webshop/webticket/eventlist',
    'Connection': 'keep-alive',
    #'Cookie': 'JSESSIONID=xxx; sso-postlogin-redirect=https://tickets.zsclions.ch/webshop/webticket/eventlist; yyy=xxx; BIGipServer~ASP~tickets.zsclions.ch=xxx',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}
events_json = []

def getEvents():
    response = requests.get(url, headers=headers)
    events_json = []
    # Assume that the HTML content is stored in a variable called html_response
    soup = BeautifulSoup(response.content, 'html.parser')
    events = soup.select('div.evt-event-list')

    # iterate over each event and extract the details
    for event in events:
        title = event.find('h2').text.strip()
        subtitle = event.find('p', {'class': 'eventSubtitle1'}).text.strip()
        date = event.select_one('span[id^="event-date-"]').text.strip()
        time = event.find('span', {'id': lambda x: x and x.startswith('event-time-')}).text.strip()
        location = event.find('span', {'id': lambda x: x and x.startswith('event-location-')}).text.strip()
        ticket_availability = event.find('span', {'id': 'soldtext'})

        if ticket_availability:
            ticket_availability = ticket_availability.text.strip()
        else:
            ticket_availability = 'Available'

        event_item = {
                "title": title,
                "subtitle": subtitle,
                "date": date,
                "time": time,
                "location": location,
                "ticket_availability": ticket_availability
            }
        events_json.append(event_item)

        print(f'Title: {title}')
        print(f'Subtitle: {subtitle}')
        print(f'Date: {date}')
        print(f'Time: {time}')
        print(f'Location: {location}')
        print(f'Ticket availability: {ticket_availability}')
        print('-------------------')
    return events_json

getEvents()

print(json.dumps(events_json))
