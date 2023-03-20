import csv
import os
from datetime import datetime

from django.conf import settings
from django.utils.crypto import get_random_string

import requests


class DatasetDownloader:
    def __init__(self):
        self.homeworlds = []
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        self.filename = generate_filename("characters.csv")
        self.filename_path = os.path.join(settings.DATA_PATH, self.filename)

    def fetch_characters(self, url):
        """
        Fetches characters from the API in batches.
        """
        while url:
            # print("###", url)
            response = requests.get(url, headers=self.headers)
            data = response.json()
            for character in data["results"]:
                yield character
            url = data["next"]
    
    def download_data(self):
        """
        Downloads and writes data to a local CSV file.
        """
        url = "https://swapi.dev/api/people/"
        with open(self.filename_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["name", "height", "mass", "hair_color", "skin_color", "eye_color", "birth_year",
                             "gender", "homeworld", "date"])
            for character in self.fetch_characters(url):
                homeworld = self.resolve_homeworld(character["homeworld"])
                edited_date = self.transform_date(character["edited"])
                writer.writerow([character["name"], character["height"], character["mass"], character["hair_color"],
                                 character["skin_color"], character["eye_color"], character["birth_year"],
                                 character["gender"], homeworld, edited_date])
        self.homeworlds = []
        return self.filename

    def resolve_homeworld(self, url):
        """
        Resolves the homeworld URL into the homeworld's name.
        """
        result = next((item for item in self.homeworlds if item["url"] == url), None)
        if result:
            return result["name"]
        
        # print(">>>", url)
        response = requests.get(url, headers=self.headers)
        homeworld = response.json()
        self.homeworlds.append({"url": url, "name": homeworld["name"]})
        return homeworld["name"]

    @staticmethod
    def transform_date(date_string):
        """
        Formats the date string.
        """
        date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date.strftime("%Y-%m-%d")


def generate_filename(filename):
    """
    Generates unique filenames for downloaded files.
    """
    name, ext = os.path.splitext(filename) 
    generated_name = f'{name}_{get_random_string(8)}{ext}'
    return generated_name