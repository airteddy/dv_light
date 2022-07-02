# main.py
import json
import tqdm
import glob
import cv2

from util.eogdata import EOGnight
from util.geocoding import osmgeo, navergeo
from util.crop import crop_by_coords, crop_korea


def main(config):
    # 1. 실행시마다 새로운 자료 있는지 확인
    # 2. 자료가 있으면 다운로드 후 EOGimages에 저장/ 없으면 바로 다음 진행
    # 3. 사용자로부터 주소나 좌표, 날짜, 기간을 받을 준비
    # 4. 받은 값 유효화 검사 -> 지오코딩
    # 5. 지오코딩 결과값을 토대로 tif를 불러오고 저장
    
    # 1. 새로운 자료 있는지확인
    # 2. 자료가 잇으면 다운로드 후 EOGimages에 저장 / 없으면 바로 다음 진행
    eogcontrol = EOGnight(config)
    eogcontrol.update() 

    # 3. 사용자로부터 주소나 좌표, 날짜, 기간을 받을 준비 
    osmcontrol = osmgeo(config)
    lat, lon = osmcontrol.findloc(input("주소 입력 : "))
    
    # 4. 좌표 유효성 검사
    assert lat is not None
    assert lon is not None

    # 5. tif 읽기
    tif = eogcontrol.read_tif_date('20220623')
    tif_crop = crop_by_coords(tif, int(lat), int(lon), int(3))
    tif_korea = crop_korea(tif)

    # 6. tif 시각화


    # 7. 결과값 저장




    




    
def configure(configpath):
    with open(configpath, 'r') as f:
        json_data = json.load(f)
    return json_data

if __name__ == "__main__":
    print("Start dv")
    print("Read config...")

    config = configure("config.json")

    main(config)

