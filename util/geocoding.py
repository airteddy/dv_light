# 지오코딩 관련 패키지
from geopy.geocoders import Nominatim
geo_local = Nominatim(user_agent='South Korea')

# 기타 관련 패키지
import time
import tqdm 
import os
import numpy as np
import pandas as pd
from urllib.request import urlopen
from urllib import parse
from urllib.request import Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json
import multiprocessing as mp

class osmgeo():
    def __init__(self, config):
        self.config = config

        self.nomiloc = config["geocoding"]["osgeo"]["nomiloc"]
        self.geo_local = Nominatim(user_agent = self.nomiloc)
        

    def findloc(self, address):
        geo = geo_local.geocode(address)
        return geo.latitude, geo.longitude


class navergeo():
    def __init__(self, config):
        self.config = config
        
        self.client_id = config["geocoding"]["navergeo"]["client_id"]
        self.client_pw = config["geocoding"]["navergeo"]["client_pw"]
        self.api_url = config["geocoding"]["navergeo"]["api_url"]

    
    def findloc(self, address):
        add_urlenc = parse.quote(address)  
        url = self.api_url + add_urlenc
        request = Request(url)
        request.add_header('X-NCP-APIGW-API-KEY-ID', self.client_id)
        request.add_header('X-NCP-APIGW-API-KEY', self.client_pw)
        try:
            response = urlopen(request)
        except HTTPError as e:
            # print('HTTP Error!')
            latitude = None
            longitude = None
        else:
            rescode = response.getcode()
            if rescode == 200:
                response_body = response.read().decode('utf-8')
                response_body = json.loads(response_body)   # json
                if response_body['addresses'] == [] :
                    # print("'result' not exist!")
                    latitude = None
                    longitude = None
                else:
                    latitude = response_body['addresses'][0]['y']
                    longitude = response_body['addresses'][0]['x']
                    # print("Success!")
            else:
                # print('Response error code : %d' % rescode)
                latitude = None
                longitude = None
        
        return latitude, longitude




if __name__ == "__main__":
    roadadd = pd.read_csv("도로명주소.csv")

    # print(roadadd["도로명"][0])

    roadadd["lat"] = -1
    roadadd["lon"] = -1
    print(roadadd)
    geocoding = navergeo()
    for i, add in enumerate(tqdm.tqdm(roadadd["도로명"])):
        # print("찾고있는 주소", add)
        lat, lon = geocoding.findloc(add)
        roadadd["lon"][i] = lon
        roadadd["lat"][i] = lat
        # if i == 5:
        #     break
    # print(lat, lon)
    print(roadadd)
    roadadd.to_csv("도로명주소_geocoded.csv", encoding='utf-8', index=False)





