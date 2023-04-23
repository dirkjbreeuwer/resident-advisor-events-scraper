import requests
import json

url = 'https://ra.co/graphql'
headers = {
    'Content-Type': 'application/json',
    'Referer': 'https://ra.co/events/uk/london',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
}


# Update the date range and other filters as needed
payload = {
    "operationName": "GET_EVENT_LISTINGS",
    "variables": {
        "filters": {
            "areas": {"eq": 13},
            "listingDate": {
                "gte": "2023-04-23T00:00:00.000Z",
                "lte": "2023-04-29T00:00:00.000Z"
            }
        },
        "filterOptions": {"genre": True},
        "pageSize": 20,
        "page": 4
    },
    "query": """
query GET_EVENT_LISTINGS($filters: FilterInputDtoInput, $filterOptions: FilterOptionsInputDtoInput, $page: Int, $pageSize: Int) {
  eventListings(filters: $filters, filterOptions: $filterOptions, pageSize: $pageSize, page: $page) {
    data {
      id
      listingDate
      event {
        ...eventListingsFields
        artists {
          id
          name
          __typename
        }
        __typename
      }
      __typename
    }
    filterOptions {
      genre {
        label
        value
        __typename
      }
      __typename
    }
    totalResults
    __typename
  }
}

fragment eventListingsFields on Event {
  id
  date
  startTime
  endTime
  title
  contentUrl
  flyerFront
  isTicketed
  attending
  queueItEnabled
  newEventForm
  images {
    id
    filename
    alt
    type
    crop
    __typename
  }
  pick {
    id
    blurb
    __typename
  }
  venue {
    id
    name
    contentUrl
    live
    __typename
  }
  __typename
}
"""
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(f"Status Code: {response.status_code}")

data = response.json()

# Extract event data from the response
events = data['data']['eventListings']['data']

# Print the event details
for event in events:
    event_data = event['event']
    print(f"Event name: {event_data['title']}")
    print(f"Artists: {[artist['name'] for artist in event_data['artists']]}")
    print(f"Venue: {event_data['venue']['name']}")
    print(f"Event URL: {event_data['contentUrl']}")
    print(f"Number of guests attending: {event_data['attending']}")
    print('-' * 80)
