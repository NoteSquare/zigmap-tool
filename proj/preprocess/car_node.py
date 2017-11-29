import json
import os
import requests
from shortid import ShortId

from config import config

sid = ShortId()
SEOUL_SERVICE_KEY = config.SEOUL_OPEN_DATA_PLAZA_SERVICE_KEY


# 파일 읽어오기
def read_file(filename='./data/cars.json'):
    with open(filename, 'r') as f:
        return json.loads(f.read())


# 파일로 저장
def write_file(data, filename='./data/car_node.json'):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2, separators=(',', ': ')))


# 키 생성하기 (short id module)
def make_key():
    return sid.generate()


# 디비 양식에 맞게 데이터 뽑아내기
def convert(data):
    ret = {}
    codes = {}
    for d in data:
        code = d['POSITN_CD']
        if code in codes:
            ret[codes[code]]['type'].append(get_type_name(d['ENTRPS']))
            continue
        key = make_key()
        tmp = {
            'address': d['ADRES'],
            'name': d['POSITN_NM'],
            'location': {
                'latitude': d['LA'],
                'longitude': d['LO']
            },
            'type': [get_type_name(d['ENTRPS'])],
            'id': d['POSITN_CD']
        }
        ret.update({key: tmp})
        codes.update({code: key})

    return ret


# 타입 이름 분류하기
def get_type_name(car_type):
    prefix = 'sharing_car_'

    if car_type == '쏘카':
        number = '01'
    elif car_type == '그린카':
        number = '02'
    elif car_type == '이지고':
        number = '03'
    else:
        number = '00'

    return prefix + number


def get_all_car_info(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.loads(f.read())
    else:
        url = 'http://openapi.seoul.go.kr:8088/%s/json/NanumcarSpotList/1/1000' % SEOUL_SERVICE_KEY
        req = requests.get(url)
        data = json.loads(req.text)

        url = 'http://openapi.seoul.go.kr:8088/%s/json/NanumcarSpotList/1001/1777' % SEOUL_SERVICE_KEY
        req = requests.get(url)
        data2 = json.loads(req.text)

        data['NanumcarSpotList']['row'].extend(data2['NanumcarSpotList']['row'])

        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        write_file(data, path)
    cars = data['NanumcarSpotList']['row']
    return cars


def run():
    filename = './data/cars.json'
    data = get_all_car_info(filename)
    cars = convert(data)
    write_file(cars)
