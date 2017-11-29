import json
from math import sin, cos, sqrt, atan2, radians
from shortid import ShortId

sid = ShortId()


# http://itmemo.tistory.com/383
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


def read_file(filename='./data/bicycle_node.json'):
    with open(filename, 'r') as f:
        return json.loads(f.read())


def write_file(data, filename='./data/bicycle_link.json'):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2, separators=(',', ': ')))


def convert(data):
    buf = {}
    key_list = list(data.keys())
    for i in range(0, len(key_list) - 1):
        for j in range(i + 1, len(key_list)):
            x1 = data[key_list[i]]['location']['latitude']
            y1 = data[key_list[i]]['location']['longitude']
            x2 = data[key_list[j]]['location']['latitude']
            y2 = data[key_list[j]]['location']['longitude']

            d = distance(x1, y1, x2, y2)
            time = d / 166  # 10km/h, 166m/min

            buf.update(make_link(key_list[i], key_list[j], time))
            buf.update(make_link(key_list[j], key_list[i], time))
    return buf


def make_link(id1, id2, time):
    return {
        sid.generate(): {
            'type': 'bicycle',
            'from': id1,
            'to': id2,
            'time': time,
            'lineId': ''
        }
    }


def run():
    data = read_file(filename='./data/bicycle_node.json')
    links = convert(data)
    write_file(links, filename='./data/bicycle_link.json')
