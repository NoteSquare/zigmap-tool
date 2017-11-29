# zigmap-tool

찍맵 Command Line Interface (CLI) Tool 입니다. 

* 새로운 대중교통 정보를 서버에 업데이트 할 수 있습니다. 


# Installation

[Github repository](https://github.com/NoteSquare/zigmap-tool)에서 프로젝트를 clone하거나, 파일을 다운로드합니다. 

```bash
git clone https://github.com/NoteSquare/zigmap-tool.git
```

그리고 [Python3](https://www.python.org/downloads/)와 [pip3](https://pypi.python.org/pypi/pip)가 설치되어 있어야 합니다. 

다음 명령어를 입력해 의존 모듈을 설치합니다. 

```bash
pip3 install -r requirements.txt
```

다음 명령어로 zigmap tool 을 실행합니다. 

```bash
python3 run.py
```

데이터베이스 서버는 [Firebase Cloud Firestore](https://firebase.google.com/docs/firestore/)를 사용합니다. 

[Firebase](https://firebase.google.com/?hl=ko) 공식 문서에서 자세한 [설정 내용](https://firebase.google.com/docs/admin/setup?authuser=0)을 참고할 수 있습니다. 

# Commands

찍맵 CLI에서 사용 가능한 옵션 목록은 다음과 같습니다. 
(환경에 따라 2시간 정도 실행시간이 소요됩니다.)

## Options

Option | Description
------ | -----------
**--proj** | 실행할 프로젝트 이름을 입력합니다. (preprocess, upload)

- preprocess : 공공API를 통해서 데이터를 수집하고, 파싱하는 과정입니다. 
- upload : Firebase cloud Firestore에 데이터를 저장합니다. 

## Samples

실행 예시입니다. 

```bash
python run.py --proj preprocess     # preprocess 실행
```

```bash
python run.py --proj upload         # upload 실행 (Firebase cloud Firestore가 연결되어 있어야함)
```

```bash
python run.py                       # 두 프로젝트 차례로 실행
```

## 필요한 파일 (수동생성)

`python run.py --proj preprocess` 명령을 위해 필요한 파일들입니다. API로 제공되지 않아 직접 파일을 다운로드하거나 편집하여 만들어낸 결과물입니다. `/data` 경로 아래에 위치해야 합니다. 

File | Description
---- | -----------
stations.json | 서울 열린 데이터 광장에서 제공하는 지하철 역 데이터입니다. [서울시 역코드로 지하철역 위치 조회](https://www.data.go.kr/subMain.jsp#/L3B1YnIvcG90L215cC9Jcm9zTXlQYWdlL29wZW5EZXZEZXRhaWxQYWdlJEBeMDgyTTAwMDAxMzBeTTAwMDAxMzUkQF5wdWJsaWNEYXRhRGV0YWlsUGs9dWRkaTplZGU4Y2E4Yy05NGJjLTQ5NTktYWFiOS1mNTAyMTAzN2I0NmYkQF5wcmN1c2VSZXFzdFNlcU5vPTI3MjkxMTckQF5yZXFzdFN0ZXBDb2RlPVNUQ0QwMQ==) 데이터셋을 JSON 형식으로 다운로드한 파일입니다.
bicycles.json | 서울 열린 데이터 광장에서 제공하는 따릉이 대여소 정보입니다. [서울시 공공자전거 대여소 정보](http://data.seoul.go.kr/openinf/sheetview.jsp?infId=OA-13252&tMenu=11) 데이터셋을 JSON 형식으로 다운로드한 파일입니다.
subway_link_data.json | 두 지하철 역을 연결하는 노선 이름과 걸리는 시간이 담긴 정보입니다. ([1~4호선](http://data.seoul.go.kr/openinf/sheetview.jsp?infId=OA-12034), [5~8호선](http://www.smrt.co.kr/program/board/detail.jsp?boardTypeID=26&searchSelect=&keyWord=%EC%8B%9C%EA%B0%84&boardCategory=%EC%97%B4%EC%B0%A8%EC%8B%9C%EA%B0%81¤tPage=1&menuID=001003010&finishIsYN=&boardID=8501&mode=detail ), [코레일](http://www.letskorail.com/ebizcom/cs/guide/guide/guide11.do), [인천지하철](https://www.ictr.or.kr/information/trafficLeadTbl.asp), [신분당선](http://www.shinbundang.co.kr/index.jsp) 등)

### stations.json
```json
{
    "DESCRIPTION": {
        "YPOINT": "Y좌표",
        "XPOINT_WGS": "X좌표(WGS)",
        "STATION_NM": "전철역명",
        "STATION_CD": "전철역코드",
        "LINE_NUM": "호선",
        "FR_CODE": "외부코드",
        "CYBER_ST_CODE": "사이버스테이션",
        "XPOINT": "X좌표",
        "YPOINT_WGS": "Y좌표(WGS)"
    },
    "DATA": [
        {
            "YPOINT": "1121815",
            "XPOINT_WGS": "37.540693",
            "STATION_NM": "건대입구",
            "STATION_CD": "2729",
            "LINE_NUM": "7",
            "FR_CODE": "727",
            "CYBER_ST_CODE": "0212",
            "XPOINT": "515365",
            "YPOINT_WGS": "127.070230"
        }
    ]
}
```
### bicycles.json
```json
{
    "DESCRIPTION" : {
        "NEW_ADDR":"대여소 주소",
        "CONTENT_ID":"대여소번호",
        "ADDR_GU":"구분",
        "LONGITUDE":"경도",
        "CRADLE_COUNT":"거치대수",
        "LATITUDE":"위도",
        "CONTENT_NM":"대여소명"
    },
    "DATA" : [
        {
            "NEW_ADDR":"화양동 169-1",
            "CONTENT_ID":"500",
            "ADDR_GU":"광진구",
            "LONGITUDE":127.074272,
            "CRADLE_COUNT":10,
            "LATITUDE":37.54707,
            "CONTENT_NM":"어린이대공원역 3번출구 앞"
        }
    ]
}
```
### subway_link_data.json
```json
[
    {
        "from": "오금",
        "to": "경찰병원",
        "time": 1.5,
        "line": 3
    }
]
```


## 필요한 파일 (자동생성)

`python run.py --proj prepreocess` 실행 과정에서 필요한 파일들입니다. `/data` 경로 아래에 위치합니다. 


File | Description
---- | -----------
buses.xml | 공공데이터포털에서 제공하는 데이터입니다. 서울특별시가 제공하는 [노선정보조회 서비스 - 노선번호에 해당하는 노선 목록 조회(getBusRouteList)](https://www.data.go.kr/subMain.jsp#/L3B1YnIvcG90L215cC9Jcm9zTXlQYWdlL29wZW5EZXZEZXRhaWxQYWdlJEBeMDgyTTAwMDAxMzBeTTAwMDAxMzUkQF5wdWJsaWNEYXRhRGV0YWlsUGs9dWRkaTplZGU4Y2E4Yy05NGJjLTQ5NTktYWFiOS1mNTAyMTAzN2I0NmYkQF5wcmN1c2VSZXFzdFNlcU5vPTI3MjkxMTckQF5yZXFzdFN0ZXBDb2RlPVNUQ0QwMQ==)의 결과값입니다. 
/bus/*.xml | buses.xml 에 언급된 모든 버스 노선에 대해서 [노선정보조회 서비스 - 노선 기본정보 조회(getRouteInfoItem)](https://www.data.go.kr/subMain.jsp#/L3B1YnIvcG90L215cC9Jcm9zTXlQYWdlL29wZW5EZXZEZXRhaWxQYWdlJEBeMDgyTTAwMDAxMzBeTTAwMDAxMzUkQF5wdWJsaWNEYXRhRGV0YWlsUGs9dWRkaTplZGU4Y2E4Yy05NGJjLTQ5NTktYWFiOS1mNTAyMTAzN2I0NmYkQF5wcmN1c2VSZXFzdFNlcU5vPTI3MjkxMTckQF5yZXFzdFN0ZXBDb2RlPVNUQ0QwMQ==)를 요청한 결과값입니다. 
/subway/*.json | 모든 지하철 역에 대한 세부정보 조회 요청의 결과값 중 출구정보(gateList)입니다. 
/subway/gate/*.json | 모든 지하철 역에 대한 [지하철역 출구 정보 조회](https://developers.kakao.com/docs/restapi/local#키워드-검색) 요청의 결과값입니다. 
cars.json | 서울 열린 데이터 광장에서 제공하는 [나눔카 대여소 정보](http://data.seoul.go.kr/openinf/board/community.jsp?bbs_cd=10001&seq=373&tMenu=35)입니다. 

### buses.xml
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes">
<ServiceResult>
    <comMsgHeader/>
    <msgHeader>
        <headerCd>0</headerCd>
        <headerMsg>정상적으로 처리되었습니다.</headerMsg>
        <itemCount>0</itemCount>
        </msgHeader><msgBody>
        <itemList>
            <busRouteId>100000010</busRouteId>
            <busRouteNm>12345</busRouteNm>
            <corpNm>BMS온라인메뉴얼  --</corpNm>
            <edStationNm>청와대분수대앞</edStationNm>
            <firstBusTm>20171124040000</firstBusTm>
            <firstLowTm>              </firstLowTm>
            <lastBusTm>20171124230000</lastBusTm>
            <lastBusYn> </lastBusYn>
            <lastLowTm>              </lastLowTm>
            <length>0</length>
            <routeType>0</routeType>
            <stStationNm>경복고교</stStationNm>
            <term>10</term>
        </itemList>
    </msgHeader>
</ServiceResult>
```

### /bus/*.xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes">
<ServiceResult>
    <comMsgHeader/>
    <msgHeader>
        <headerCd>0</headerCd>
        <headerMsg>정상적으로 처리되었습니다.</headerMsg>
        <itemCount>0</itemCount>
    </msgHeader>
    <msgBody>
        <itemList>
            <arsId>03320</arsId>
            <beginTm>07:00</beginTm>
            <busRouteId>100100001</busRouteId>
            <busRouteNm>02</busRouteNm>
            <direction>남산서울타워</direction>
            <gpsX>126.9904431246</gpsX>
            <gpsY>37.5511572043</gpsY>
            <lastTm>23:30</lastTm>
            <posX>199155.61435325549</posX>
            <posY>450187.3153560101</posY>
            <routeType>5</routeType>
            <sectSpd>0</sectSpd>
            <section>0</section>
            <seq>1</seq>
            <station>102000226</station>
            <stationNm>남산서울타워</stationNm>
            <stationNo>03320</stationNo>
            <transYn>Y</transYn>
            <fullSectDist>0</fullSectDist>
            <trnstnid>102000226</trnstnid>
        </itemList>
    </msgBody>
</ServiceResult>
```

### /subway/*.json

```json
{
    "gateList": [
        {
            "beginRow": null,
            "endRow": null,
            "curPage": null,
            "pageRow": null,
            "totalCount": 3,
            "rowNum": 1,
            "selectedCount": 3,
            "statnId": "1001000109",
            "statnNm": "가능",
            "ectrcNo": "1",
            "subwayId": "1001",
            "subwayNm": "1호선",
            "ectrcCnt": "3",
            "cfrBuild": "가능1동주민센터,의정부중학교,의정부여자중학교,의정부여자고등학교,의정부경찰서,가능초등학교",
            "subwayXcnts": null,
            "subwayYcnts": null,
            "ectrcId": null
        }
    ]
}
```

### /subway/gate/*.json

```json
{
    "meta": {
        "same_name": {
            "region": [],
            "keyword": "가능역 1호선 1번출구",
            "selected_region": ""
        },
        "pageable_count": 1,
        "total_count": 1,
        "is_end": true
    },
    "documents": [
        {
            "place_url": "http://place.map.daum.net/8115720",
            "category_group_name": "",
            "place_name": "가능역 1호선 1번출구",
            "distance": "",
            "address_name": "경기 의정부시 가능동",
            "road_address_name": "",
            "id": "8115720",
            "phone": "",
            "category_group_code": "",
            "category_name": "교통,수송 > 지하철,전철",
            "x": "127.04411657797226",
            "y": "37.748356728417804"
        }
    ]
}
```
### cars.json

```json
{
    "NanumcarSpotList": {
        "list_total_count": 1777,
        "RESULT": {
            "CODE": "INFO-000",
            "MESSAGE": "정상 처리되었습니다"
        },
        "row": [
            {
                "ENTRPS": "그린카",
                "LA": 37.44437,
                "LO": 126.9042,
                "POSITN_CD": "1841",
                "ELCTYVHCLE_AT": "GA",
                "ADRES": "서울 금천구 시흥동 939-4",
                "POSITN_NM": "GS칼텍스 일신"
            }
        ]
    }
}
```

## 만들어지는 파일

`python run.py --proj preprocess`를 실행하고 나서 만들어지는 파일들입니다. `/data` 경로 아래에 위치합니다. 

File | Description
---- | -----------
bicycle_link.json | 자전거 경로
bicycle_node.json | 자전거 대여소
bus_line.json | 버스 노선
bus_link.json | 버스 경로
bus_station_to_key.json | 버스 정류장 mapping table
bus_station.json | 버스 정류장
car_node.json | 나눔카 대여소
gate_link.json | 지하철 역, 지하철 역 출구 사이의 경로
subway_gate.json | 지하철 역 출구
subway_line.json | 지하철 노선
subway_link.json | 지하철 역 간 경로
subway_station.json | 지하철 역
subway_transfer.json | 지하철 환승 정보
walk_link.json | 도보 경로

### bicycle_link.json

```json
{
    "9NdQRY1Z": {
        "type": "bicycle",
        "from": "jAvstpcC",
        "to": "gAKswAi9L",
        "time": 6.864834561570508,
        "lineId": ""
    }
}
```

### bicycle_node.json

```json
{
    "jAvstpcC": {
        "address": "서울특별시 광진구 화양동 169-1",
        "name": "어린이대공원역 3번출구 앞",
        "location": {
            "latitude": 37.54707,
            "longitude": 127.074272
        },
        "id": "500",
        "type": "sharing_bicycle_01"
    }
}
```

### bus_line.json

```json
{
    "08lw8FIK": {
        "id": "100000010",
        "name": "12345",
        "type": "bus"
    }
}
```

### bus_link.json

```json
{
    "pR6XOYRi": {
        "from": "oMSvMJElEA",
        "to": "NxS3MnaqA",
        "time": 1.64,
        "distance": 274.0,
        "type": "bus",
        "lineId": "100100341"
    }
}
```

### bus_station_to_key.json

```json
{
    "115000073":"RMEIMFP4Z2",
    "115000600":"oxS3qaEsZQ",
    "115000603":"NGXBM-QFwP",
    "115000634":"RxXvq0buZ9",
    "115000896":"oqXBqurukf"
}
```

### bus_station.json

```json
{
    "lqpvqXeP":{
        "type":"bus",
        "address":"",
        "name":"개화검문소",
        "location":{
            "latitude":37.5785277,
            "longitude":126.799863985
        },
        "id":"16170",
        "stationId":"115000073"
    }
}
```

### car_node.json

```json
{
    "fghz3QKZ": {
        "address": "서울 금천구 시흥동 939-4",
        "name": "GS칼텍스 일신",
        "location": {
            "latitude": 37.44437,
            "longitude": 126.9042
        },
        "type": [
            "sharing_car_02"
        ],
        "id": "1841"
    }
}
```

### gate_link.json

```json
{
    "bPyEDcSL": {
        "type": "walk",
        "from": "gqOSeMpr",
        "to": "nUL1FJMtGf",
        "time": 5,
        "lineId": "line_id"
    }
}
```

### subway_gate.json

```json
{
    "gqOSeMpr": {
        "name": "대야미역 4호선 1번출구",
        "type": "subway_gate",
        "location": {
            "latitude": 37.32782278091888,
            "longitude": 126.91698923445665
        },
        "address": "경기 군포시 대야미동"
    }
}
```

### subway_line.json

```json
{
    "60kz0dQg": {
        "name": "1호선",
        "type": "subway",
        "id": "1"
    }
}
```

### subway_link.json

```json
{
    "FoD5oC6I": {
        "type": "subway",
        "from": null,
        "to": null,
        "time": 1.5,
        "lineId": 3
    }
}
```

### subway_station.json

```json
{
    "zZJNY2_f": {
        "type": "subway",
        "location": {
            "latitude": 37.540693,
            "longitude": 127.07023
        },
        "name": "건대입구",
        "address": "",
        "fr_code": "727",
        "line_num": "7"
    }
}
```

### subway_transfer.json

```json
{
    "uZq5ZPHYecf": {
        "from": "zZJNY2_f",
        "to": "WZq5ZYy_K",
        "time": 5,
        "lineId": "line_id",
        "type": "transfer"
    }
}
```

### walk_link.json

```json
{
    "gq4xq3yF": {
        "type": "walk",
        "from": "gqOSeMpr",
        "to": "RGSvx1bIAA",
        "time": 4,
        "lineId": "line_id"
    }
}
```
