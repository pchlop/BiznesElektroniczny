from config import settings
from client.UdemyClient import UdemyClient
import urllib.request
import os
import csv
import math

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
COURSE_LIMIT = 500
OUTPUT_FILE = 'courses.csv'
OUTPUT_IMAGE_DIR = 'images/'

client = UdemyClient(CLIENT_ID, CLIENT_SECRET)
images = {}

print("Downloading courses data...")
for i in range(math.ceil(COURSE_LIMIT / 20)):
    courses = client.courses(page=i, page_size=1)  # 20 results per request
    for item in courses['results']:
        with open(OUTPUT_FILE, mode='a') as csv_file:
            images[item['published_title']] = item['image_480x270']
            courses_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            courses_writer.writerow([
                item['title'], item['published_title'], item['headline'], item['price'], item['image_480x270']
            ])

print("Downloading courses images...")
for filename, url in images.items():
    urllib.request.urlretrieve(url, OUTPUT_IMAGE_DIR + filename + '.jpg')

