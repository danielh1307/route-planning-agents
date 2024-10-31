import json
import os

from langchain_core.tools import tool


@tool
def get_events(date_str: str) -> dict:
    """ This function returns the events for a user at a specific date.
    The date must be given in the format YYYY-MM-DD"""
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the JSON file based on the date
    file_path = os.path.join(script_dir, f"{date_str}.json")

    # Check if the file exists
    if not os.path.isfile(file_path):
        return {
            "date": date_str,
            "events": []
        }

    # Read and return the JSON content
    with open(file_path, 'r') as file:
        content = json.load(file)

    return content

# print(get_events("2024-11-01"))
