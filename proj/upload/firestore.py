# firestore test
from google.cloud import firestore
from google.cloud.firestore_v1beta1 import GeoPoint
import json


# 모든 waypoints를 업로드한다. 
def upload_all_waypoints(db):
    upload_subway_stations(db)
    upload_subway_gates(db)
    upload_bus_stations(db)
    upload_bicycle_stations(db)
    upload_car_stations(db)


# 지하철 역 waypoints
def upload_subway_stations(db):
    with open('./data/subway_station.json', 'r') as f:
        subway_station = json.loads(f.read())

    ref = db.collection('waypoints')
    for n in subway_station:
        lat = subway_station[n]['location']['latitude']
        lon = subway_station[n]['location']['longitude']
        point = GeoPoint(lat, lon)
        metadata = {}
        metadata.update({
            'fr_code': subway_station[n]['fr_code'],
            'line_num': subway_station[n]['line_num']
        })

        ref.document(n).set({
            'type': subway_station[n]['type'],
            'name': subway_station[n]['name'],
            'address': subway_station[n]['address'],
            'location': point,
            'metadata': metadata
        })


# 지하철 출구 waypoints
def upload_subway_gates(db):
    with open('./data/subway_gate.json', 'r') as f:
        subway_gates = json.loads(f.read())

    ref = db.collection('waypoints')
    for n in subway_gates:
        lat = subway_gates[n]['location']['latitude']
        lon = subway_gates[n]['location']['longitude']
        point = GeoPoint(lat, lon)

        ref.document(n).set({
            'type': subway_gates[n]['type'],
            'name': subway_gates[n]['name'],
            'address': subway_gates[n]['address'],
            'location': point
        })


# 버스 정류장 waypoints
def upload_bus_stations(db):
    with open('./data/bus_station.json', 'r') as f:
        bus_stations = json.loads(f.read())

    ref = db.collection('waypoints')
    for n in bus_stations:
        lat = bus_stations[n]['location']['latitude']
        lon = bus_stations[n]['location']['longitude']
        point = GeoPoint(lat, lon)
        metadata = {}
        metadata.update({
            'ars_id': bus_stations[n]['id']
        })

        ref.document(n).set({
            'type': bus_stations[n]['type'],
            'name': bus_stations[n]['name'],
            'address': bus_stations[n]['address'],
            'location': point,
            'metadata': metadata
        })


# 자전거 정류장 waypoints
def upload_bicycle_stations(db):
    with open('./data/bicycle_node.json', 'r') as f:
        bicycle_stations = json.loads(f.read())

    ref = db.collection('nodes')
    for n in bicycle_stations:
        lat = bicycle_stations[n]['location']['latitude']
        lon = bicycle_stations[n]['location']['longitude']
        point = GeoPoint(lat, lon)
        metadata = {}
        metadata.update({
            'id': bicycle_stations[n]['id']
        })

        ref.document(n).set({
            'type': bicycle_stations[n]['type'],
            'name': bicycle_stations[n]['name'],
            'address': bicycle_stations[n]['address'],
            'location': point,
            'metadata': metadata
        })


# 나눔카 정류장 waypoints
def upload_car_stations(db):
    with open('./data/car_node.json', 'r') as f:
        car_stations = json.loads(f.read())

    ref = db.collection('waypoints')
    for n in car_stations:
        lat = car_stations[n]['location']['latitude']
        lon = car_stations[n]['location']['longitude']
        point = GeoPoint(lat, lon)
        metadata = {}
        metadata.update({
            'id': car_stations[n]['id']
        })

        ref.document(n).set({
            'type': car_stations[n]['type'],
            'name': car_stations[n]['name'],
            'address': car_stations[n]['address'],
            'location': point,
            'metadata': metadata
        })


# 모든 라인을 업로드
def upload_all_lines(db):
    upload_bus_lines(db)
    upload_subway_lines(db)


def upload_bus_lines(db):
    with open('./data/bus_line.json', 'r') as f:
        bus_lines = json.loads(f.read())

    ref = db.collection('lines')
    for n in bus_lines:
        ref.document(n).set({
            'type': bus_lines[n]['type'],
            'name': bus_lines[n]['name'],
            'id': bus_lines[n]['id'],
        })


def upload_subway_lines(db):
    with open('./data/subway_line.json', 'r') as f:
        subway_lines = json.loads(f.read())

    ref = db.collection('lines')
    for n in subway_lines:
        ref.document(n).set({
            'type': subway_lines[n]['type'],
            'name': subway_lines[n]['name'],
            'id': subway_lines[n]['id'],
        })


# 모든 directions를 업로드
def upload_all_directions(db):
    # 지하철 링크
    upload_subway_links(db)
    # 지하철 환승
    upload_subway_transfer_links(db)
    # 지하철역 - 출구
    upload_gate_links(db)
    # 지전거
    upload_bicycle_links(db)
    # 버스
    upload_bus_links(db)
    # 걸어서 닿을 수 있는 거리
    upload_bus_walk_link(db)


# 지하철 링크
def upload_subway_links(db):
    with open('./data/subway_link.json', 'r') as f:
        subway_links = json.loads(f.read())

    ref = db.collection('directions')
    for n in subway_links:
        ref.document(n).set(subway_links[n])


# 지하철 환승
def upload_subway_transfer_links(db):
    with open('./data/subway_transfer.json', 'r') as f:
        subway_transfer_links = json.loads(f.read())

    ref = db.collection('directions')
    for n in subway_transfer_links:
        ref.document(n).set(subway_transfer_links[n])


# 지하철역 - 출구
def upload_gate_links(db):
    with open('./data/gate_link.json', 'r') as f:
        gate_links = json.loads(f.read())

    ref = db.collection('directions')
    for n in gate_links:
        ref.document(n).set(gate_links[n])


# 지전거
def upload_bicycle_links(db):
    with open('./data/bicycle_link.json', 'r') as f:
        bicycle_links = json.loads(f.read())

    ref = db.collection('directions')
    for n in bicycle_links:
        ref.document(n).set(bicycle_links[n])


# 버스
def upload_bus_links(db):
    with open('./data/bus_link.json', 'r') as f:
        bus_links = json.loads(f.read())

    ref = db.collection('directions')
    for n in bus_links:
        ref.document(n).set(bus_links[n])


# 걸어서 닿을 수 있는 거리
def upload_bus_walk_link(db):
    with open('./data/walk_link.json', 'r') as f:
        walk_links = json.loads(f.read())

    ref = db.collection('directions')
    for n in walk_links:
        ref.document(n).set(walk_links[n])


def run():
    db = firestore.Client()
    upload_all_waypoints(db)
    upload_all_lines(db)
    upload_all_directions(db)
