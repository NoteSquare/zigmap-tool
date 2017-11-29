import json

from shortid import ShortId
from config import config

sid = ShortId()

DATA_SERVICE_KEY = config.PUBLIC_DATA_PORTAL_SERVICE_KEY
SEOUL_SERVICE_KEY = config.SEOUL_OPEN_DATA_PLAZA_SERVICE_KEY
KAKAO_REST_KEY = config.KAKAO_REST_KEY


def read_file(filename='./data/stations.json'):
    with open(filename, 'r') as f:
        buf = json.loads(f.read())
    return buf['DATA']


# 모든 지하철 역에 대해서, 위도, 경도, 이름 등을 뽑아냄
def convert(data):
    results = {}
    for d in data:
        results.update({
            make_key(): {
                'type': 'subway',
                'location': {
                    'latitude': float(d['XPOINT_WGS']) if d['XPOINT_WGS'] else 0,
                    'longitude': float(d['YPOINT_WGS']) if d['YPOINT_WGS'] else 0,
                },
                'name': d['STATION_NM'] if d['STATION_NM'] else '',
                'address': '',
                'fr_code': d['FR_CODE'],
                'line_num': d['LINE_NUM']
            }
        })
    return results


def write_file(data, filename='./data/subway_station.json'):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2, separators=(',', ': ')))


# make key by short id
def make_key():
    return sid.generate()


# 위도, 경도가 비어있는 지하철 역 출력
def find_emtpy_items():
    with open('./data/subway_station.json', 'r') as f:
        data = json.loads(f.read())

    buf = []
    for d in data:
        a = data[d]['location']['latitude']
        b = data[d]['location']['longitude']
        if a * b == 0:
            buf.append((data[d]['name'], data[d]['line_num']))
    return buf


def transfer_station(stations):
    buf = {}
    # 이름이 같으면 환승역
    for s in stations:
        name = stations[s]['name']
        if name == '':
            continue
        elif name in buf:
            buf[name].append(s)
        else:
            buf.update({name: [s]})
    return buf


def connect(data):
    names = list(filter(lambda x: len(data[x]) >= 2, data))

    buf = {}
    for n in names:
        for i in range(0, len(data[n]) - 1):
            for j in range(i + 1, len(data[n])):
                buf.update({
                    make_key(): {
                        'from': data[n][i],
                        'to': data[n][j],
                        'time': 5,
                        'lineId': 'line_id',
                        'type': 'transfer'
                    }
                })
                buf.update({
                    make_key(): {
                        'from': data[n][j],
                        'to': data[n][i],
                        'time': 5,
                        'lineId': 'line_id',
                        'type': 'transfer'
                    }
                })
    return buf


def run():
    data = read_file(filename='./data/stations.json')
    # 역 정보 파일에 기록하기
    stations = convert(data)
    write_file(stations)

    # 환승정보 입력하기
    with open('./data/subway_station.json', 'r') as f:
        stations = json.loads(f.read())
    transfer_stations = transfer_station(stations)
    connected = connect(transfer_stations)
    write_file(connected, './data/subway_transfer.json')
