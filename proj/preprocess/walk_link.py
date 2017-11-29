import json
import time
from math import sin, cos, sqrt, atan2, radians, ceil
from shortid import ShortId

sid = ShortId()

stations = {}


# http://itmemo.tistory.com/383
# x1 = 37.556041319821745
# y1 = 126.92299742410859
# x2 = 37.55630421267684
# y2 = 126.92270289663293
def distance(x1, y1, x2, y2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(x1)
    lon1 = radians(y1)
    lat2 = radians(x2)
    lon2 = radians(y2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c * 1000  # meter
    return distance


def read_nodes():
    # 지하쳘역
    # 지하철역 출구
    with open('./data/subway_gate.json', 'r') as f:
        gates = json.loads(f.read())
    # 버스 정류장
    with open('./data/bus_station.json', 'r') as f:
        buses = json.loads(f.read())
    # 따릉이 정류장
    with open('./data/bicycle_node.json', 'r') as f:
        bicycles = json.loads(f.read())
    # 나눔카
    with open('./data/car_node.json', 'r') as f:
        cars = json.loads(f.read())

    all_node = {}
    all_node.update(gates)
    all_node.update(buses)
    all_node.update(bicycles)
    all_node.update(cars)

    return all_node


def calculate_links(nodes):
    links = {}
    keys = list(nodes.keys())

    # count time
    start_time = time.time()
    complete = len(keys)
    percent = complete // 100

    for i in range(0, len(keys)):
        if i % percent == 1:
            t = time.time() - start_time  # elapsed time
            remaining_time = ceil((complete - i) * t / i)
            total_time = t + remaining_time
            print('%d%%, %02d:%02d, %02d:%02d' % (int(i / complete * 100),
                  remaining_time // 60, remaining_time % 60,
                  total_time // 60, total_time % 60))

        for j in range(i+1, len(keys)):
            try:
                a = nodes[keys[i]]
                b = nodes[keys[j]]

                # 지하철 역 출구끼리 연결되는 경우
                if a['type'] == 'subway_gate' and b['type'] == 'subway_gate':
                    continue

                # 지하철 역이 연결되는 경우
                if a['type'] == 'subway' or b['type'] == 'subway':
                    continue

                x1 = float(a['location']['latitude'])
                y1 = float(a['location']['longitude'])
                x2 = float(b['location']['latitude'])
                y2 = float(b['location']['longitude'])
                d = distance(x1, y1, x2, y2)
                # 300m 이상이면 추가히지 않음
                if d >= 300:
                    continue

                t = ceil(d * 0.015)
                links.update(make_link(keys[i], keys[j], link_time=t))
                links.update(make_link(keys[j], keys[i], link_time=t))

            except KeyError:
                continue
    return links


def write_file(data, filename='./data/walk_link.json'):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2, separators=(',', ': ')))


def get_station_ids(name):
    return list(filter(lambda x: stations[x]['name'] == name, stations.keys()))


def make_link(id1, id2, link_time=5, link_type='walk', line_id='line_id'):
    return {
        sid.generate(): {
            'type': link_type,
            'from': id1,
            'to': id2,
            'time': link_time,
            'lineId': line_id
        }
    }


def run():
    global stations

    with open('./data/subway_station.json', 'r') as f:
        stations.update(json.loads(f.read()))

    nodes = read_nodes()
    links = calculate_links(nodes)
    write_file(links)
