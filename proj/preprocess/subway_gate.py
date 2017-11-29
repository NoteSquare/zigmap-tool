import json
import requests
import os

from shortid import ShortId
from config import config

sid = ShortId()

DATA_SERVICE_KEY = config.PUBLIC_DATA_PORTAL_SERVICE_KEY
SEOUL_SERVICE_KEY = config.SEOUL_OPEN_DATA_PLAZA_SERVICE_KEY
KAKAO_REST_KEY = config.KAKAO_REST_KEY


# make key by short id
def make_key():
    return sid.generate()


# 지하철 역 중복없이 받아오기
def get_stations(filename):
    with open(filename, 'r') as f:
        buf = json.loads(f.read())
    data = buf['DATA']
    return list(set(map(lambda x: x['STATION_NM'], data)))


# 역 이름으로 출구 정보 조회
# data/subway/역이름.json
def get_gates(station_name):
    path = './data/subway/%s.json' % station_name
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.loads(f.read())
    else:
        url = 'http://swopenapi.seoul.go.kr/api/subway/%s/json/gateInfo/0/30/%s' % (SEOUL_SERVICE_KEY, station_name)
        req = requests.get(url)
        data = json.loads(req.text)
        # 파일이 없으면 새로 저장
        # 폴더가 없으면 만들기
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(path, 'w') as f:
            f.write(json.dumps(data, ensure_ascii=False, separators=(',', ': '), indent=2))

    try:
        return list(map(lambda x: '%s역 %s %s번출구' % (station_name, x['subwayNm'], x['ectrcNo']), data['gateList']))
    except KeyError:
        return []


# 모든 지하철 역 이름으로 검색해서 몇 번 출구까지 있는지 확인
def get_gates_of_all_stations(filename='./data/stations.json'):
    stations = get_stations(filename)
    ret = []
    for station in stations:
        ret.extend(get_gates(station))
    return ret
    # return list(map(lambda x: get_gates(x), stations))


# kakao에서 출구 번호 검색하기
def get_gate_info(gatename):
    path = './data/subway/gates/%s.json' % gatename

    if os.path.exists(path):
        with open(path, 'r') as f:
            data = f.read()
    else:
        url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query=%s' % gatename
        headers = {'Authorization': 'KakaoAK %s' % KAKAO_REST_KEY}
        req = requests.get(url, headers=headers)
        data = req.text

        # 파일이 없으면 새로 저장
        # 폴더가 없으면 만들기
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(path, 'w') as f:
            f.write(json.dumps(json.loads(req.text), ensure_ascii=False, separators=(',', ': '), indent=2))
    return data


# 검색 결과로부터 지하철 출구 정보 만들어내기
def convert(gatename):
    ret = {}
    result = json.loads(get_gate_info(gatename))
    for r in result['documents']:
        if r['place_name'] == gatename:
            ret.update({
                'name': gatename,
                'type': 'subway_gate',
                'location': {
                    'latitude': float(r['y']),
                    'longitude': float(r['x'])
                },
                'address': r['address_name']
            })
            break
    if len(ret) == 0:
        return None
    else:
        return ret


def write_file(data, filename='./data/subway_gate.json'):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False, separators=(',', ': '), indent=2))


def run():
    # 출구 정보 기록
    gates = get_gates_of_all_stations(filename='./data/stations.json')
    buf = {}
    for gatename in gates:
        gate = convert(gatename)
        if gate is None:
            continue
        buf.update({make_key(): gate})
    write_file(buf)
