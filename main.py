import json
import requests
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CWA_API_KEY = os.environ.get("CWA_API_KEY")
LINE_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN")
USER_ID = os.environ.get("USER_ID")


def main():
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-B969C6D1-AF9D-46C1-B2A2-8B3F25A3F7A1&locationName=臺中市"
    response = requests.get(url, verify=False).json()

    all_locations = response["records"]["location"]
    taichung_data = next(item for item in all_locations if item["locationName"] == "臺中市")

    weather_elements = taichung_data["weatherElement"]

    pop_element = next((item for item in weather_elements if item["elementName"] in ["PoP12h", "PoP"]), None)
     
    if pop_element and "time" in pop_element and len(pop_element["time"]) > 0:
        time_data = pop_element["time"][0]
        if "elementValue" in time_data:
            rain_chance = int(time_data["elementValue"][0]["value"])
        else:
            rain_chance = int(time_data["parameter"]["parameterName"])
    else:
        rain_chance = 0
        
    threshold = 40
    
    if rain_chance >= threshold:
        line_url = "https://api.line.me/v2/bot/message/push"
        headers = {
            "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "to": USER_ID,
            "messages": [{
                "type": "text",
                "text": f"🌧️ 【出門提醒】目前台中預報降雨機率達 {rain_chance}%，出門記得帶傘喔！"
            }]
        }
        res = requests.post(line_url, headers=headers, json=payload)
        print(f"發送成功，LINE 回傳狀態代碼：{res.status_code}")
    else:
        print(f"今日降雨機率：{rain_chance}%，未達門檻不發送通知")

if __name__ == "__main__":
    main()
