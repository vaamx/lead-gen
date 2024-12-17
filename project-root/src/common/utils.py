import random
import time
import json
import csv
from src.config.config import Config
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def random_delay():
    time.sleep(random.uniform(Config.REQUEST_DELAY_MIN, Config.REQUEST_DELAY_MAX))

def random_user_agent():
    return random.choice(Config.USER_AGENTS)

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def deduplicate_records(records, unique_key):
    seen = set()
    unique = []
    for r in records:
        if r[unique_key] not in seen:
            unique.append(r)
            seen.add(r[unique_key])
    return unique 

def export_to_csv(data, filename):
    if not data:
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def export_to_google_sheets(data, spreadsheet_name, worksheet_name):
    if not data:
        return

    # Define the scope
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]

    # Add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/credentials.json', scope)

    # Authorize the clientsheet
    client = gspread.authorize(creds)

    # Get the spreadsheet
    spreadsheet = client.open(spreadsheet_name)

    # Select the worksheet
    worksheet = spreadsheet.worksheet(worksheet_name)

    # Clear existing data
    worksheet.clear()

    # Prepare data for insertion
    keys = data[0].keys()
    worksheet.append_row(list(keys))  # Add header
    for row in data:
        worksheet.append_row([row[key] for key in keys])