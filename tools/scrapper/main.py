from config import settings
from client.UdemyClient import UdemyClient
from pathlib import Path
from tqdm import tqdm
import urllib.request
import os
import csv
import math
import sys

# Configuration
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
COURSE_LIMIT = 40
OUTPUT_FILE = 'courses.csv'
OUTPUT_IMAGE_DIR = 'images/'
LANGUAGE = 'en'

client = UdemyClient(CLIENT_ID, CLIENT_SECRET)
images = {}
total = math.ceil(COURSE_LIMIT / 20)

# Download courses data
with tqdm(total=COURSE_LIMIT, desc='Downloading courses data', file=sys.stdout) as pbar:
    for i in range(total):
        courses = client.courses(page=i, page_size=1, language=LANGUAGE)  # 20 results per request
        for item in courses['results']:
            images[item['published_title']] = item['image_480x270']
            image_location = '/'.join([str(x) for x in str(item['id'])]) + '/' + item['published_title'] + '.jpg'
            with open(OUTPUT_FILE, mode='a') as csv_file:
                courses_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                courses_writer.writerow([
                    item['id'], item['title'], item['published_title'], item['headline'],
                    item['price_detail']['amount'], image_location
                ])
        pbar.update(20)

# Create images directory if not exists
Path('./images').mkdir(parents=True, exist_ok=True)

# Download courses images and save them to images catalog
with tqdm(total=len(images), desc='Downloading courses images', file=sys.stdout) as pbar:
    for filename, url in images.items():
        urllib.request.urlretrieve(url, OUTPUT_IMAGE_DIR + filename + '.jpg')
        pbar.update(1)
