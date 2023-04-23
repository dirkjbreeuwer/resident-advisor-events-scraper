# RA.co Event Fetcher

A Python tool to fetch event data from the RA.co GraphQL API and save it as a CSV or JSON file. This tool accepts event area, start date, and end date as command-line arguments and saves the fetched events to a CSV file by default.

## Requirements

- Python 3.6 or higher
- requests library (pip install requests)
- pandas library (pip install pandas)

## Installation

1. Clone the repository or download the source code.
2. Run pip install -r requirements.txt to install the required libraries.

## Usage

### Command-Line Arguments

- `areas`: The area code to filter events.
- `start_date`: The start date for event listings (inclusive, format: `YYYY-MM-DD`).
- `end_date`: The end date for event listings (inclusive, format: `YYYY-MM-DD`).
- `-o` or `--output`: (Optional) The output file path (default: `events.csv`).

### Example

To fetch events for area 13 between April 23, 2023, and April 29, 2023, and save them to a CSV file named `events.csv`, run the following command:

```
python event_fetcher.py 13 2023-04-23 2023-04-29 -o events.csv
```

## Output

The fetched events will be saved to the specified output file (CSV by default) with the following columns:

- Event name
- Date
- Start Time
- End Time
- Artists
- Venue
- Event URL
- Number of guests attending