import json
import os
from bs4 import BeautifulSoup
from shortid import ShortId
import requests

from config import config


DATA_SERVICE_KEY = config.PUBLIC_DATA_PORTAL_SERVICE_KEY
sid = ShortId()


def read_file(filename='./data/buses.xml'):
    with open(filename, 'r') as f:
        return f.read()


def convert(data):
    soup = BeautifulSoup(data, 'lxml-xml')

    results = {}
    for d in soup.find_all('itemList'):
        results.update({
            sid.generate(): {
                'id': d.find('busRouteId').string,
                'name': d.find('busRouteNm').string,
                'type': 'bus'
            }
        })
    return results


def write_file(data, filename='./data/bus_line.json'):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2, separators=(',', ': ')))


def get_all_bus_line(path):
    if os.path.exists(path):
        data = read_file(path)
    else:
        url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getBusRouteList?serviceKey=%s' % DATA_SERVICE_KEY
        req = requests.get(url)
        data = req.text

        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(path, 'w') as f:
            f.write(req.text)
    return data


def run():
    # 파일이 없으면 api 요청해서 결과값 저장하기
    filename = './data/buses.xml'
    data = get_all_bus_line(filename)
    lines = convert(data)
    write_file(lines)
