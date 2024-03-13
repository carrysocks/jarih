import requests
import xmljson
import xml.etree.ElementTree as ET
import json
import datetime
import logging
import time
import os
import csv

root_path = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(root_path, "logs/data.log")
resource_path = os.path.join(root_path, "resources")
csv_file_path = os.path.join(resource_path, "bus_data_219000013.csv")

logging.basicConfig(filename=log_file_path,
                    level=logging.WARNING,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def store_bus_data():
    """ 현재 시간에 해당하는 버스 데이터를 수집하여 csv 파일로 저장하는 함수 """

    with open(f"{resource_path}/route.json", "r") as f:
        route_map = json.load(f)

    with open(f"{resource_path}/station.json", "r") as f:
        station_map = json.load(f)

    base_url = "http://openapi.gbis.go.kr/ws/rest/buslocationservice?serviceKey=1234567890&routeId={}"
    route_id = "219000013"
    route_name = "1000"
    url = base_url.format(route_id)
    response = requests.get(url)
    xml_str = response.text

    xml_element = ET.fromstring(xml_str)
    json_data = xmljson.parker.data(xml_element)

    if len(json_data) == 1 or json_data["msgHeader"]["resultCode"] != 0:
        logging.warning(f"Request ignored or result is unexpected: {json_data}")
        return

    result = []

    for data in json_data["msgBody"]["busLocationList"]:
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            plate_no = data["plateNo"]
            plate_type = data["plateType"]

            remain_seat_cnt = data.get("remainSeatCnt")
            if remain_seat_cnt in [None, -1, "-1"]:
                logging.warning(f"Data without remainSeatCnt received: {data}")
                continue

            station_id = data["stationId"]
            station_name = station_map.get(str(station_id), "Unknown Station")
            if station_name == "Unknown Station":
                logging.warning(f"Unknown station ID received: {station_id}")
                continue
            station_seq = data["stationSeq"]

            result.append([now, plate_no, plate_type, route_id, route_name, remain_seat_cnt, station_id,
                           station_name, station_seq])


        except Exception as e:
            logging.error(f"Error processing data: {data}, with error: {e}")

    with open(csv_file_path, "a", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        if os.stat(csv_file_path).st_size == 0:
            writer.writerow(["now", "plate_no", "plate_type", "route_id", "route_name", "remain_seat_cnt", "station_id",
                             "station_name", "station_seq"])
        for record in result:
            writer.writerow(record)

    print("len(result): ", len(result))
    print("result : ")
    print(result)


while True:
    time.sleep(5)
    try:
        store_bus_data()
    except Exception as e:
        logging.error(f"Error in store_bus_data: {e}")