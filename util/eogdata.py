"""
eog 사이트 ("https://eogdata.mines.edu/nighttime_light/nightly/rade9d/") 에서
1. 신규 저장 이미지가 올라갔는지 확인하고
2. 이를 자동으로 다운받고
3. DB에 저장
"""

print("eog start..")
print("read package")
from multiprocessing.connection import wait
from matplotlib.pyplot import rc
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import glob
import json 
import tqdm 
import chromedriver_autoinstaller
import numpy as np
from osgeo import gdal

print("read done")

class EOGnight():
    def __init__(self, config):
        self.config = config

    def get_korea_opt(self):
        return self.config["nightly"]["raw"]["save_only_korea"]

    def read_tif_date(self, date, is_only_korea = get_korea_opt()):
        try:
            date = int(date)
            date = str(date)
            # yyyy = date[0:4]
            # mm = date[4:6]
            # dd = date[6:]
            # assert int(1980) < int(yyyy) < int()
        except:
            print(str(date) + "is not a from like YYYYMMDD")
            return None

        if is_only_korea:
            filelist = glob.glob(self.config["nightly"]["korea"]["save_path"] + "*")
        else:
            filelist = glob.glob(self.config["nightly"]["raw"]["save_path"] + "*")

        tifpath = list(filter(lambda x: date in x, filelist))[0]
        tif = gdal.Open(tifpath)

        return tif

    def load_saved_file_list(self, is_only_korea = get_korea_opt()):
        if is_only_korea:
            filelist = glob.glob(self.config["nightly"]["korea"]["save_path"] + "*")
        else:
            filelist = glob.glob(self.config["nightly"]["raw"]["save_path"] + "*")

        return filelist

    def load_website_file_list(self):
        response = requests.get(self.config["eog"]["url"])
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            middle = str(soup).split(self.config["eog"]["filename"])[1:]
            result = list(reversed(sorted([tifdate.split('.rade9d.tif')[0] for tifdate in middle ])))
        else : 
            result = response.status_code

        return result

    def is_new_file(self):
        saved_list = self.load_saved_file_list(is_only_korea=self.config["nightly"]["raw"]["save_only_korea"])
        web_list = self.load_website_file_list()

        web_list = list(reversed(sorted(list(set(web_list)))))
        saved_list = [tifname.split('npp_d')[1].split(".rade9d.tif")[0] for tifname in saved_list]
        
        result_list = []
        for name in web_list:
            if name in saved_list:
                continue
            else:
                result_list.append(name)

        self.result_list = result_list

        return result_list

    def download_tif(self, date):
        def wait_download(path_to_downloads):
            dlCounter = len(glob.glob1(path_to_downloads,"*.crdownload"))
            if dlCounter == 1:
                dl_wait = True
            else:
                dl_wait = False
            return dl_wait
        
        # date -> str : yyyymmdd 

        download_path = os.path.abspath(self.config["eog"]["downloadpath"])

        print(download_path)

        options = webdriver.ChromeOptions()
        options.add_argument(self.config["eog"]["chrome_user_agent"])
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        prefs = {"download.default_directory":download_path}
        options.add_experimental_option("prefs", prefs)

        chromedriver_autoinstaller.install()

        driver = webdriver.Chrome(options=options)
        driver.get("https://eogdata.mines.edu/nighttime_light/nightly/rade9d/SVDNB_npp_d"+date+".rade9d.tif")
        time.sleep(5)

        id = self.config["eog"]["id"]
        pswd = self.config["eog"]["pw"]

        driver.find_element(By.ID,"username").send_keys(id)
        driver.find_element(By.ID,"password").send_keys(pswd)
        driver.find_element(By.ID,"kc-login").click()

        for i in tqdm.tqdm(range(0,int(self.config["eog"]["waittime"]))):
            time.sleep(1)

        while (wait_download(download_path)):
            time.sleep(1)
 
    def update(self):
        if int(self.config["nightly"]["raw"]["update_period"]) != 0:
            self.is_new_file()
            max_period_num = np.min([1+int(self.config["nightly"]["raw"]["update_period"]), len(self.result_list)])
        else:
            max_period_num = 0


        if int(max_period_num) < 2:
            print("eog update end")
        else:
            print(self.result_list[1:max_period_num])
            for index in range(1,max_period_num):
                print(str(self.result_list[index]) + "is on queue...")
                self.download_tif(str(self.result_list[index]))
                print(str(self.result_list[index]) + "is end\n\n===============")



if __name__ == "__main__":
    def configure(configpath):
        with open(configpath, 'r') as f:
            json_data = json.load(f)
        return json_data

    config = configure("config.json")

    eogcontrol = EOGnight(config)
    # print(eogcontrol.load_saved_file_list())
    # print(eogcontrol.load_website_file_list())

    # print(eogcontrol.is_new_file())
    print(eogcontrol.update())








