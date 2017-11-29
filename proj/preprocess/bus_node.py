import requests
import json
import os
from bs4 import BeautifulSoup
from shortid import ShortId
from config import config

sid = ShortId()
keys = {}

DATA_SERVICE_KEY = config.PUBLIC_DATA_PORTAL_SERVICE_KEY
SEOUL_SERVICE_KEY = config.SEOUL_OPEN_DATA_PLAZA_SERVICE_KEY


def write_file(data, filename):
    with open(filename, 'w') as f:
        f.write(data)


def get_stations(bus_id):
    path = './data/bus/%s.xml' % bus_id
    if os.path.exists(path):
        # 파일이 있으면 파일에서 읽어오기
        with open(path, 'r') as f:
            data = f.read()
    else:
        # 파일이 없으면 새로 요청하기
        url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute'
        params = {}
        params.update({'serviceKey': DATA_SERVICE_KEY})
        params.update({'busRouteId': bus_id})
        query = '&'.join(list(map(lambda x: x + '=' + params[x], params.keys())))
        req = requests.get(url + '?' + query)
        data = req.text

    soup = BeautifulSoup(data, 'lxml-xml')

    stations = {}
    for bus_station in soup.find_all('itemList'):
        key = sid.generate()
        latitude = float(bus_station.find('gpsY').string)
        longitude = float(bus_station.find('gpsX').string)
        stations.update({
            key: {
                'type': 'bus',
                'address': '',
                'name': bus_station.find('stationNm').string,
                'location': {
                    'latitude': latitude if isValidLatitude else 0,
                    'longitude': longitude if isValidLongitude else 0
                },
                'id': bus_station.find('arsId').string,
                'stationId': bus_station.find('station').string
            }
        })
        # 노선id, 정류장id 에 key값 추가
        keys.update({bus_station.find('station').string: key})

    # save xml file
    if not os.path.exists(path):
        write_file(req.text, path)
    return stations


def isValidLatitude(latitude):
    return latitude <= 90 and latitude >= -90


def isValidLongitude(longitude):
    return longitude <= 180 and longitude >= -180


def get_all_stations(filename):
    numbers = get_bus_numbers(filename)
    all_stations = {}
    station_ids = set()
    for n in numbers:
        stations = get_stations(n)
        for s in stations:
            # 중복제거하기
            if stations[s]['stationId'] in station_ids:
                continue
            station_ids.add(stations[s]['stationId'])
            all_stations.update({s: stations[s]})
    return all_stations


def get_bus_numbers(filename):
    with open(filename, 'r') as f:
        buf = f.read()
    soup = BeautifulSoup(buf, 'lxml-xml')
    return list(map(lambda x: x.string, soup.find_all('busRouteId')))


def run():
    filename = './data/buses.xml'
    all_stations = get_all_stations(filename)
    with open('./data/bus_station.json', 'w') as f:
        f.write(json.dumps(all_stations, ensure_ascii=False, indent=2, separators=(',', ':')))

    with open('./data/bus_station_to_key.json', 'w') as f:
        f.write(json.dumps(keys, ensure_ascii=False, indent=2, separators=(',', ':')))
