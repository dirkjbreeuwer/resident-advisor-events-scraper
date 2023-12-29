import requests
import json
import time
import csv
import sys
import argparse
from datetime import datetime, timedelta

URL = 'https://ra.co/graphql'
HEADERS = {
    'Content-Type': 'application/json',
    'Referer': 'https://ra.co/events/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
}
QUERY_TEMPLATE_PATH = "graphql_query_template.json"
DELAY = 1  # Adjust this value as needed


class ArtistFetcher:
    """
    A class to fetch and print event details from RA.co
    """

    def __init__(self, areas, listing_date_gte, listing_date_lte):
        self.payload = self.generate_payload(areas, listing_date_gte, listing_date_lte)

    @staticmethod
    def generate_payload(areas, listing_date_gte, listing_date_lte):
        """
        Generate the payload for the GraphQL request.

        :param areas: The area code to filter events.
        :param listing_date_gte: The start date for event listings (inclusive).
        :param listing_date_lte: The end date for event listings (inclusive).
        :return: The generated payload.
        """
        with open(QUERY_TEMPLATE_PATH, "r") as file:
            payload = json.load(file)

        payload["variables"]["filters"]["areas"]["eq"] = areas
        payload["variables"]["filters"]["listingDate"]["gte"] = listing_date_gte
        payload["variables"]["filters"]["listingDate"]["lte"] = listing_date_lte

        return payload

    def get_artists(self, page_number):
        """
        Fetch artists for the given page number.

        :param page_number: The page number for event listings.
        :return: A list of artists.
        """
        self.payload["variables"]["page"] = page_number
        response = requests.post(URL, headers=HEADERS, json=self.payload)

        try:
            response.raise_for_status()
            data = response.json()
        except (requests.exceptions.RequestException, ValueError):
            print(f"Error: {response.status_code}")
            return []

        if 'data' not in data:
            print(f"Error: {data}")
            return []

        return data["data"]["eventListings"]["data"]

    @staticmethod
    def print_event_details(events):
        """
        Print the details of the events.

        :param events: A list of events.
        """
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

    def fetch_and_print_all_artists(self):
        """
        Fetch and print all artists.
        """
        page_number = 1

        while True:
            events = self.get_artists(page_number)

            if not events:
                break

            self.print_event_details(events)
            page_number += 1
            time.sleep(DELAY)

    def fetch_all_artists(self):
        """
        Fetch all events and return them as a list.

        :return: A list of all events.
        """
        all_artists = []
        page_number = 1

        while True:
            events = self.get_artists(page_number)

            if not events:
                break

            all_artists.extend(events)
            page_number += 1
            time.sleep(DELAY)

        return all_artists

    def save_artists_to_csv(self, events, output_file="artists.csv"):
        """
        Save events to a CSV file.

        :param events: A list of events.
        :param output_file: The output file path. (default: "artists.csv")
        """
        with open(output_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Event name", "Date", "Artists",
                             "Venue"])

            for event in events:
                event_data = event["event"]
                date_string = event_data["date"]
                date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f")
                readable_date = date_object.strftime("%B %d, %Y")
                writer.writerow([event_data['title'], readable_date,
                                 ' | '.join([artist['name'] for artist in event_data['artists']]),
                                 event_data['venue']['name']])


def main():
    parser = argparse.ArgumentParser(description="Fetch artists from ra.co and save them to a CSV file.")
    parser.add_argument("areas", type=int, help="The area code to filter artists.")
    parser.add_argument("start_date", type=str,
                        help="The start date for event listings (inclusive, format: YYYY-MM-DD).")
    parser.add_argument("end_date", type=str, help="The end date for event listings (inclusive, format: YYYY-MM-DD).")
    parser.add_argument("-o", "--output", type=str, default="artists.csv",
                        help="The output file path (default: artists.csv).")
    args = parser.parse_args()

    listing_date_gte = f"{args.start_date}"
    listing_date_lte = f"{args.end_date}"

    artist_fetcher = ArtistFetcher(args.areas, listing_date_gte, listing_date_lte)

    all_artists = []
    current_start_date = datetime.strptime(args.start_date, "%Y-%m-%d")

    while current_start_date <= datetime.strptime(args.end_date, "%Y-%m-%d"):
        listing_date_gte = current_start_date.strftime("%Y-%m-%d")
        artist_fetcher.payload = artist_fetcher.generate_payload(args.areas, listing_date_gte, listing_date_lte)
        artists = artist_fetcher.fetch_all_artists()
        all_artists.extend(artists)
        current_start_date += timedelta(days=len(artists))

    artist_fetcher.save_artists_to_csv(all_artists, args.output)


if __name__ == "__main__":
    main()
