#!/usr/bin/env python
# coding: utf-8

import time
from datetime import date

from requests import get
import json

import pandas as pd

def vehicle_df_creator(vehicles):
    
    vehicles_df = pd.DataFrame(vehicles['list']).drop(['stale', 'serviceDate', 'stopSequence', 'lastUpdateTime', 'status', 'congestionLevel', 'bearing', 'capacity', 'stopDistancePercent', 'wheelchairAccessible', 'style', 'deviated'], 1)
    vehicles_df = pd.concat([vehicles_df, pd.json_normalize(vehicles_df['location'])], 1)

    vehicles_df = vehicles_df.merge(routes, left_on = 'routeId', right_on = 'id', how = 'left')
    vehicles_df.rename(columns = {'name' : 'Megálló'}, inplace = True)

    return vehicles_df

headers = {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'}

current_time = time.time()
time_epoch = str(int(current_time))
today = date.today().strftime("%Y%m%d")
lat = str(47.497913)
lon = str(19.040236)

vehicles_link = 'https://futar.bkk.hu/api/query/v1/ws/otp/api/where/vehicles-for-location.json?ifModifiedSince=' + time_epoch + '&lat=' + lat + '&latSpan=1&lon=' + lon + '&lonSpan=1&key=bkk-web&version=4&appVersion=3.13.1-59506-4e2e9a7b'
stops_link = 'https://futar.bkk.hu/api/query/v1/ws/otp/api/where/stops-for-location.json?lat=' + lat + '&latSpan=1&lon=' + lon + '&lonSpan=1&key=bkk-web&version=4&appVersion=3.13.1-59506-4e2e9a7b'

time.sleep(5)
vehicles = get(vehicles_link, headers = headers).json()['data']

time.sleep(5)
stops = get(stops_link, headers = headers).json()['data']

routes = pd.DataFrame.from_dict(stops['references']['routes'], orient = 'index')                     .reset_index(drop = True)                     .drop(['color', 'textColor', 'agencyId', 'iconDisplayType', 'iconDisplayText', 'style', 'sortOrder', 'bikesAllowed'], 1)

routes[['From', 'To']] = routes['description'].str.split('|', expand = True)
routes['To'] = routes['To'].str.strip()
routes['From'] = routes['From'].str.strip()

routes.drop(['description'], 1, inplace = True)

vehicles_df = vehicle_df_creator(vehicles)


drop_cols = ['vehicleId', 'stopId', 'label', 'longName', 'innerInternal', 'location', 'type', 'routeId', 'id'] #'tripId', 
for i in drop_cols:
    if i in vehicles_df.columns:
        vehicles_df.drop(i, 1, inplace = True)

file_name = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(int(current_time)))

vehicles_df.to_csv('vehicle_data/' + file_name + '.csv', index = False)