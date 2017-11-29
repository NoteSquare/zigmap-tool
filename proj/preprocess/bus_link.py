import json
import os
import glob
from bs4 import BeautifulSoup
from shortid import ShortId

sid = ShortId()
bus_to_key = {}


# read a file
def read_file(filename='./data/bus/100100001.xml'):
    with open(filename, 'r') as f:
        return f.read()


# save file
def write_file(data, filename='./data/bus_link.json'):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2, separators=(',', ': ')))


# read all files
def read_all_files(dirname='./data/bus'):
    path = dirname + '/*.xml'
    files = list(map(lambda x: os.path.basename(x), glob.glob(path)))
    data_list = []
    for filename in files:
        data_list.append(read_file('./data/bus/' + filename))
    return data_list


# make id by shortid
def make_key():
    return sid.generate()


# parse xml and convert data
def convert(data):
    soup = BeautifulSoup(data, 'lxml-xml')

    links = {}
    prev_id = 0
    for bus_station in soup.find_all('itemList'):
        # 미정차 정류장은 경로에서 제외
        if bus_station.find('stationNo').string == '미정차':
            continue
        # (경유) 쓰여있는 정류장도 제외
        if bus_station.find('stationNm').string.find('(경유)') >= 0:
            continue
        # 첫 정류장이면 제외
        route_id = bus_station.find('busRouteId').string
        station_id = bus_station.find('station').string
        if prev_id == 0:
            prev_id = station_id
            continue

        speed = int(bus_station.find('sectSpd').string)
        if speed == 0:
            speed = 10
        distance = float(bus_station.find('fullSectDist').string)
        time = float('%0.2f' % (distance / speed / 1000 * 60))

        links.update({
            make_key(): {
                'from': bus_to_key[prev_id],
                'to': bus_to_key[station_id],
                'time': time,
                'distance': distance,
                'type': 'bus',
                'lineId': route_id
            }
        })
        prev_id = station_id
    return links


def run():
    global bus_to_key
    with open('./data/bus_station_to_key.json', 'r') as f:
        bus_to_key.update(json.loads(f.read()))

    data_list = read_all_files()
    links = {}
    for data in data_list:
        links.update(convert(data))
    write_file(links)
