from config import settings
from client.UdemyClient import UdemyClient
from pathlib import Path
from tqdm import tqdm
import urllib.request
import os
import csv
import sys
import logging

# Configuration
# DO NOT DELETE config/categories.csv file!
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
COURSE_LIMIT = 500
OUTPUT_FILE = 'courses.csv'
OUTPUT_FILE_IMAGE_LOCATION = 'images.csv'
OUTPUT_IMAGE_DIR = 'images/'
LANGUAGE = 'pl'

client = UdemyClient(CLIENT_ID, CLIENT_SECRET)
images = {}
locations = {}
counter = 0
page = 1

# Load categories from CSV
categories = []
with open('config/categories.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        categories.append(row['name'])

current_cat = 0

# Download courses data
with tqdm(total=COURSE_LIMIT, desc='Downloading courses data', file=sys.stdout) as pbar:
    while counter < COURSE_LIMIT:
        # 20 results per request
        courses = client.courses(page=page, page_size=1, language=LANGUAGE, subcategory=categories[current_cat])
        try:
            for item in courses['results']:
                if counter == COURSE_LIMIT:
                    break
                image_filename = item['published_title'] + '.jpg'
                image_location = '/'.join([str(x) for x in str(item['id'])]) + '/' + image_filename
                images[image_filename] = item['image_480x270']
                locations[image_filename] = image_location
                price = item['price_detail']['amount'] if item['is_paid'] else 0
                with open(OUTPUT_FILE, mode='a') as csv_file:
                    courses_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    courses_writer.writerow([
                        item['id'], current_cat + 1, item['title'], item['published_title'], item['headline'],
                        price, image_location
                    ])
                counter += 1
            else:
                pbar.update(len(courses['results']))
                current_cat += 1
                continue
            pbar.update(COURSE_LIMIT - pbar.n)
            break
        except Exception as e:
            logging.exception(e)
            break

# Create images directory if not exists
Path('./images').mkdir(parents=True, exist_ok=True)

# Download courses images and save them to images catalog
with tqdm(total=len(images), desc='Downloading courses images', file=sys.stdout) as pbar:
    for filename, url in images.items():
        urllib.request.urlretrieve(url, OUTPUT_IMAGE_DIR + filename)
        pbar.update(1)

# Create image location file (usage for uploading images to prestashop img directory)
with tqdm(total=len(locations), desc='Writing image locations file', file=sys.stdout) as pbar:
    for title, location in locations.items():
        with open(OUTPUT_FILE_IMAGE_LOCATION, mode='a') as csv_file:
            courses_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            courses_writer.writerow([title, location])
        pbar.update(1)
