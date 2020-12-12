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
COURSE_LIMIT = 100
OUTPUT_FILE = 'courses.csv'
OUTPUT_IMAGE_DIR = 'images/'
LANGUAGE = 'pl'

client = UdemyClient(CLIENT_ID, CLIENT_SECRET)
images = {}
total = math.ceil(COURSE_LIMIT / 20)
total_items = total * 20

# Download courses data
with tqdm(total=total_items, desc='Downloading courses data', file=sys.stdout) as pbar:
    for i in range(total):
        courses = client.courses(page=i, page_size=1, language=LANGUAGE)  # 20 results per request
        for item in courses['results']:
            images[item['published_title']] = item['image_480x270']
            with open(OUTPUT_FILE, mode='a') as csv_file:
                courses_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                courses_writer.writerow([
                    item['title'], item['published_title'], item['headline'], item['price'], item['image_480x270']
                ])
        pbar.update(20)

# Create images directory if not exists
Path('./images').mkdir(parents=True, exist_ok=True)

# Download courses images and save them to images catalog
with tqdm(total=total_items, desc='Downloading courses images', file=sys.stdout) as pbar:
    for filename, url in images.items():
        urllib.request.urlretrieve(url, OUTPUT_IMAGE_DIR + filename + '.jpg')
        pbar.update(1)
