import cv2
import os
import requests
import shutil
import skimage.metrics
import subprocess

TOKEN_NAME = "BOARD_BOT_TOKEN"

if TOKEN_NAME not in os.environ:
    print(f"Error: {TOKEN_NAME} is not set")
    exit(1)

CURRENT_PATH = "current.jpeg"
CANDIDATE_PATH = "candidate.jpeg"

SIMILARITY_THRESHOLD = 0.9

def post_image(path):
  url = "https://gate.whapi.cloud/messages/image"
  token = os.environ[TOKEN_NAME]

  data = {
    "to": "120363422200045729@g.us", # Board-bot-test group
    "caption": "The latest image from Board-bot.",
  }

  files = {
    "media": open(path, "rb")
  }

  headers = {
    "authorization": f"Bearer {token}",
  }

  response = requests.post(url, data=data, files=files, headers=headers)

  print(response.text)

print(f"Capturing {CANDIDATE_PATH}")
subprocess.run(["rpicam-jpeg", "--immediate", "--autofocus-on-capture", "--width", "1296", "--height", "972", "--output", CANDIDATE_PATH], check=True)

current = cv2.imread(CURRENT_PATH)
candidate = cv2.imread(CANDIDATE_PATH)

current = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
candidate = cv2.cvtColor(candidate, cv2.COLOR_BGR2GRAY)

print("Calculating structural similarity")
similarity = skimage.metrics.structural_similarity(current, candidate)

print(f"Structural similarity = {similarity}")

if similarity < SIMILARITY_THRESHOLD:
  print("Updating current image")
  shutil.copyfile(CANDIDATE_PATH, CURRENT_PATH)
  post_image(CURRENT_PATH)
else:
  print("No change")
