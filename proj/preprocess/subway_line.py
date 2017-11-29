import json
from shortid import ShortId

sid = ShortId()


def get_line_names():
    subway_line_list = ['1호선', '2호선', '3호선', '4호선', '5호선',
                        '6호선', '7호선', '8호선', '9호선', '공항철도',
                        '경의중앙선', '신분당선', '경강선', '경춘선', '용인경전철',
                        '인천1호선', '인천2호선', '분당선', '수인선', '의정부경전철',
                        '우이신설']
    return subway_line_list


def get_line_numbers():
    subway_line_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9',
                           'A', 'K', 'S', 'KK', 'G', 'E', 'I', 'I2',
                           'B', 'SU', 'U', 'UI']
    return subway_line_numbers


def convert(names, line_numbers):
    lines = {}
    for i in range(0, len(names)):
        lines.update({
            sid.generate(): {
                'name': names[i],
                'type': 'subway',
                'id': line_numbers[i]
            }
        })
    return lines


def write_file(data, filename='./data/subway_line.json'):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2, separators=(',', ': ')))


def run():
    names = get_line_names()
    line_numbers = get_line_numbers()
    lines = convert(names, line_numbers)
    write_file(lines)
