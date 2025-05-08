from github import Auth
from github import Github

from datetime import datetime, timedelta

import json
import pandas as pd
import pytz
import os
import requests
import sys

API_KEY = os.environ['API_KEY']


def update_date_list(today, repo, date_contents, date_list, update_time):
  '''
  : modify list of dates, upload new list
  :
  : (returns nothing)
  '''
  # read data from github
  date_list.remove(today)
  date_string = json.dumps(date_list)

  repo.update_file(path = date_contents.path
                  ,message = f'update - {update_time}'\
                  ,content = date_string
                  ,sha = date_contents.sha
                  )

def update_weather_data(repo, weather_list_name, weather_git_url, weather_site, update_time):
  '''
  : try to get existing weather data
  :   create new if not found
  : download data from city site
  : format
  : if exists, update, else create
  '''
  try:
    weather_contents = repo.get_contents(weather_list_name)
    weather_data = requests.get(weather_git_url).json()
    file_exists = True
  except:
    weather_data = {}
    file_exists = False

  # download data, add to data structure (with various formatting)
  new_data = pd.read_json(weather_site)
  k = new_data['measurement_timestamp'].values[0]
  v = new_data['air_temperature'].values[0]
  v = round(float(v), 2)
  weather_data[k] = v

  # sorting data just cuz
  weather_data = dict(sorted(weather_data.items(), reverse=True))

  # github needs a string or bytes via this API; converting dictionary to string
  weather_data_string = json.dumps(weather_data)

  # append to existing, if exists
  # else, send new
  if file_exists:
    repo.update_file(path = weather_contents.path
                    ,message = f'update - {update_time}'\
                    ,content = weather_data_string
                    ,sha = weather_contents.sha
                    )
  else:
    repo.create_file(path = weather_list_name
                    ,message = f'start_upload - {update_time}'\
                    ,content = weather_data_string)


#________________________________________________________________________________
if __name__ == '__main__':

  # initial variables
  main_url = 'https://raw.githubusercontent.com/jbeaudette3/Hello_World/refs/heads/main/'

  date_list_name = 'list_1.json'
  date_git_url = main_url + date_list_name

  weather_list_name = 'weather_data_dict_1.json'
  weather_git_url = main_url + weather_list_name

  weather_site = 'https://data.cityofchicago.org/resource/k7hf-8y75.json?$select=measurement_timestamp,air_temperature&station_name=Foster%20Weather%20Station&$order=measurement_timestamp%20DESC&$limit=1'

  # check if file exists
  try:
    date_list = requests.get(date_git_url).json()
  else:
    sys.exit()

  # login, get repo and info
  g = Github(auth=Auth.Token(API_KEY))
  repo = g.get_user().get_repo('Hello_World')
  date_contents = repo.get_contents(date_list_name)

  # misc timestamps ('dt' not used directly, but as a shortcut for the other 2)
  dt = datetime.now(pytz.timezone('America/Chicago'))
  update_time = dt.strftime('%Y.%m.%d %H:%M')
  today = dt.strftime('%Y.%m.%d')

  # if the date list is empty but still exists
  if not date_list:
    repo.delete_file(path = date_contents.path
                     ,message = f'delete - {update_time}'\
                     ,sha = date_contents.sha
                     )
    sys.exit()

  if today in date_list:
    update_date_list(today = today,\
                     repo = repo,\
                     date_contents = date_contents,\
                     date_list = date_list,\
                     update_time = update_time)
    
    update_weather_data(repo = repo, \
                        weather_list_name = weather_list_name, \
                        weather_git_url = weather_git_url, \
                        weather_site = weather_site, \
                        update_time = update_time)

    # logout
    g.close()
