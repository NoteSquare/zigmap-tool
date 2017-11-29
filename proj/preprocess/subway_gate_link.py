import json
from shortid import ShortId

sid = ShortId()
stations = {}


def make_gate_link():
    with open('./data/subway_gate.json', 'r') as f:
        gates = json.loads(f.read())

    buf = {}
    for g in gates:
        name = gates[g]['name'].split()[0]
        name = name[:len(name)-1]
        for s in get_station_ids(name):
            buf.update(make_link(g, s))
            buf.update(make_link(s, g))
    with open('./data/gate_link.json', 'w') as f:
        f.write(json.dumps(buf, ensure_ascii=False, indent=2, separators=(',', ': ')))


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
    make_gate_link()
