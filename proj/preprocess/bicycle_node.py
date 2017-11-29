import json
from shortid import ShortId

sid = ShortId()


# 따릉이 시트에서 데이터 뽑아내기
def read_file(filename='./data/bicycles.json'):
    with open(filename, 'r') as f:
        return json.loads(f.read())


# 갈무리 한 정보 다시 파일로 저장하기
def write_file(data, filename='./data/bicycle_node.json'):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False, separators=(',', ': ')))


# 디비 양식에 맞게 데이터 뽑아내기
def convert(data):
    ret = {}
    for d in data['DATA']:
        # 새주소에 구가 겹치면 삭제
        borough = d['ADDR_GU'].strip()  # 구
        address = d['NEW_ADDR'].replace(borough, '').strip()

        addr = '서울특별시 %s %s' % (borough, address)
        ret.update({
            sid.generate(): {
                'address': addr,
                'name': d['CONTENT_NM'].strip(),
                'location': {
                    'latitude': d['LATITUDE'],
                    'longitude': d['LONGITUDE']
                },
                'id': d['CONTENT_ID'],
                'type': 'sharing_bicycle_01'
            }
        })
    return ret


def run():
    data = read_file()
    bicycles = convert(data)
    write_file(bicycles)
