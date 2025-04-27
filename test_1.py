from github import Auth
from github import Github

from datetime import datetime

import json
import pandas as pd
import requests
import os

API_KEY = os.environ['API_KEY']

auth = Auth.Token(API_KEY)
g = Github(auth=auth)

# see if file exists online, and save to variable.
# variable will be used for download and upload
# no need to check multiple times
repo = g.get_user().get_repo('Hello_World')

repo_all_contents = repo.get_contents("")
for c in repo_all_contents:
  if c.name == file_name:
    file_exists = True
    repo_contents = repo.get_contents(file_name)
  else:
    file_exists = False

# if file exists, download data and format into json.
# if file does not exist, create new data structure for upload.
if file_exists:
  data = requests.get(git_url).json()
else:
  data = {}

# download data, add to data structure (with various formatting)
site = 'https://data.cityofchicago.org/resource/k7hf-8y75.json?$select=measurement_timestamp,air_temperature&station_name=Foster%20Weather%20Station&$order=measurement_timestamp%20DESC&$limit=1'
new_data = pd.read_json(site)
k = new_data['measurement_timestamp'].values[0]
v = new_data['air_temperature'].values[0]
v = round(float(v), 2)
data[k] = v

# sorting data just cuz
data = dict(sorted(data.items(), reverse=True))

# github needs a string or bytes via this API; converting dictionary to string
data_string = json.dumps(data)

# add timestamp of latest data
update_time = datetime.now().strftime('%Y-%m-%d %H:%M')

# append to existing, if exists
# else, send new
if file_exists:
  repo.update_file(path = repo_contents.path
                   ,message = f'update - {update_time} UTC'\
                   ,content = data_string
                   ,sha = repo_contents.sha
                   )
else:
  repo.create_file(path = file_name
                  ,message = f'start_upload - {update_time} UTC'\
                  ,content = data_string)

# be polite, close your connection
g.close()
