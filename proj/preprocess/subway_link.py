import json
from shortid import ShortId

sid = ShortId()

stations = {}
lines = {}


def read_file(filename='./data/subway_link_data.json'):
    with open(filename, 'r') as f:
        return json.loads(f.read())


def write_file(data, filename='./data/subway_link.json'):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2, separators=(',', ': ')))


def get_subway_node(filename):
    subway_nodes = {}
    return subway_nodes


def convert(data):
    buf = {}
    for d in data:
        id1 = get_station_id(d['from'], d['line'])
        id2 = get_station_id(d['to'], d['line'])
        time = d['time']
        line = d['line']
        buf.update(make_link(id1, id2, time, line))
        buf.update(make_link(id2, id1, time, line))
    return buf


def make_link(id1, id2, time, line_id='line_id'):
    return {
        sid.generate(): {
            'type': 'subway',
            'from': id1,
            'to': id2,
            'time': time,
            'lineId': line_id
        }
    }


def get_station_id(name, line_num):
    for s in stations:
        if stations[s]['name'] == name and stations[s]['line_num'] == line_num:
            return s
    return None


def run():
    global stations
    global lines

    with open('./data/subway_station.json', 'r') as f:
        stations.update(json.loads(f.read()))
    with open('./data/subway_line.json', 'r') as f:
        lines.update(json.loads(f.read()))

    data = read_file('./data/subway_link_data.json')
    links = convert(data)
    write_file(links)
