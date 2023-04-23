import requests
import json
import time


def get_events(page_number, url, headers, payload):
    payload["variables"]["page"] = page_number
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if 'data' not in data:
        print(f"Error: {data}")
        return []

    return data["data"]["eventListings"]["data"]



def print_event_details(events):
    for event in events:
        event_data = event["event"]
        print(f"Event name: {event_data['title']}")
        print(f"Date: {event_data['date']}")
        print(f"Start Time: {event_data['startTime']}")
        print(f"End Time: {event_data['endTime']}")
        print(f"Artists: {[artist['name'] for artist in event_data['artists']]}")
        print(f"Venue: {event_data['venue']['name']}")
        print(f"Event URL: {event_data['contentUrl']}")
        print(f"Number of guests attending: {event_data['attending']}")
        print("-" * 80)


def generate_payload(areas, listing_date_gte, listing_date_lte):
    with open("graphql_query_template.json", "r") as file:
        payload = json.load(file)

    # Update the relevant fields in the payload
    payload["variables"]["filters"]["areas"]["eq"] = areas
    payload["variables"]["filters"]["listingDate"]["gte"] = listing_date_gte
    payload["variables"]["filters"]["listingDate"]["lte"] = listing_date_lte

    return payload




url = 'https://ra.co/graphql'
headers = {
    'Content-Type': 'application/json',
    'Referer': 'https://ra.co/events/uk/london',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
}

areas = 13
listing_date_gte = "2023-04-23T00:00:00.000Z"
listing_date_lte = "2023-04-29T00:00:00.000Z"
payload = generate_payload(areas, listing_date_gte, listing_date_lte)


# Initialize the page number
page_number = 1

# Define the delay between requests (in seconds)
delay = 10  # Adjust this value as needed

# Loop until there are no more events left
while True:
    events = get_events(page_number, url, headers, payload)

    # Break the loop if there are no more events
    if not events:
        break

    print_event_details(events)

    # Increment the page number
    page_number += 1

    # Sleep for the specified delay before sending the next request
    time.sleep(delay)
